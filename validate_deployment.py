#!/usr/bin/env python3
"""
CleanNet Shield - Comprehensive Test & Validation Suite
This script performs final validation before deployment
"""

import sys
import os
import json
import traceback
from datetime import datetime

# Add project to path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

def test_all_modules():
    """Test all module imports and basic functionality"""
    
    tests = {
        "Module Imports": False,
        "Core Objects": False,
        "File Structure": False,
        "Configuration": False,
        "Data Directories": False,
        "Documentation": False,
        "Scripts": False,
        "Deployment Files": False
    }
    
    print("🔍 CleanNet Shield - Comprehensive Validation Suite")
    print("=" * 60)
    print(f"📅 Test Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # Test 1: Module Imports
    print("\n📦 Testing Module Imports...")
    try:
        from utils.logger import Logger
        from utils.permissions import check_admin_rights
        from blocker.hosts_blocker import HostsBlocker
        from blocker.dns_config import DNSConfig
        from blocker.blocklist_updater import BlocklistUpdater
        from recovery.journaling import Journal
        from recovery.streak_tracker import StreakTracker
        from recovery.accountability import AccountabilityBot
        print("✅ All modules imported successfully")
        tests["Module Imports"] = True
    except Exception as e:
        print(f"❌ Module import failed: {e}")
    
    # Test 2: Core Objects
    print("\n🏗️ Testing Object Creation...")
    try:
        logger = Logger()
        hosts = HostsBlocker()
        dns = DNSConfig()
        updater = BlocklistUpdater()
        journal = Journal()
        tracker = StreakTracker()
        accountability = AccountabilityBot()
        print("✅ All core objects created successfully")
        tests["Core Objects"] = True
    except Exception as e:
        print(f"❌ Object creation failed: {e}")
    
    # Test 3: File Structure
    print("\n📁 Testing File Structure...")
    required_files = [
        "main.py", "launcher.py", "requirements.txt",
        "README.md", "LICENSE", "CONTRIBUTING.md",
        "setup.py", "RELEASE_NOTES.md"
    ]
    
    required_dirs = [
        "blocker", "recovery", "utils", "config", 
        "scripts", "docs", "data"
    ]
    
    missing_files = []
    missing_dirs = []
    
    for file in required_files:
        if not os.path.exists(os.path.join(project_root, file)):
            missing_files.append(file)
    
    for dir in required_dirs:
        if not os.path.exists(os.path.join(project_root, dir)):
            missing_dirs.append(dir)
    
    if not missing_files and not missing_dirs:
        print("✅ All required files and directories present")
        tests["File Structure"] = True
    else:
        print(f"❌ Missing files: {missing_files}")
        print(f"❌ Missing directories: {missing_dirs}")
    
    # Test 4: Configuration
    print("\n⚙️ Testing Configuration...")
    try:
        config_file = os.path.join(project_root, "config", "blocker_config.json")
        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                config = json.load(f)
            print("✅ Configuration file valid")
            tests["Configuration"] = True
        else:
            print("❌ Configuration file missing")
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
    
    # Test 5: Data Directories
    print("\n💾 Testing Data Directory Creation...")
    try:
        data_dirs = ["logs", "journal", "streaks", "accountability"]
        data_root = os.path.join(project_root, "data")
        
        for dir_name in data_dirs:
            dir_path = os.path.join(data_root, dir_name)
            os.makedirs(dir_path, exist_ok=True)
        
        print("✅ Data directories created successfully")
        tests["Data Directories"] = True
    except Exception as e:
        print(f"❌ Data directory creation failed: {e}")
    
    # Test 6: Documentation
    print("\n📚 Testing Documentation...")
    doc_files = [
        "docs/README.md", "docs/INSTALLATION_GUIDE.md",
        "docs/PROJECT_OVERVIEW.md", "docs/prd.md"
    ]
    
    doc_exists = all(os.path.exists(os.path.join(project_root, doc)) for doc in doc_files)
    
    if doc_exists:
        print("✅ All documentation files present")
        tests["Documentation"] = True
    else:
        print("❌ Some documentation files missing")
    
    # Test 7: Scripts
    print("\n🚀 Testing Scripts...")
    script_files = [
        "scripts/start.bat", "scripts/setup.bat", 
        "scripts/run_admin.bat", "scripts/test_suite.py"
    ]
    
    script_exists = all(os.path.exists(os.path.join(project_root, script)) for script in script_files)
    
    if script_exists:
        print("✅ All script files present")
        tests["Scripts"] = True
    else:
        print("❌ Some script files missing")
    
    # Test 8: Deployment Files
    print("\n📦 Testing Deployment Files...")
    deploy_files = [
        ".gitignore", "deploy.py", "DEPLOYMENT_SUCCESS.md"
    ]
    
    deploy_exists = all(os.path.exists(os.path.join(project_root, deploy)) for deploy in deploy_files)
    
    if deploy_exists:
        print("✅ All deployment files present")
        tests["Deployment Files"] = True
    else:
        print("❌ Some deployment files missing")
    
    return tests

def generate_test_report(tests):
    """Generate a test report"""
    
    print("\n" + "=" * 60)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for result in tests.values() if result)
    total = len(tests)
    success_rate = (passed / total) * 100
    
    for test_name, result in tests.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:<20} {status}")
    
    print("-" * 60)
    print(f"TOTAL TESTS:     {total}")
    print(f"PASSED:          {passed}")
    print(f"FAILED:          {total - passed}")
    print(f"SUCCESS RATE:    {success_rate:.1f}%")
    print("-" * 60)
    
    if success_rate >= 90:
        print("🎉 EXCELLENT - Ready for deployment!")
        deployment_status = "READY"
    elif success_rate >= 75:
        print("✅ GOOD - Minor issues to address")
        deployment_status = "MOSTLY_READY"
    else:
        print("⚠️ NEEDS WORK - Address failures before deployment")
        deployment_status = "NOT_READY"
    
    return deployment_status, success_rate

