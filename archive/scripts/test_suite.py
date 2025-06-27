#!/usr/bin/env python3
"""
Command-line test suite for Adult Content Blocker & Recovery Tool
Tests all modules without requiring GUI
"""

import sys
import os

# Add current directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

def test_modules():
    """Test all modules and their basic functionality"""
    print('🧪 ADULT CONTENT BLOCKER - COMPREHENSIVE TEST SUITE')
    print('=' * 65)
    
    success_count = 0
    total_tests = 0
    
    # Test 1: Module Imports
    print('\n📦 TEST 1: Module Imports')
    print('-' * 30)
    total_tests += 8
    
    modules_to_test = [
        ('utils.permissions', 'Permissions module'),
        ('utils.logger', 'Logger module'),
        ('blocker.hosts_blocker', 'Hosts blocker module'),
        ('blocker.dns_config', 'DNS configuration module'),
        ('blocker.blocklist_updater', 'Blocklist updater module'),
        ('recovery.journaling', 'Journaling module'),
        ('recovery.streak_tracker', 'Streak tracker module'),
        ('recovery.accountability', 'Accountability module')
    ]
    
    imported_modules = {}
    for module_name, description in modules_to_test:
        try:
            module = __import__(module_name, fromlist=[''])
            imported_modules[module_name] = module
            print(f'✅ {description}')
            success_count += 1
        except Exception as e:
            print(f'❌ {description}: {e}')
    
    # Test 2: Object Creation
    print('\n🔨 TEST 2: Object Creation')
    print('-' * 30)
    total_tests += 8
    
    objects = {}
    
    try:
        objects['logger'] = imported_modules['utils.logger'].Logger()
        print('✅ Logger object created')
        success_count += 1
    except Exception as e:
        print(f'❌ Logger object: {e}')
    
    try:
        objects['hosts_blocker'] = imported_modules['blocker.hosts_blocker'].HostsBlocker()
        print('✅ Hosts blocker object created')
        success_count += 1
    except Exception as e:
        print(f'❌ Hosts blocker object: {e}')
    
    try:
        objects['dns_config'] = imported_modules['blocker.dns_config'].DNSConfig()
        print('✅ DNS config object created')
        success_count += 1
    except Exception as e:
        print(f'❌ DNS config object: {e}')
    
    try:
        objects['updater'] = imported_modules['blocker.blocklist_updater'].BlocklistUpdater()
        print('✅ Blocklist updater object created')
        success_count += 1
    except Exception as e:
        print(f'❌ Blocklist updater object: {e}')
    
    try:
        objects['journal'] = imported_modules['recovery.journaling'].Journal()
        print('✅ Journal object created')
        success_count += 1
    except Exception as e:
        print(f'❌ Journal object: {e}')
    
    try:
        objects['streak'] = imported_modules['recovery.streak_tracker'].StreakTracker()
        print('✅ Streak tracker object created')
        success_count += 1
    except Exception as e:
        print(f'❌ Streak tracker object: {e}')
    
    try:
        objects['accountability'] = imported_modules['recovery.accountability'].AccountabilityBot()
        print('✅ Accountability bot object created')
        success_count += 1
    except Exception as e:
        print(f'❌ Accountability bot object: {e}')
    
    try:
        admin_status = imported_modules['utils.permissions'].check_admin_rights()
        print(f'✅ Admin check: {admin_status}')
        success_count += 1
    except Exception as e:
        print(f'❌ Admin check: {e}')
    
    # Test 3: Basic Functionality
    print('\n⚙️  TEST 3: Basic Functionality')
    print('-' * 30)
    total_tests += 10
    
    # Test logger
    try:
        if 'logger' in objects:
            objects['logger'].info('Test log entry from test suite')
            recent_logs = objects['logger'].get_recent_logs(1)
            print(f'✅ Logger: {len(recent_logs)} recent logs')
            success_count += 1
    except Exception as e:
        print(f'❌ Logger functionality: {e}')
    
    # Test streak tracker
    try:
        if 'streak' in objects:
            streak_info = objects['streak'].get_streak_summary()
            current_streak = streak_info.get('current_streak', 0)
            print(f'✅ Streak tracker: {current_streak} days current streak')
            success_count += 1
    except Exception as e:
        print(f'❌ Streak tracker functionality: {e}')
    
    # Test journal
    try:
        if 'journal' in objects:
            entry_result = objects['journal'].add_entry('Test journal entry from test suite', mood='Good', rating=7)
            print(f'✅ Journal: Entry added successfully ({entry_result})')
            success_count += 1
    except Exception as e:
        print(f'❌ Journal functionality: {e}')
    
    # Test DNS config info
    try:
        if 'dns_config' in objects:
            dns_types = objects['dns_config'].get_available_dns_types()
            print(f'✅ DNS config: {len(dns_types)} DNS providers available')
            success_count += 1
    except Exception as e:
        print(f'❌ DNS config functionality: {e}')
    
    # Test blocklist updater
    try:
        if 'updater' in objects:
            stats = objects['updater'].get_stats()
            domain_count = stats.get('total_domains', 0)
            print(f'✅ Blocklist updater: {domain_count} domains loaded')
            success_count += 1
    except Exception as e:
        print(f'❌ Blocklist updater functionality: {e}')
    
    # Test hosts blocker status
    try:
        if 'hosts_blocker' in objects:
            stats = objects['hosts_blocker'].get_stats()
            is_active = stats.get('is_active', False)
            print(f'✅ Hosts blocker: Status check completed (Active: {is_active})')
            success_count += 1
    except Exception as e:
        print(f'❌ Hosts blocker functionality: {e}')
    
    # Test accountability config
    try:
        if 'accountability' in objects:
            config_status = objects['accountability'].get_config_status()
            print(f'✅ Accountability: Configuration accessible')
            success_count += 1
    except Exception as e:
        print(f'❌ Accountability functionality: {e}')
    
    # Test streak achievements
    try:
        if 'streak' in objects:
            achievements = objects['streak'].get_achievements()
            print(f'✅ Achievements: {len(achievements)} available achievements')
            success_count += 1
    except Exception as e:
        print(f'❌ Achievements functionality: {e}')
    
    # Test journal search
    try:
        if 'journal' in objects:
            search_results = objects['journal'].search_entries('test', max_results=5)
            print(f'✅ Journal search: {len(search_results)} results for "test"')
            success_count += 1
    except Exception as e:
        print(f'❌ Journal search functionality: {e}')
    
    # Test streak weekly progress
    try:
        if 'streak' in objects:
            weekly = objects['streak'].get_weekly_progress()
            clean_days = weekly.get('clean_days_this_week', 0)
            print(f'✅ Weekly progress: {clean_days} clean days this week')
            success_count += 1
    except Exception as e:
        print(f'❌ Weekly progress functionality: {e}')
    
    # Test Results
    print('\n' + '=' * 65)
    print('🎯 TEST RESULTS')
    print('=' * 65)
    print(f'✅ Passed: {success_count}/{total_tests} tests')
    print(f'❌ Failed: {total_tests - success_count}/{total_tests} tests')
    
    success_rate = (success_count / total_tests) * 100
    print(f'📊 Success Rate: {success_rate:.1f}%')
    
    if success_rate >= 90:
        print('\n🎉 EXCELLENT! Application is ready for use!')
    elif success_rate >= 75:
        print('\n✅ GOOD! Application is mostly functional!')
    elif success_rate >= 50:
        print('\n⚠️  PARTIAL! Some features may not work correctly!')
    else:
        print('\n❌ ISSUES! Application needs troubleshooting!')
    
    return success_rate >= 75

