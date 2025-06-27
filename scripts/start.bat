@echo off
REM Adult Content Blocker & Recovery Tool Launcher
REM This batch file launches the Python application with proper setup

title Adult Content Blocker & Recovery Tool

echo.
echo ================================================================
echo           ADULT CONTENT BLOCKER ^& RECOVERY TOOL
echo ================================================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo.
    echo Please install Python 3.8+ from https://python.org
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

REM Check if we're running as administrator
net session >nul 2>&1
if errorlevel 1 (
    echo WARNING: Not running as administrator
    echo Some features may not work properly
    echo.
    echo To run as administrator:
    echo 1. Right-click this batch file
    echo 2. Select "Run as administrator"
    echo.
    set /p choice="Continue anyway? (y/N): "
    if /i not "%choice%"=="y" exit /b 1
) else (
    echo ✓ Running as administrator
)

echo.
echo Starting application...
echo.

REM Launch the Python application
python launcher.py

REM Pause if there was an error
if errorlevel 1 (
    echo.
    echo Application exited with an error
    pause
)

echo.
echo Application closed
pause
