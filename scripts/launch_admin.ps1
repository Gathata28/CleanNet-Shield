# CleanNet Shield - Admin Launcher
# This script automatically requests admin privileges and launches the application

param([switch]$Elevated)

function Test-Admin {
    $currentUser = [Security.Principal.WindowsIdentity]::GetCurrent()
    $principal = New-Object Security.Principal.WindowsPrincipal($currentUser)
    return $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

function Start-Elevated {
    Write-Host "🔒 Requesting administrator privileges..." -ForegroundColor Yellow
    Start-Process PowerShell -Verb RunAs -ArgumentList ("-NoProfile -ExecutionPolicy Bypass -File `"{0}`" -Elevated" -f $PSCommandPath)
}

# Check if we need to elevate
if ((Test-Admin) -eq $false) {
    if ($Elevated) {
        Write-Host "❌ Failed to obtain administrator privileges" -ForegroundColor Red
        Write-Host "Please run this script as administrator manually" -ForegroundColor Yellow
        Read-Host "Press Enter to exit"
        exit 1
    } else {
        Start-Elevated
        exit 0
    }
}

# We have admin privileges, proceed with launch
Write-Host "✅ Administrator privileges confirmed" -ForegroundColor Green
Write-Host ""

# Get script directory
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectDir = Split-Path -Parent $scriptDir

# Change to project directory
Set-Location $projectDir

Write-Host "📁 Project directory: $projectDir" -ForegroundColor Cyan
Write-Host ""

# Check if Python is available
try {
    $pythonVersion = python --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Python found: $pythonVersion" -ForegroundColor Green
    } else {
        throw "Python not found"
    }
} catch {
    Write-Host "❌ Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python from: https://www.python.org/downloads/" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Launch the application
Write-Host "🚀 Launching CleanNet Shield..." -ForegroundColor Green
Write-Host ""

try {
    # Use launcher.py with force flag to skip admin check since we already have admin
    python launcher.py --force-run
} catch {
    Write-Host "❌ Failed to launch application: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "Try running 'python main.py' manually" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Press any key to exit..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
