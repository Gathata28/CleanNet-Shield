#!/usr/bin/env python3
"""
Launcher script for Adult Content Blocker & Recovery Tool
This script handles basic setup and launches the main application
"""

import sys
import os
import subprocess

def check_python_version():
    """Check if Python version is adequate"""
    if sys.version_info < (3, 8):
        print("ERROR: Python 3.8 or higher is required.")
        print(f"You are running Python {sys.version}")
        return False
    return True

def check_admin_privileges():
    """Check if running with admin privileges on Windows"""
    if os.name == 'nt':  # Windows
        try:
            import ctypes
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
    return True  # Non-Windows systems

def install_dependencies():
    """Install required dependencies"""
    try:
        import requests
        print("✓ All dependencies are available")
        return True
    except ImportError:
        print("Installing required dependencies...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
            print("✓ Dependencies installed successfully")
            return True
        except subprocess.CalledProcessError:
            print("ERROR: Failed to install dependencies. Please run:")
            print("pip install requests")
            return False

def main():
    """Main launcher function"""
    import argparse
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="CleanNet Shield Launcher")
    parser.add_argument("--force-run", action="store_true", 
                       help="Skip admin privilege check (use when already running as admin)")
    args = parser.parse_args()
    
    print("=" * 60)
    print("🛡️  ADULT CONTENT BLOCKER & RECOVERY TOOL")
    print("=" * 60)
    
    # Check Python version
    if not check_python_version():
        input("Press Enter to exit...")
        return
    
    # Check admin privileges on Windows (unless force-run is specified)
    if not args.force_run and os.name == 'nt' and not check_admin_privileges():
        print("⚠️  WARNING: This application requires administrator privileges")
        print("   Please right-click and 'Run as administrator'")
        print("   Some features may not work without admin access.")
        
        response = input("\\nContinue anyway? (y/N): ").strip().lower()
        if response != 'y':
            return
    else:
        print("✓ Running with appropriate privileges")
    
    # Install dependencies if needed
    if not install_dependencies():
        input("Press Enter to exit...")
        return
    
    # Add current directory to path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)
    
    # Launch main application
    try:
        print("\\n🚀 Launching Adult Content Blocker...")
        from main import AdultBlockerApp
        
        app = AdultBlockerApp()
        app.run()
        
    except ImportError as e:
        print(f"ERROR: Failed to import main application: {e}")
        print("Please ensure all required files are present.")
        input("Press Enter to exit...")
    except Exception as e:
        print(f"ERROR: Application failed to start: {e}")
        print("Check the logs for more details.")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()
