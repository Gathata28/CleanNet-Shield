#!/usr/bin/env python3
"""
Simple functionality test for CleanNet Shield
Tests core features without requiring GUI interaction
"""

import sys
import os

# Add project to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_core_functionality():
    """Test core functionality without GUI"""
    
    print("🧪 CleanNet Shield - Core Functionality Test")
    print("=" * 50)
    
    try:
        # Test logger
        from utils.logger import Logger
        logger = Logger()
        logger.info("Test log entry")
        print("✅ Logger working")
        
        # Test permissions
        from utils.permissions import check_admin_rights
        is_admin = check_admin_rights()
        print(f"✅ Admin check: {'Yes' if is_admin else 'No'}")
        
        # Test hosts blocker
        from blocker.hosts_blocker import HostsBlocker
        hosts = HostsBlocker()
        is_active = hosts.is_active()
        print(f"✅ Hosts blocker: {'Active' if is_active else 'Inactive'}")
        
        # Test DNS config
        from blocker.dns_config import DNSConfig
        dns = DNSConfig()
        print("✅ DNS config working")
        
        # Test streak tracker
        from recovery.streak_tracker import StreakTracker
        tracker = StreakTracker()
        current_streak = tracker.get_current_streak()
        print(f"✅ Streak tracker: {current_streak} days")
        
        # Test journal
        from recovery.journaling import Journal
        journal = Journal()
        print("✅ Journal system working")
        
        # Test blocklist updater
        from blocker.blocklist_updater import BlocklistUpdater
        updater = BlocklistUpdater()
        stats = updater.get_stats()
        print(f"✅ Blocklist updater: {stats.get('total_domains', 0)} domains")
        
        print("\n🎉 All core functionality tests passed!")
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_core_functionality()
    if not success:
        input("\nPress Enter to exit...")
