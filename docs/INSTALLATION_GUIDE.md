# 🚀 INSTALLATION GUIDE - Adult Content Blocker & Recovery Tool

## 📋 **PREREQUISITES**

Your system needs the following components installed:

### ✅ **STEP 1: Install Python**

```powershell
# Using winget (recommended)
winget install Python.Python.3.12

# OR download from python.org
# Make sure to check "Add Python to PATH" during installation
```

### ✅ **STEP 2: Install Required Python Packages**

```powershell
# Install requests library (only required dependency)
pip install requests

# Optional: Install all dependencies from requirements.txt
pip install -r requirements.txt
```

### ✅ **STEP 3: Verify Installation**

```powershell
# Test Python installation
python --version

# Test package installation
python -c "import requests; print('✅ Dependencies OK')"
```

---

## 🛠️ **INSTALLATION METHODS**

### **METHOD 1: Easy Launch (Recommended)**

1. **Double-click** `scripts\start.bat`
2. Follow the prompts
3. Application will check dependencies and launch

### **METHOD 2: Automated Setup**

```powershell
# Navigate to application directory
cd C:\Users\HomePC\ContentBlocker\AdultBlockerApp

# Run automated setup
scripts\setup.bat
```

### **METHOD 3: Python Direct**

```powershell
# Navigate to application directory
cd C:\Users\HomePC\ContentBlocker\AdultBlockerApp

# Launch the application
python launcher.py
```

### **METHOD 3: Test First, Then Launch**

```powershell
# Run comprehensive tests
python test_suite.py

# If tests pass, launch GUI
python main.py
```

---

## 🔧 **TROUBLESHOOTING**

### **Python Not Found**

```powershell
# Check if Python is in PATH
where python

# If not found, try
where python3

# Or add Python to PATH manually
# Add C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python312\ to PATH
```

### **Permission Errors**

```powershell
# Run PowerShell as Administrator
# Right-click PowerShell → "Run as administrator"

# Or check execution policy
Get-ExecutionPolicy
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### **Missing Dependencies**

```powershell
# Force reinstall packages
pip install --force-reinstall requests

# Or upgrade pip first
python -m pip install --upgrade pip
```

---

## 🎯 **POST-INSTALLATION VERIFICATION**

### **Quick Test Commands:**

```powershell
# Test 1: Check modules load
python -c "import sys; sys.path.append('.'); import utils.logger; print('✅ Modules OK')"

# Test 2: Check admin status
python -c "import sys; sys.path.append('.'); from utils.permissions import check_admin_rights; print(f'Admin: {check_admin_rights()}')"

# Test 3: Run full test suite
python test_suite.py
```

### **Expected Output:**

- ✅ All modules imported successfully
- ✅ Objects created without errors
- ✅ Data directories created
- ✅ Admin privileges detected (if running as admin)

---

## 🚀 **FIRST-TIME SETUP**

After successful installation:

1. **Launch as Administrator:**
   - Right-click `start.bat` → "Run as administrator"
   - Or: Right-click PowerShell → "Run as administrator" → `python main.py`

2. **Configure Blocking:**
   - Go to "Blocking" tab
   - Click "Enable All Protection"
   - Update blocklist as needed

3. **Set Up Recovery Tools:**
   - Go to "Recovery" tab
   - Mark your first clean day
   - Write a journal entry

4. **Configure Notifications (Optional):**
   - Go to "Settings" tab
   - Set up email or Telegram notifications
   - Configure DNS settings

---

## 📦 **WHAT GETS INSTALLED**

### **Application Files:**

- `main.py` - Main GUI application
- `launcher.py` - Smart launcher with dependency checking
- `test_suite.py` - Comprehensive testing
- `start.bat` - Windows batch launcher

### **Core Modules:**

- `blocker/` - Content blocking system
- `recovery/` - Recovery support tools
- `utils/` - Utility functions

### **Data Directories:**

- `data/logs/` - Application logs
- `data/journal/` - Journal entries
- `data/streaks/` - Streak tracking
- `data/accountability/` - Notification settings

---

## 🛡️ **SECURITY NOTES**

- **Admin privileges required** for hosts file modification
- **Local data only** - no cloud sync
- **Automatic backups** before system changes
- **Privacy-first design** - no external data transmission

---

## 📞 **NEED HELP?**

If you encounter issues:

1. **Check the logs:** `data/logs/blocker_*.log`
2. **Run diagnostics:** `python test_suite.py`
3. **Verify admin rights:** Run as administrator
4. **Check Python version:** `python --version` (need 3.8+)

---

## 🎉 **YOU'RE READY!**

Once Python is installed and the tests pass, your comprehensive Adult Content Blocker & Recovery Tool will be fully operational on Windows!

**Commands to run after Python installation:**

```powershell
cd C:\Users\HomePC\ContentBlocker\AdultBlockerApp
python test_suite.py
python launcher.py
```

## Quick Start

1. **Clone or download** the repository
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the application**:
   ```bash
   python main.py
   ```
   - This will launch the GUI by default.
   - To run tests: `python main.py --test`

## Developer Usage
- You can also run from the src directory for development:
  ```bash
  python src/main.py
  ```
- Or launch the GUI directly:
  ```bash
  python -m src.gui.launcher
  ```

## Notes
- Always run as administrator for full functionality.
- The main entry point is now `main.py` at the project root.
- Old/empty entry points in src/ are no longer used.

## Troubleshooting
- If you see import errors, ensure you are running from the project root and have installed all dependencies.
- For advanced usage, see the README.md.