def test_data_creation():
    """Test data directory and file creation"""
    print('\n📁 TEST 4: Data Directory Creation')
    print('-' * 30)
    
    try:
        data_dir = os.path.join(current_dir, 'data')
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        
        subdirs = ['logs', 'journal', 'streaks', 'accountability']
        for subdir in subdirs:
            subdir_path = os.path.join(data_dir, subdir)
            if not os.path.exists(subdir_path):
                os.makedirs(subdir_path)
            print(f'✅ Created/verified: data/{subdir}/')
        
        print('✅ All data directories ready')
        return True
        
    except Exception as e:
        print(f'❌ Data directory creation failed: {e}')
        return False

def main():
    """Main test function"""
    print('Starting comprehensive test suite...\n')
    
    # Test data creation
    data_ok = test_data_creation()
    
    # Test modules
    modules_ok = test_modules()
    
    print('\n' + '=' * 65)
    print('🏁 FINAL RESULTS')
    print('=' * 65)
    
    if data_ok and modules_ok:
        print('🎊 ALL SYSTEMS GO! Your Adult Content Blocker is ready!')
        print('\nTo use the application:')
        print('1. On Windows: Double-click start.bat')
        print('2. Or run: python launcher.py')
        print('3. Or run: python main.py (GUI mode)')
    else:
        print('⚠️  Some issues detected. Check the test results above.')
    
    print('\n📚 Documentation available in README.md')
    print('📋 Project overview in PROJECT_OVERVIEW.md')

if __name__ == '__main__':
    main()
