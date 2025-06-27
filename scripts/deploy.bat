@echo off
REM CleanNet Shield - Repository Deployment Script
REM This script prepares and deploys the project to a git repository

echo.
echo ========================================
echo CleanNet Shield - Repository Deployment
echo ========================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python first: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo Python is available
echo.

REM Check if we're in the right directory
if not exist "main.py" (
    echo ERROR: This script must be run from the CleanNet Shield project directory
    echo Make sure you're in the folder containing main.py
    echo.
    pause
    exit /b 1
)

echo Project directory confirmed
echo.

REM Run the Python deployment script
echo Running deployment script...
echo.
python deploy.py

if errorlevel 1 (
    echo.
    echo ERROR: Deployment script failed
    echo Check the error messages above
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo Deployment preparation complete!
echo ========================================
echo.
echo Your CleanNet Shield project is now ready for repository deployment.
echo.
echo Quick Git commands for reference:
echo   git status                           - Check repository status
echo   git add .                           - Add all files
echo   git commit -m "Your message"        - Create a commit
echo   git remote add origin ^<URL^>         - Add remote repository
echo   git push -u origin main             - Push to remote repository
echo.
echo Happy coding! 🚀
echo.
pause
