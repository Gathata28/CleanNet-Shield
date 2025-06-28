#!/usr/bin/env python3
"""
CleanNet Shield - Main Application Entry Point
Modern content blocking and recovery support application

This is the primary entry point for the CleanNet Shield application.
It provides a clean interface for launching the GUI, CLI, or running tests.

Usage:
    python main.py                    # Launch GUI (default)
    python main.py --gui             # Launch GUI explicitly
    python main.py --cli             # Launch command-line interface
    python main.py --test            # Run test suite
    python main.py --version         # Show version
"""

import sys
import argparse
from pathlib import Path

def main():
    """Main application entry point"""
    parser = argparse.ArgumentParser(
        description="CleanNet Shield - Content Blocking & Recovery Support",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py              # Launch GUI (default)
  python main.py --cli        # Launch CLI mode
  python main.py --test       # Run tests
  python main.py --version    # Show version
        """
    )
    
    parser.add_argument(
        '--gui', 
        action='store_true', 
        default=True,
        help='Launch graphical user interface (default)'
    )
    parser.add_argument(
        '--cli', 
        action='store_true',
        help='Launch command-line interface'
    )
    parser.add_argument(
        '--test', 
        action='store_true',
        help='Run test suite'
    )
    parser.add_argument(
        '--version', 
        action='version', 
        version='CleanNet Shield 2.0.0'
    )
    
    args = parser.parse_args()
    
    try:
        if args.test:
            # Run test suite
            print("🧪 Running test suite...")
            from test_phase3_gui import main as run_tests
            success = run_tests()
            sys.exit(0 if success else 1)
            
        elif args.cli:
            # Launch CLI mode
            print("🖥️  Launching CLI mode...")
            # TODO: Implement CLI interface
            print("CLI mode not yet implemented. Use --gui for now.")
            sys.exit(1)
            
        else:
            # Launch GUI (default)
            print("🚀 Launching CleanNet Shield GUI...")
            from src.gui.launcher import main as launch_gui
            launch_gui()
            
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Make sure all dependencies are installed:")
        print("   pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error launching application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 