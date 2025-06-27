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
- Windows 10/11
- Python 3.8+ (optional if using executable)
- Administrator privileges

### Quick Start
1. **Download/Clone** the repository
2. **Run as Administrator**: Right-click and "Run as administrator"
3. **Execute**: `python main.py` or use the compiled executable

### Python Setup (Developer)
```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
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

## Module Structure

```
AdultBlockerApp/
├── main.py                    # Main application and GUI
├── blocker/                   # Content blocking modules
│   ├── hosts_blocker.py      # Hosts file management
│   ├── dns_config.py         # DNS configuration
│   └── blocklist_updater.py  # Blocklist fetching/updating
├── recovery/                  # Recovery support modules
│   ├── journaling.py         # Daily journaling system
│   ├── streak_tracker.py     # Progress tracking
│   └── accountability.py     # Notifications and support
├── utils/                     # Utility modules
│   ├── permissions.py        # Admin rights management
│   └── logger.py             # Comprehensive logging
└── data/                      # Data storage
    ├── logs/                 # Application logs
    ├── journal/              # Journal entries
    ├── streaks/              # Streak tracking data
    └── accountability/       # Notification settings
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

### Streak Tracking
- Track consecutive clean days
- Milestone achievements (1, 3, 7, 14, 30, 90, 365 days)
- Progress visualization
- Automatic streak validation

### Journaling System
- Daily mood and trigger tracking
- Coping strategy recording
- Search and export functionality
- Monthly summaries and insights

### Accountability
- Daily check-in reminders
- Weekly progress reports
- Emergency support messages
- Motivation and encouragement

## Security & Privacy

- **Local storage**: All data stored locally
- **No cloud sync**: Complete privacy
- **Encrypted logs**: Sensitive information protected
- **Admin-only access**: Prevents tampering

## Troubleshooting

### Common Issues

**"Access Denied" errors:**
- Ensure running as administrator
- Check Windows UAC settings
- Verify hosts file permissions

**DNS not changing:**
- Restart network adapter
- Flush DNS cache: `ipconfig /flushdns`
- Check Windows network settings

**PowerShell errors:**
- Verify execution policy: `Get-ExecutionPolicy`
- Run: `Set-ExecutionPolicy RemoteSigned`
- Check PowerShell script path

**Blocklist not updating:**
- Check internet connection
- Verify firewall settings
- Review application logs

### Logs Location
- **Application logs**: `data/logs/`
- **Journal data**: `data/journal/`
- **Streak data**: `data/streaks/`
- **Configuration**: `data/*/config.json`

## Development

### Adding New Blocklist Sources
Edit `blocker/blocklist_updater.py`:
```python
"sources": [
    {
        "name": "New Source",
        "url": "https://example.com/blocklist.txt",
        "format": "hosts",  # or "domains"
        "enabled": True
    }
]
```

### Custom Recovery Features
Extend `recovery/` modules:
- Add new tracking metrics
- Implement custom notifications
- Create additional analysis tools

### GUI Modifications
Edit `main.py` to:
- Add new tabs
- Modify existing interfaces
- Integrate new features

## Building Executable

To create a standalone executable:

```bash
# Install PyInstaller
pip install pyinstaller

# Build executable
pyinstaller --onefile --windowed --icon=icon.ico main.py

# Output: dist/main.exe
```

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review application logs
3. Verify administrator privileges
4. Check PowerShell integration

## License

This project is for personal use and recovery support. Use responsibly and ensure compliance with local laws and regulations.

## Contributing

Contributions welcome! Focus areas:
- Additional blocklist sources
- New recovery features
- GUI improvements
- Cross-platform support

---

**Remember**: This tool is designed to support your recovery journey. It's most effective when combined with professional support, community involvement, and personal commitment to change.
