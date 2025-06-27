#!/usr/bin/env python3
"""
Debug script to test CleanNet Shield imports and functionality
"""

import sys
import os

def test_imports():
    """Test all module imports"""
    print("🧪 Testing CleanNet Shield imports...")
    
    try:
        # Test standard library imports
        import smtplib
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart
        print("✅ Email modules imported")
        
        import json
        import datetime
        print("✅ Standard library modules imported")
        
        # Test external imports
        import requests
        print("✅ Requests module imported")
        
        # Set up path for local imports
        sys.path.insert(0, os.path.dirname(__file__))
        
        # Test utility imports
        from utils.logger import Logger
        print("✅ Logger imported")
        
        from utils.permissions import check_admin_rights
        print("✅ Permissions imported")
        
        # Test blocker imports
        from blocker.hosts_blocker import HostsBlocker
        print("✅ HostsBlocker imported")
        
        from blocker.dns_config import DNSConfig
        print("✅ DNSConfig imported")
        
        from blocker.blocklist_updater import BlocklistUpdater
        print("✅ BlocklistUpdater imported")
        
        # Test recovery imports
        from recovery.journaling import Journal
        print("✅ Journal imported")
        
        from recovery.streak_tracker import StreakTracker
        print("✅ StreakTracker imported")
        
        from recovery.accountability import AccountabilityBot
        print("✅ AccountabilityBot imported")
        
        print("\n🎉 All imports successful!")
        return True
        
    except Exception as e:
        print(f"\n❌ Import error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_object_creation():
    """Test creating objects"""
    print("\n🔧 Testing object creation...")
    
    try:
        sys.path.insert(0, os.path.dirname(__file__))
        
        from utils.logger import Logger
        logger = Logger()
        print("✅ Logger created")
        
        from utils.permissions import check_admin_rights
        admin_status = check_admin_rights()
        print(f"✅ Admin check: {admin_status}")
        
        from blocker.hosts_blocker import HostsBlocker
        hosts_blocker = HostsBlocker()
        print("✅ HostsBlocker created")
        
        from blocker.dns_config import DNSConfig
        dns_config = DNSConfig()
        print("✅ DNSConfig created")
        
        from recovery.journaling import Journal
        journal = Journal()
        print("✅ Journal created")
        
        from recovery.streak_tracker import StreakTracker
        streak_tracker = StreakTracker()
        print("✅ StreakTracker created")
        
        # Test the problematic module last
        from recovery.accountability import AccountabilityBot
        accountability = AccountabilityBot()
        print("✅ AccountabilityBot created")
        
        print("\n🎉 All objects created successfully!")
        return True
        
    except Exception as e:
        print(f"\n❌ Object creation error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main test function"""
    print("🛡️ CleanNet Shield - Debug Test")
    print("=" * 40)
    
    # Test imports
    if not test_imports():
        return False
    
    # Test object creation
    if not test_object_creation():
        return False
    
    print("\n✅ All tests passed!")
    print("🚀 CleanNet Shield is ready to run!")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
