#!/usr/bin/env python3
"""
Phase 3 GUI Test Script
Tests the modern PySide6 GUI implementation
"""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_pyside6_availability():
    """Test if PySide6 is available"""
    try:
        import PySide6
        print("✅ PySide6 is available")
        return True
    except ImportError:
        print("❌ PySide6 is not available")
        print("   Install with: pip install PySide6")
        return False

def test_theme_system():
    """Test the theme system"""
    try:
        from src.gui.themes import ModernTheme, ThemeType, get_current_theme, set_theme
        
        # Test theme creation
        dark_theme = ModernTheme(ThemeType.DARK)
        light_theme = ModernTheme(ThemeType.LIGHT)
        
        print("✅ Theme system working")
        print(f"   Dark theme primary color: {dark_theme.get_color('primary')}")
        print(f"   Light theme primary color: {light_theme.get_color('primary')}")
        
        # Test global theme
        current = get_current_theme()
        print(f"   Current theme type: {current.theme_type.value}")
        
        return True
    except Exception as e:
        print(f"❌ Theme system failed: {e}")
        return False

def test_gui_launcher():
    """Test the GUI launcher"""
    try:
        from src.gui.launcher import check_pyside6_availability, check_customtkinter_availability
        
        pyside6_available = check_pyside6_availability()
        customtkinter_available = check_customtkinter_availability()
        
        print("✅ GUI launcher working")
        print(f"   PySide6 available: {pyside6_available}")
        print(f"   CustomTkinter available: {customtkinter_available}")
        
        return True
    except Exception as e:
        print(f"❌ GUI launcher failed: {e}")
        return False

def test_main_window_import():
    """Test main window import"""
    try:
        from src.gui.main_window import ModernMainWindow
        print("✅ Main window import successful")
        return True
    except Exception as e:
        print(f"❌ Main window import failed: {e}")
        return False

def test_legacy_gui():
    """Test legacy GUI import"""
    try:
        from src.gui.advanced_dashboard import AdvancedDashboard
        print("✅ Legacy GUI import successful")
        return True
    except Exception as e:
        print(f"❌ Legacy GUI import failed: {e}")
        return False

def test_onboarding_and_notification():
    """Test onboarding dialog and notification system in ModernMainWindow"""
    from src.gui.main_window import ModernMainWindow
    from PySide6.QtWidgets import QApplication
    import sys
    app = QApplication.instance() or QApplication(sys.argv)
    win = ModernMainWindow()
    # Simulate first run
    win.settings.setValue("first_run", True)
    win.show_onboarding_if_needed()
    assert win.settings.value("first_run", False, type=bool) is False
    # Test notification
    try:
        win.show_notification("Test Title", "Test message")
    except Exception as e:
        assert False, f"Notification system failed: {e}"
    print("Onboarding and notification system tested successfully.")
    return True

def test_advanced_dashboard_features():
    """Test advanced dashboard features with charts and analytics"""
    from src.gui.main_window import ModernMainWindow
    from PySide6.QtWidgets import QApplication
    import sys
    
    app = QApplication.instance() or QApplication(sys.argv)
    win = ModernMainWindow()
    
    # Test dashboard components
    assert hasattr(win, 'streak_card'), "Streak card not found"
    assert hasattr(win, 'blocked_card'), "Blocked card not found"
    assert hasattr(win, 'recovery_card'), "Recovery card not found"
    assert hasattr(win, 'risk_card'), "Risk card not found"
    assert hasattr(win, 'streak_chart'), "Streak chart not found"
    assert hasattr(win, 'activity_chart'), "Activity chart not found"
    assert hasattr(win, 'activity_list'), "Activity list not found"
    
    print("✅ Advanced dashboard features working")
    return True

def test_keyboard_shortcuts():
    """Test keyboard shortcuts and menu system"""
    from src.gui.main_window import ModernMainWindow
    from PySide6.QtWidgets import QApplication
    from PySide6.QtGui import QAction
    import sys
    
    app = QApplication.instance() or QApplication(sys.argv)
    win = ModernMainWindow()
    
    # Test menu actions
    menu_bar = win.menuBar()
    assert menu_bar is not None, "Menu bar not found"
    
    # Test that shortcuts are set
    actions = win.findChildren(QAction)
    shortcuts_found = []
    for action in actions:
        if action.shortcut():
            shortcuts_found.append(action.shortcut().toString())
    
    expected_shortcuts = ['Ctrl+N', 'Ctrl+E', 'Ctrl+Q', 'Ctrl+1', 'Ctrl+2', 'Ctrl+3', 'Ctrl+4', 'Ctrl+5']
    for shortcut in expected_shortcuts:
        assert any(shortcut in s for s in shortcuts_found), f"Shortcut {shortcut} not found"
    
    print("✅ Keyboard shortcuts working")
    return True

def test_contextual_help():
    """Test contextual help system"""
    from src.gui.main_window import ModernMainWindow
    from PySide6.QtWidgets import QApplication
    import sys
    
    app = QApplication.instance() or QApplication(sys.argv)
    win = ModernMainWindow()
    
    # Test help system
    assert hasattr(win, 'help_buttons'), "Help buttons not initialized"
    assert hasattr(win, '_show_recovery_help'), "Recovery help method not found"
    assert hasattr(win, '_show_blocking_help'), "Blocking help method not found"
    assert hasattr(win, '_show_analytics_help'), "Analytics help method not found"
    
    # Test tooltips
    assert win.tab_widget.toolTip(), "Tab widget tooltip not set"
    
    print("✅ Contextual help system working")
    return True

def test_export_functionality():
    """Test data export functionality"""
    from src.gui.main_window import ModernMainWindow
    from PySide6.QtWidgets import QApplication
    import sys
    
    app = QApplication.instance() or QApplication(sys.argv)
    win = ModernMainWindow()
    
    # Test export method exists
    assert hasattr(win, '_export_data'), "Export data method not found"
    
    print("✅ Export functionality available")
    return True

def main():
    """Main test function"""
    print("🚀 Phase 3 GUI Test Suite")
    print("=" * 40)
    
    tests = [
        ("PySide6 Availability", test_pyside6_availability),
        ("Theme System", test_theme_system),
        ("GUI Launcher", test_gui_launcher),
        ("Main Window Import", test_main_window_import),
        ("Legacy GUI Import", test_legacy_gui),
        ("Onboarding and Notification", test_onboarding_and_notification),
        ("Advanced Dashboard Features", test_advanced_dashboard_features),
        ("Keyboard Shortcuts", test_keyboard_shortcuts),
        ("Contextual Help", test_contextual_help),
        ("Export Functionality", test_export_functionality),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 Testing: {test_name}")
        print("-" * 30)
        
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} PASSED")
            else:
                print(f"❌ {test_name} FAILED")
        except Exception as e:
            print(f"❌ {test_name} ERROR: {e}")
    
    print("\n" + "=" * 40)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Phase 3 GUI is ready.")
        print("\nTo launch the modern GUI:")
        print("   python -m src.gui.launcher")
        print("\nTo install PySide6:")
        print("   pip install PySide6")
    else:
        print("⚠️ Some tests failed. Check the output above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 