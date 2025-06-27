#!/usr/bin/env python3
"""
Student Edition Setup Script - FREE Professional Development Environment
Leverages GitHub Student Pack benefits for zero-cost premium tools
"""

import subprocess
import sys
import os
from pathlib import Path

def install_free_professional_tools():
    """Install all free professional tools available to students"""
    
    print("🎓 Setting up GitHub Student Pack Professional Environment...")
    
    # Free Professional Python Packages
    free_packages = [
        # GUI Framework (100% Free Alternative to PyQt6)
        "PySide6>=6.5.0",           # Same as PyQt6 but completely free
        
        # Database & ORM (Enterprise Grade, Free)
        "sqlalchemy>=2.0.0",       # Professional ORM
        "alembic>=1.11.0",         # Database migrations
        
        # System Integration (Free)
        "pywin32>=306",             # Windows system access
        "psutil>=5.9.0",           # System monitoring
        "watchdog>=3.0.0",         # File monitoring
        
        # Security (Free)
        "cryptography>=41.0.0",    # Professional encryption
        "keyring>=24.0.0",         # Secure credential storage
        
        # Scheduling & Automation (Free)
        "schedule>=1.2.0",         # Task scheduling
        "apscheduler>=3.10.0",     # Advanced scheduling
        
        # Modern GUI Alternatives (Free)
        "dearpygui>=1.10.0",       # Modern, fast GUI
        "customtkinter>=5.2.0",    # Modern Tkinter
        
        # Cloud & Networking (Free)
        "aiohttp>=3.8.0",          # Async HTTP
        "azure-storage-blob>=12.17.0",  # Azure integration (free credits)
        
        # AI & Analytics (Free)
        "scikit-learn>=1.3.0",     # Machine learning
        "pandas>=2.0.0",           # Data analysis
        "matplotlib>=3.7.0",       # Visualization
        
        # Development Tools (Free)
        "pytest>=7.4.0",           # Testing framework
        "black>=23.0.0",           # Code formatting
        "flake8>=6.0.0",           # Code linting
        "mypy>=1.5.0",             # Type checking
        
        # Packaging (Free)
        "cx-Freeze>=6.15.0",       # Create executables
        "setuptools>=68.0.0",      # Package building
    ]
    
    print("📦 Installing FREE professional packages...")
    for package in free_packages:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"✅ Installed: {package}")
        except subprocess.CalledProcessError:
            print(f"⚠️  Failed to install: {package}")
    
    print("\n🔧 Setting up free development tools...")
    
    # Create professional project structure
    create_professional_structure()
    
    # Setup free CI/CD with GitHub Actions
    setup_github_actions()
    
    # Create free code signing setup
    setup_code_signing()
    
    print("\n🎉 Professional development environment ready!")
    print("💰 Total cost: $0 (Thanks to GitHub Student Pack!)")

def create_professional_structure():
    """Create enterprise-grade project structure"""
    
    base_path = Path(__file__).parent
    
    # Professional directory structure
    dirs = [
        "core",           # Windows Service & Protection
        "gui_modern",     # PySide6 GUI (Free alternative)
        "monitor",        # Advanced monitoring
        "cloud",          # Free cloud integration
        "database",       # SQLite + migrations
        "security",       # Tamper protection
        "installer",      # Free installer creation
        "tests",          # Professional testing
        "docs",           # Documentation
        ".github/workflows",  # Free CI/CD
    ]
    
    for dir_name in dirs:
        dir_path = base_path / dir_name
        dir_path.mkdir(exist_ok=True)
        
        # Create __init__.py for Python packages
        if not dir_name.startswith('.'):
            (dir_path / "__init__.py").touch()
    
    print("📁 Professional project structure created")

def setup_github_actions():
    """Setup free CI/CD with GitHub Actions"""
    
    workflow_content = """
name: CleanNet Shield CI/CD

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: windows-latest
    strategy:
      matrix:
        python-version: [3.9, 3.10, 3.11]
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v3
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pytest black flake8 mypy
    
    - name: Lint with flake8
      run: |
        flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
    
    - name: Format check with black
      run: |
        black --check .
    
    - name: Type check with mypy
      run: |
        mypy --ignore-missing-imports .
    
    - name: Test with pytest
      run: |
        pytest tests/ -v
    
    - name: Build executable
      run: |
        python setup.py build
    
  security:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Run security analysis
      uses: github/codeql-action/analyze@v2
      with:
        languages: python
"""
    
    workflow_path = Path(__file__).parent / ".github" / "workflows" / "ci.yml"
    workflow_path.parent.mkdir(parents=True, exist_ok=True)
    workflow_path.write_text(workflow_content)
    
    print("🔄 Free CI/CD pipeline configured")

def setup_code_signing():
    """Setup free code signing for student projects"""
    
    signing_script = """
# Free Code Signing Setup for Students
# Uses self-signed certificates for development

# Generate self-signed certificate (FREE)
$cert = New-SelfSignedCertificate -Type CodeSigningCert -Subject "CN=CleanNet Shield Student Edition" -KeyAlgorithm RSA -KeyLength 2048 -Provider "Microsoft Enhanced RSA and AES Cryptographic Provider" -KeyExportPolicy Exportable -KeyUsage DigitalSignature -CertStoreLocation Cert:\\CurrentUser\\My

# Sign the executable
Set-AuthenticodeSignature -FilePath "dist\\CleanNetShield.exe" -Certificate $cert

Write-Host "✅ Executable signed with student certificate"
"""
    
    signing_path = Path(__file__).parent / "scripts" / "sign_student.ps1"
    signing_path.parent.mkdir(exist_ok=True)
    signing_path.write_text(signing_script)
    
    print("🔒 Free code signing setup created")

if __name__ == "__main__":
    install_free_professional_tools()
