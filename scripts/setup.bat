@echo off
echo ================================================================
echo           SETTING UP ADULT CONTENT BLOCKER
echo ================================================================
echo.

echo Installing required dependencies...
python -m pip install requests
if errorlevel 1 (
    echo Failed to install requests. Trying alternative method...
    python -c "import subprocess; subprocess.run(['pip', 'install', 'requests'])"
)

echo.
echo Testing installation...
python -c "import requests; print('✅ Requests installed successfully!')"
if errorlevel 1 (
    echo ❌ Failed to install requests library
    echo Please try manually: pip install requests
    pause
    exit /b 1
)

echo.
echo Running comprehensive tests...
python test_suite.py

echo.
echo Setup complete! You can now run:
echo   python main.py        (GUI mode)
echo   python launcher.py    (Full launcher)
echo   start.bat            (Batch launcher)
echo.
pause
