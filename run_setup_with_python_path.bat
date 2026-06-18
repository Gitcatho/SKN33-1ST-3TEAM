@echo off
setlocal

cd /d "%~dp0"

echo ========================================
echo SKN33-1ST-3TEAM setup launcher
echo ========================================
echo.
echo Paste the full path to python.exe.
echo Example: C:\Users\your-name\AppData\Local\Programs\Python\Python312\python.exe
echo.
set /p PYTHON_EXE=python.exe path: 

if not exist "%PYTHON_EXE%" (
    echo.
    echo Python executable was not found:
    echo %PYTHON_EXE%
    echo.
    pause
    exit /b 1
)

powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0setup\bootstrap.ps1" -PythonCommand "%PYTHON_EXE%"
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
