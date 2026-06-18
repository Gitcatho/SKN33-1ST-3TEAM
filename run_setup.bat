@echo off
setlocal

cd /d "%~dp0"

echo ========================================
echo SKN33-1ST-3TEAM setup launcher
echo ========================================
echo.
echo This will run setup\bootstrap.ps1.
echo You may be asked for DB and MySQL passwords.
echo.

powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0setup\bootstrap.ps1"
if errorlevel 1 (
    echo.
    echo ========================================
    echo Setup failed. Please check the error above.
    echo ========================================
    pause
    exit /b 1
)

echo.
echo ========================================
echo Setup process finished.
echo If Streamlit is running, keep this window open.
echo ========================================
pause
