@echo off
REM CleanNet Shield - Windows Admin Launcher
REM This batch file launches the application with proper admin privileges

echo.
echo ========================================
echo    CleanNet Shield - Admin Launcher
echo ========================================
echo.

REM Check if we're running as administrator
net session >nul 2>&1
if %errorLevel% == 0 (
    echo ✅ Running with administrator privileges
    goto :launch
) else (
    echo ⚠️  Administrator privileges required
    echo    You can either:
    echo    1. Right-click this file and 'Run as administrator'
    echo    2. Run from an elevated command prompt
    echo    3. Continue without admin (some features may not work)
    echo.
    set /p choice="Continue without admin privileges? (y/N): "
    if /i "%choice%"=="y" goto :launch
    echo    Exiting...
    pause
    exit /b 0
)

:launch
echo 📁 Current directory: %CD%
echo.

REM Navigate to project root (parent of scripts directory)
cd /d "%~dp0\.."

echo 📁 Project directory: %CD%
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo    Please install Python from: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo ✅ Python is available
python --version
echo.

REM Check if main.py exists
if not exist "main.py" (
    echo ❌ main.py not found in current directory
    echo    Make sure you're running this from the CleanNet Shield folder
    echo.
    pause
    exit /b 1
)

echo ✅ Application files found
echo.

REM Launch the application directly
echo 🚀 Launching CleanNet Shield...
echo.

python main.py

if errorlevel 1 (
    echo.
    echo ❌ Application encountered an error
    echo Check the error messages above for details
    echo.
) else (
    echo.
    echo ✅ Application closed successfully
)

echo.
echo Press any key to exit...
pause >nul
