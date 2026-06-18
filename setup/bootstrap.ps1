param(
    [string]$PythonCommand = "python",
    [string]$MysqlCommand = "mysql",
    [string]$MysqlRootUser = "root",
    [switch]$SkipDatabase,
    [switch]$SkipStreamlit
)

$ErrorActionPreference = "Stop"

function Write-Step {
    param([string]$Message)
    Write-Host ""
    Write-Host "==> $Message" -ForegroundColor Cyan
}

function Read-Default {
    param(
        [string]$Prompt,
        [string]$Default
    )
    $value = Read-Host "$Prompt [$Default]"
    if ([string]::IsNullOrWhiteSpace($value)) {
        return $Default
    }
    return $value
}

function Read-SecretText {
    param([string]$Prompt)
    $secure = Read-Host $Prompt -AsSecureString
    $ptr = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($secure)
    try {
        return [Runtime.InteropServices.Marshal]::PtrToStringBSTR($ptr)
    }
    finally {
        [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($ptr)
    }
}

function Assert-SafeSqlIdentifier {
    param(
        [string]$Value,
        [string]$Name
    )
    if ($Value -notmatch "^[A-Za-z0-9_]+$") {
        throw "$Name must contain only letters, numbers, and underscores: $Value"
    }
}

function Escape-SqlString {
    param([string]$Value)
    return $Value.Replace("'", "''")
}

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = (Resolve-Path (Join-Path $ScriptDir "..")).Path
Set-Location $ProjectRoot

Write-Step "Project root"
Write-Host $ProjectRoot

Write-Step "Create virtual environment"
if (-not (Test-Path ".venv")) {
    & $PythonCommand -m venv .venv
}
else {
    Write-Host ".venv already exists. Skipping creation."
}

$VenvPython = Join-Path $ProjectRoot ".venv\Scripts\python.exe"
if (-not (Test-Path $VenvPython)) {
    $CondaStylePython = Join-Path $ProjectRoot ".venv\python.exe"
    if (Test-Path $CondaStylePython) {
        $VenvPython = $CondaStylePython
    }
    else {
        throw "Virtual environment python was not found: $VenvPython"
    }
}

Write-Step "Install Python packages"
& $VenvPython -m pip install --upgrade pip
& $VenvPython -m pip install -r requirements.txt

Write-Step "Create or check .env"
$EnvPath = Join-Path $ProjectRoot ".env"
if (-not (Test-Path $EnvPath)) {
    $DbUser = Read-Default "DB_USER" "skn_ai"
    $DbPassword = Read-SecretText "DB_PASSWORD"
    $DbHost = Read-Default "DB_HOST" "localhost"
    $DbPort = Read-Default "DB_PORT" "3306"
    $DbName = Read-Default "DB_NAME" "recallcardb"
    $NaverClientId = Read-Default "NAVER_CLIENT_ID (optional)" ""
    $NaverClientSecret = Read-Default "NAVER_CLIENT_SECRET (optional)" ""

    if ($DbPort -notmatch "^\d+$") {
        throw "DB_PORT must be a number: $DbPort"
    }

    @(
        "DB_USER=$DbUser",
        "DB_PASSWORD=$DbPassword",
        "DB_HOST=$DbHost",
        "DB_PORT=$DbPort",
        "DB_NAME=$DbName",
        "",
        "NAVER_CLIENT_ID=$NaverClientId",
        "NAVER_CLIENT_SECRET=$NaverClientSecret"
    ) | Set-Content -Path $EnvPath -Encoding UTF8

    Write-Host ".env created."
}
else {
    Write-Host ".env already exists. Skipping creation."
}

$EnvValues = @{}
Get-Content $EnvPath | ForEach-Object {
    if ($_ -match "^\s*#" -or $_ -notmatch "=") {
        return
    }
    $parts = $_.Split("=", 2)
    $EnvValues[$parts[0].Trim()] = $parts[1].Trim()
}

$RequiredEnv = @("DB_USER", "DB_PASSWORD", "DB_HOST", "DB_PORT", "DB_NAME")
foreach ($key in $RequiredEnv) {
    if (-not $EnvValues.ContainsKey($key) -or [string]::IsNullOrWhiteSpace($EnvValues[$key])) {
        throw "$key is missing in .env"
    }
}

if ($EnvValues["DB_PORT"] -notmatch "^\d+$") {
    throw "DB_PORT must be a number: $($EnvValues["DB_PORT"])"
}

Assert-SafeSqlIdentifier $EnvValues["DB_USER"] "DB_USER"
Assert-SafeSqlIdentifier $EnvValues["DB_NAME"] "DB_NAME"

if (-not $SkipDatabase) {
    Write-Step "Prepare MySQL database and user"
    $mysqlCmdInfo = Get-Command $MysqlCommand -ErrorAction SilentlyContinue
    if (-not $mysqlCmdInfo) {
        throw "mysql command was not found. Install MySQL client or rerun with -SkipDatabase."
    }

    $RootPassword = Read-SecretText "MySQL root password"
    $DbUserSql = Escape-SqlString $EnvValues["DB_USER"]
    $DbPasswordSql = Escape-SqlString $EnvValues["DB_PASSWORD"]
    $DbNameSql = $EnvValues["DB_NAME"]

    $SetupSql = @"
CREATE DATABASE IF NOT EXISTS `$DbNameSql` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER IF NOT EXISTS '$DbUserSql'@'%' IDENTIFIED BY '$DbPasswordSql';
ALTER USER '$DbUserSql'@'%' IDENTIFIED BY '$DbPasswordSql';
GRANT ALL PRIVILEGES ON `$DbNameSql`.* TO '$DbUserSql'@'%';
FLUSH PRIVILEGES;
"@

    $TempSql = Join-Path $env:TEMP "skn33_setup_$([Guid]::NewGuid().ToString('N')).sql"
    $SetupSql | Set-Content -Path $TempSql -Encoding UTF8
    try {
        & $MysqlCommand -u $MysqlRootUser "--password=$RootPassword" "--host=$($EnvValues["DB_HOST"])" "--port=$($EnvValues["DB_PORT"])" $DbNameSql -e "SELECT 1;" 2>$null | Out-Null
    }
    catch {
        Write-Host "Database may not exist yet. Continuing with setup SQL."
    }
    try {
        Get-Content -Raw -Path $TempSql | & $MysqlCommand -u $MysqlRootUser "--password=$RootPassword" "--host=$($EnvValues["DB_HOST"])" "--port=$($EnvValues["DB_PORT"])"
    }
    finally {
        Remove-Item -LiteralPath $TempSql -Force -ErrorAction SilentlyContinue
    }

    Write-Step "Create tables"
    Get-Content -Raw -Path "db\recallcardb_script.sql" | & $MysqlCommand -u $EnvValues["DB_USER"] "--password=$($EnvValues["DB_PASSWORD"])" "--host=$($EnvValues["DB_HOST"])" "--port=$($EnvValues["DB_PORT"])" $EnvValues["DB_NAME"]

    Write-Step "Insert CSV data"
    & $VenvPython "db\insert_data.py"
}
else {
    Write-Host "Database setup skipped."
}

if (-not $SkipStreamlit) {
    Write-Step "Run Streamlit"
    Write-Host "Open http://localhost:8501 if the browser does not open automatically."
    & $VenvPython -m streamlit run app.py
}
else {
    Write-Host "Streamlit startup skipped."
}
