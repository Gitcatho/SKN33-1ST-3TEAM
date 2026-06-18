# Setup Automation

Run this after cloning the repository on Windows.

The easiest way is to double-click:

```text
run_setup.bat
```

Before running it, install Python 3.10 or newer and enable `Add python.exe to PATH`.

You can also run the PowerShell script directly:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\setup\bootstrap.ps1
```

The script performs these steps:

1. Creates `.venv` if it does not exist.
2. Installs packages from `requirements.txt`.
3. Creates `.env` from prompted values if it does not exist.
4. Creates the MySQL database/user.
5. Creates tables from `db/recallcardb_script.sql`.
6. Inserts CSV data with `db/insert_data.py`.
7. Starts Streamlit with `streamlit run app.py`.

Useful options:

```powershell
.\setup\bootstrap.ps1 -SkipDatabase
.\setup\bootstrap.ps1 -SkipStreamlit
.\setup\bootstrap.ps1 -PythonCommand py
.\setup\bootstrap.ps1 -MysqlCommand "C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe"
```
