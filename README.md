# Adult Content Blocker & Recovery Tool

A comprehensive desktop application for Windows that combines content blocking with recovery support tools.

## Features

### 🛡️ Content Blocking
- **Multi-layer protection**: Hosts file, DNS, and PowerShell integration
- **Auto-updating blocklists**: Fetches from multiple sources
- **1500+ domains**: Comprehensive coverage including social media adult content
- **Family-safe DNS**: Automatic configuration of filtering DNS servers

### 🎯 Recovery Tools
- **Streak tracking**: Monitor clean days with achievements and milestones
- **Daily journaling**: Track mood, triggers, and coping strategies
- **Accountability system**: Email and Telegram notifications
- **Progress monitoring**: Weekly and monthly statistics

### 🔧 Technical Features
- **Modular architecture**: Clean separation of concerns
- **Comprehensive logging**: Track all actions and errors
- **PowerShell integration**: Leverages existing ultimate blocker script
- **Admin privilege handling**: Automatic elevation when needed

## Installation

### Prerequisites
- Windows 10/11, MacOS, or Linux
- Python 3.8+ (optional if using executable)
- Administrator privileges

### Quick Start

1. **Download/Clone** the repository
2. **Run as Administrator**: Right-click and "Run as administrator"
3. **Execute**:
   - `python main.py` (recommended)
   - Or: `python src/main.py`
   - Or: `python -m src.gui.launcher`

### Python Setup (Developer)
```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
default: python main.py
```

## Usage

### First Time Setup
1. **Launch** the application as administrator
2. **Configure** blocking in the "Blocking" tab
3. **Set up** recovery tools in the "Recovery" tab
4. **Configure** notifications in the "Settings" tab

### Daily Use
1. **Check status** in the "Status" tab
2. **Mark clean days** in the "Recovery" tab
3. **Write journal entries** for reflection
4. **Update blocklists** as needed

## Running Tests

To run the full test suite:
```bash
python main.py --test
```
Or:
```bash
python test_phase3_gui.py
```

## Module Structure
```
AdultBlockerApp/
├── main.py                    # Main application and GUI entry point
├── src/
│   ├── main.py                # (Secondary entry point for devs)
│   ├── launcher.py            # (Secondary launcher for devs)
│   └── gui/
│       ├── launcher.py        # GUI launcher logic
│       └── main_window.py     # Main GUI window
├── blocker/                   # Content blocking modules
├── recovery/                  # Recovery support modules
├── utils/                     # Utility modules
├── data/                      # Data storage
```

## Configuration

### Blocking Sources
The application fetches blocklists from:
- StevenBlack hosts (multiple variants)
- Ultimate NSFW blocklists
- Custom domain additions
- Social media adult content patterns

### DNS Servers
Family-safe DNS options:
- **CleanBrowsing Family Filter** (default)
- **OpenDNS FamilyShield**
- **Cloudflare for Families**
- **Quad9 Family Protection**
- **AdGuard Family Protection**

### Notifications
Set up accountability notifications via:
- **Email**: SMTP configuration (Gmail supported)
- **Telegram**: Bot token and chat ID setup

## PowerShell Integration
The application integrates with the existing PowerShell ultimate blocker:
- Calls `SuperUltimateContentBlocker_AutoUpdate.ps1`
- Provides GUI interface for PowerShell features
- Combines Python flexibility with PowerShell system access

## Recovery Features
(see above)
