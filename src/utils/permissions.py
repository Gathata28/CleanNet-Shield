#!/usr/bin/env python3
"""
Permissions utility module for checking and requesting admin rights
"""

import ctypes
import sys
import os

def check_admin_rights():
    """
    Check if the current process has administrator privileges
    Returns True if running as admin, False otherwise
    """
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def request_admin_rights():
    """
    Request administrator privileges by restarting the script with elevated rights
    """
    if check_admin_rights():
        return True
    
    try:
        # Re-run the program with admin rights
        ctypes.windll.shell32.ShellExecuteW(
            None,
            "runas",
            sys.executable,
            " ".join(sys.argv),
            None,
            1
        )
        return True
    except Exception as e:
        print(f"Failed to request admin rights: {e}")
        return False

def ensure_admin_rights():
    """
    Ensure admin rights, exit if not available
    """
    if not check_admin_rights():
        print("Administrator privileges required!")
        if request_admin_rights():
            sys.exit(0)  # Original process exits, new admin process starts
        else:
            print("Failed to obtain administrator privileges. Exiting.")
            sys.exit(1)

def can_modify_hosts():
    """
    Check if we can modify the hosts file
    """
    hosts_path = os.path.join(os.environ.get('WINDIR', 'C:\\Windows'), 'System32', 'drivers', 'etc', 'hosts')
    try:
        # Try to open hosts file for writing
        with open(hosts_path, 'a') as f:
            pass
        return True
    except PermissionError:
        return False
    except Exception:
        return False

def can_modify_dns():
    """
    Check if we can modify DNS settings (requires admin)
    """
    return check_admin_rights()

if __name__ == "__main__":
    print(f"Running as admin: {check_admin_rights()}")
    print(f"Can modify hosts: {can_modify_hosts()}")
    print(f"Can modify DNS: {can_modify_dns()}")
