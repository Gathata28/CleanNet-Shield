# CleanNet Shield – Product Requirements Document (PRD) v2

## 📄 Overview

**Product Name**: CleanNet Shield
**Type**: Desktop application (Windows)
**Owner**: kWan
**Platform**: Windows 11+
**Development Tool**: VS Code Agent
**Languages**: Python, PowerShell (optional: JavaScript for GUI)

---d

## 🧽 Purpose

CleanNet Shield is a personal and public-use tool that blocks adult content (pornographic sites, NSFW social media pages, and search triggers). It includes recovery features such as streak tracking, journaling, and accountability logging to help users quit porn permanently. The updated version also focuses on security hardening, tamper prevention, self-reflection analytics, and optional community integrations.

---

## 🌟 Goals & Success Criteria

| Goal                       | Description                              | Success Criteria                      |
| -------------------------- | ---------------------------------------- | ------------------------------------- |
| Block all known porn sites | Prevent access to adult domains          | 95%+ block success rate               |
| Block social media NSFW    | Block hashtags, pages, or usernames      | Full block or redirect functionality  |
| Track recovery streaks     | Show user clean days and history         | Visual clean counter + reset logic    |
| Auto-update blocklists     | Sync from trusted public sources         | Weekly updates without duplicates     |
| Protect app from tampering | Prevent uninstall or file edits          | Admin lock, run as service, watchdog  |
| Easy install and use       | Setup in a few minutes                   | CLI or GUI installer                  |
| Block offline content      | Warn about suspicious files in downloads | Flag or delete common porn file types |
| Community support          | Optional partner or bot alerts           | Telegram/email reports enabled        |
| Data backup                | Prevent log/config loss                  | Auto-backup + optional cloud sync     |

---

## 🧱 Key Features

### 🔒 Blocking Engine

* Hosts file injection
* DNS reconfiguration (CleanBrowsing, OpenDNS)
* Manual blocklist management
* Browser monitor or killer (optional)
* Tamper-proof mode (Windows service + reapply protection)

### 🧠 Recovery Tools

* Streak counter and history
* Daily journaling/logging
* Relapse reset tracking
* Accountability logging/report sharing (via Telegram or email)
* Self-reflection analytics (e.g., heatmaps, urge patterns)

### ♻️ Auto-Update System

* Fetches new domains from public blocklist sources
* Avoids duplicates
* Scheduled weekly updates

### 🖥️ Optional GUI

* Streak dashboard
* Journal input window
* Blocklist editor
* Settings + Lock mode

### ⚡ Offline File Monitoring (Optional)

* Warn user about suspicious file types in known download folders
* List/delete unwanted media content

---

## 🛠️ Technical Stack

| Component       | Tool / Language        |
| --------------- | ---------------------- |
| Core logic      | Python                 |
| System access   | PowerShell scripts     |
| GUI (optional)  | Tkinter or Electron.js |
| Logging         | JSON or SQLite         |
| Scheduling      | Windows Task Scheduler |
| Notification    | SMTP, Telegram API     |
| File Monitoring | Python + watchdog      |

---

## 📁 Project Structure

```
CleanNetShield/
├── main.py
├── config/
│   └── blocklist.txt
│   └── settings.json
├── blocker/
│   ├── hosts_blocker.py
│   ├── dns_setter.py
│   ├── browser_guard.py
│   ├── watchdog_service.py
│   └── blocklist_updater.py
├── recovery/
│   ├── streak.py
│   ├── journal.py
│   ├── analytics.py
│   └── accountability.py
├── utils/
│   ├── permissions.py
│   ├── logger.py
│   └── backup.py
├── monitor/
│   └── file_scanner.py
├── logs/
│   ├── usage.json
│   └── relapses.json
└── gui/
    └── app_window.py (optional)
```

---

## 🔮 Testing Plan

| Component         | Test Scenario                               |
| ----------------- | ------------------------------------------- |
| Domain blocking   | Attempt to access known porn site           |
| Hosts editing     | Check hosts file for entries                |
| DNS setting       | Validate DNS change via `ipconfig`          |
| Journal logging   | Add an entry and verify content + date      |
| Streak tracker    | Confirm counter resets and increments       |
| Auto-updater      | Verify new domains get added weekly         |
| File scanner      | Detect flagged file types in download dir   |
| Lock system       | Ensure admin rights are required            |
| Tamper resistance | Try disabling program, ensure it relaunches |
| Notification      | Check email/Telegram alerts send correctly  |

---

## 🗓️ Development Timeline

| Week | Milestone                                      |
| ---- | ---------------------------------------------- |
| 1    | Build core blocker: hosts + DNS                |
| 2    | Add journaling, logging, streak tracking       |
| 3    | Implement updater, watchdog, and UI (optional) |
| 4    | Build file scanner + report system             |
| 5    | Final testing, tamper-proofing, and release    |

---

## 🧰 Future Expansion Ideas

| Feature                  | Priority | Description                              |
| ------------------------ | -------- | ---------------------------------------- |
| Cloud sync               | Low      | Save settings and logs in cloud          |
| Mobile companion app     | Medium   | Track streak, journal, and block via app |
| AI-based image detection | Medium   | Use OCR and AI to detect NSFW media      |
| Community blocklist      | Low      | Share/import custom blocklists           |
| Emergency lockdown mode  | Medium   | Disable all internet temporarily         |

---

## 🧑‍💻 User Stories

* As a user, I want to block all known porn sites so I can focus.
* As someone recovering from addiction, I want to track my clean streak.
* As a user, I want to log my thoughts daily to stay accountable.
* As an accountability partner, I want reports on any relapses or violations.
* As a parent, I want to lock the program so it can't be uninstalled.
* As a dev, I want to back up my data in case of crash.
* As a clean user, I want to see analytics to know when I'm most vulnerable.

---

## 🧰 Dependencies

| Library/Tool    | Use                          |
| --------------- | ---------------------------- |
| requests        | Fetch external blocklists    |
| subprocess      | Run PowerShell commands      |
| ctypes          | Check admin privileges       |
| json, os        | Logging and config parsing   |
| Tkinter         | Optional desktop GUI         |
| psutil          | Monitor browser activity     |
| watchdog        | Monitor file system for porn |
| smtplib         | Email notifications          |
| telebot/aiogram | Telegram bot reporting       |

---

## 📌 Blocklist Sources

* [StevenBlack hosts](https://github.com/StevenBlack/hosts)
* [Blocklist.site](https://blocklist.site/app/)
* Manually added keywords, social links

---

## 🚨 Notes

* The tool should be open-source and usable by non-coders.
* Must be difficult to bypass without real admin intervention.
* All logs should be private and securely stored locally unless the user chooses to export.
* Data loss should be prevented with local and optional cloud backup.

---

**Made by kWan** 🧠💪