def create_validation_report(tests, deployment_status, success_rate):
    """Create a validation report file"""
    
    report = {
        "validation_date": datetime.now().isoformat(),
        "project_name": "CleanNet Shield",
        "version": "2.0.0",
        "tests": tests,
        "summary": {
            "total_tests": len(tests),
            "passed_tests": sum(1 for result in tests.values() if result),
            "success_rate": success_rate,
            "deployment_status": deployment_status
        },
        "recommendations": []
    }
    
    # Add recommendations based on failures
    if not tests.get("Module Imports"):
        report["recommendations"].append("Fix module import issues - check Python path and dependencies")
    
    if not tests.get("Core Objects"):
        report["recommendations"].append("Resolve object creation errors - check module dependencies")
    
    if not tests.get("File Structure"):
        report["recommendations"].append("Ensure all required files and directories are present")
    
    if not tests.get("Configuration"):
        report["recommendations"].append("Verify configuration files are valid and accessible")
    
    if deployment_status == "READY":
        report["recommendations"].append("All tests passed - project is ready for deployment!")
    
    # Save report
    report_file = os.path.join(project_root, "VALIDATION_REPORT.json")
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"\n📄 Validation report saved to: {report_file}")

def main():
    """Main validation function"""
    
    try:
        # Run all tests
        tests = test_all_modules()
        
        # Generate summary
        deployment_status, success_rate = generate_test_report(tests)
        
        # Create report file
        create_validation_report(tests, deployment_status, success_rate)
        
        # Final message
        print("\n" + "=" * 60)
        print("🎯 VALIDATION COMPLETE")
        print("=" * 60)
        
        if deployment_status == "READY":
            print("🚀 CleanNet Shield is ready for deployment!")
            print("   Run 'python deploy.py' to initialize git repository")
            print("   Then push to GitHub for public release")
        else:
            print("🔧 Please address the failed tests before deployment")
        
        return deployment_status == "READY"
        
    except Exception as e:
        print(f"\n💥 Validation script crashed: {e}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    print(f"\n{'✅ SUCCESS' if success else '❌ FAILED'}")
    input("\nPress Enter to exit...")
