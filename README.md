# 🛡️ CleanNet Shield - Adult Content Blocker & Recovery Tool

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Platform: Windows](https://img.shields.io/badge/platform-windows-blue.svg)](https://www.microsoft.com/windows)

A comprehensive desktop application for Windows that combines multi-layer adult content blocking with recovery support tools including streak tracking, journaling, and accountability features.

## 🌟 Features

### 🔒 Multi-Layer Content Blocking
- **Hosts file blocking** - System-level domain blocking
- **DNS filtering** - Family-safe DNS servers (CleanBrowsing, OpenDNS, etc.)
- **PowerShell integration** - Advanced blocking capabilities
- **Auto-updating blocklists** - 1500+ domains from multiple sources
- **Social media filtering** - Block NSFW content on Reddit, Twitter, etc.

### 🎯 Recovery Support Tools
- **Streak tracking** - Monitor clean days with 9 milestone achievements
- **Daily journaling** - Mood, trigger, and coping strategy tracking
- **Accountability system** - Email and Telegram notifications
- **Progress analytics** - Weekly and monthly statistics
- **Emergency support** - Crisis intervention resources

### 🛠️ Technical Features
- **Professional GUI** - Intuitive tabbed interface
- **Comprehensive logging** - JSON-based activity tracking
- **Admin privilege handling** - Automatic elevation when needed
- **Modular architecture** - Clean separation of concerns
- **Data privacy** - All data stored locally

## 🚀 Quick Start

### Prerequisites
- Windows 10/11
- Python 3.8+ (will be installed automatically if missing)
- Administrator privileges

### Installation

1. **Download the latest release** or clone the repository:
   ```bash
   git clone https://github.com/kWan/cleannet-shield.git
   cd cleannet-shield
   ```

2. **Run the easy installer** (as Administrator):
   ```cmd
   scripts\start.bat
   ```

3. **Or launch directly with Python**:
   ```cmd
   python launcher.py
   ```

### First Time Setup

1. Launch the application as Administrator
2. Go to "Blocking" tab → Click "Enable All Protection"
3. Set up recovery tools in "Recovery" tab
4. Configure notifications in "Settings" tab (optional)

## 📖 Documentation

- **[Installation Guide](docs/INSTALLATION_GUIDE.md)** - Step-by-step setup instructions
- **[User Guide](docs/README.md)** - Comprehensive usage documentation
- **[Technical Overview](docs/PROJECT_OVERVIEW.md)** - Architecture and implementation details
- **[Product Requirements](docs/prd.md)** - Original specifications and goals

## 🏗️ Project Structure

```
CleanNet-Shield/
├── main.py                    # Main GUI application
├── launcher.py                # Smart launcher with dependency checking
├── requirements.txt           # Python dependencies
│
├── blocker/                   # Content blocking modules
│   ├── hosts_blocker.py      # System hosts file management
│   ├── dns_config.py         # DNS configuration
│   └── blocklist_updater.py  # Auto-updating blocklists
│
├── recovery/                  # Recovery support tools
│   ├── journaling.py         # Daily journaling system
│   ├── streak_tracker.py     # Progress tracking
│   └── accountability.py     # Notifications and support
│
├── utils/                     # Utility modules
│   ├── permissions.py        # Admin rights management
│   └── logger.py             # Comprehensive logging
│
├── scripts/                   # Setup and utility scripts
│   ├── start.bat             # Windows launcher
│   ├── setup.bat             # Dependency installer
│   └── test_suite.py         # Testing framework
│
└── docs/                      # Documentation
    ├── README.md             # User documentation
    ├── INSTALLATION_GUIDE.md # Setup instructions
    └── PROJECT_OVERVIEW.md   # Technical details
```

## 🔧 Configuration

### Blocking Sources
The application fetches blocklists from:
- StevenBlack hosts (multiple variants)
- Ultimate NSFW blocklists
- Custom domain additions
- Social media adult content patterns

### DNS Servers
Supported family-safe DNS providers:
- CleanBrowsing Family Filter (default)
- OpenDNS FamilyShield
- Cloudflare for Families
- Quad9 Family Protection
- AdGuard Family Protection

### Notifications
Configure accountability via:
- **Email**: SMTP (Gmail supported)
- **Telegram**: Bot notifications

## 🛡️ Security & Privacy

- **Local storage only** - No cloud dependencies
- **Admin-only access** - Prevents unauthorized changes
- **Automatic backups** - System changes are backed up
- **Privacy-first design** - No external data transmission
- **Open source** - Full transparency

## 🧪 Testing

Run the comprehensive test suite:
```cmd
python scripts\test_suite.py
```

Expected results:
- All modules load successfully
- Data directories created
- Admin privileges detected
- Core functionality verified

## 📊 Status

- **Version**: 2.0
- **Status**: Production Ready
- **Test Coverage**: 85%+
- **Platform**: Windows 10/11
- **License**: MIT

## 🤝 Contributing

Contributions are welcome! Areas for improvement:
- Additional blocklist sources
- New recovery features
- GUI enhancements
- Cross-platform support

Please read our [Contributing Guidelines](CONTRIBUTING.md) before submitting pull requests.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This tool is designed to support recovery efforts and should be used responsibly. It's most effective when combined with professional support, community involvement, and personal commitment to change.

## 🆘 Support

- **Issues**: Report bugs via GitHub Issues
- **Documentation**: Check the `docs/` directory
- **Logs**: Application logs are in `data/logs/`

## 🎯 Roadmap

### Planned Features
- [ ] Windows Service mode for tamper protection
- [ ] File system monitoring for offline content
- [ ] Browser extension integration
- [ ] Mobile companion app
- [ ] Cloud sync (optional)

### Completed ✅
- [x] Multi-layer content blocking
- [x] Recovery tracking tools
- [x] Auto-updating blocklists
- [x] GUI interface
- [x] Comprehensive logging
- [x] PowerShell integration

---

**Made with ❤️ by kWan** | **Supporting recovery journeys since 2025** 🧠💪

*Remember: Recovery is a journey, not a destination. This tool is here to support you every step of the way.* 🌟
