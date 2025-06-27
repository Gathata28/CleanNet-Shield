# CleanNet Shield - Project Structure

## Directory Structure

```
CleanNet Shield/
├── blocker/                 # Content blocking functionality
│   ├── __init__.py
│   ├── blocklist_updater.py # Updates blocklists from sources
│   ├── dns_config.py        # DNS filtering configuration
│   └── hosts_blocker.py     # Hosts file editing functionality
├── config/                  # Configuration files
│   └── blocker_config.json  # Main configuration file
├── data/                    # Data storage
│   ├── accountability/      # Accountability data
│   ├── blocklist_cache.json # Cached blocklist data
│   ├── blocklist.txt        # Active blocklist domains
│   ├── journal/             # Journal entries
│   ├── logs/                # Application logs
│   ├── streaks/             # Streak tracking data
│   └── updater_config.json  # Blocklist updater configuration
├── docs/                    # Documentation
│   ├── CLEANUP_SUMMARY.md
│   ├── INSTALLATION_GUIDE.md
│   ├── prd.md               # Product Requirements Document
│   ├── PROJECT_OVERVIEW.md
│   ├── PROJECT_STRUCTURE.md # This file
│   ├── README.md
│   └── TEST_RESULTS.md
├── recovery/                # Recovery support tools
│   ├── __init__.py
│   ├── accountability.py    # Accountability system
│   ├── journaling.py        # Journaling functionality
│   └── streak_tracker.py    # Streak tracking system
├── scripts/                 # Helper scripts
├── utils/                   # Utility functions
│   ├── __init__.py
│   ├── logger.py            # Logging functionality
│   └── permissions.py       # Admin permission handling
├── .gitignore               # Git ignore configuration
├── CONTRIBUTING.md          # Contribution guidelines
├── final_check.py           # Final deployment check script
├── gui_simple_modern.py     # Modern GUI implementation
├── launcher.py              # Application launcher
├── LICENSE                  # Software license (MIT)
├── main.py                  # Main application entry point
├── README.md                # Project overview
├── RELEASE_NOTES.md         # Release notes
├── requirements.txt         # Python dependencies
├── setup.py                 # Installation script
├── SIMPLE_PERSONAL_PLAN.md  # Personal app plan
├── validate_deployment.py   # Detailed validation script
└── VALIDATION_REPORT.json   # Validation results
```

## Main Components

### 1. Core Application Files
- `main.py` - Main application with the comprehensive GUI
- `launcher.py` - Bootstrap script that handles initial setup
- `gui_simple_modern.py` - Modern user interface implementation

### 2. Blocking Components (`blocker/`)
- `hosts_blocker.py` - System hosts file configuration for domain blocking
- `dns_config.py` - DNS server configuration for filtered internet
- `blocklist_updater.py` - Updates blocklists from various sources

### 3. Recovery Tools (`recovery/`)
- `streak_tracker.py` - Tracks daily streaks and achievements
- `journaling.py` - Daily journaling system
- `accountability.py` - External accountability notifications

### 4. Utilities (`utils/`)
- `logger.py` - Logging system with rotation and formatting
- `permissions.py` - Admin privilege detection and elevation

### 5. Data Storage (`data/`)
- Configuration files and cached blocklists
- User data (journals, streaks, logs, accountability)

### 6. Documentation (`docs/`)
- Installation guides
- Project overview
- Product requirements document

### 7. Scripts
- Installation and setup scripts
- Administrative execution helpers
