#!/usr/bin/env python3
"""
COMPREHENSIVE ADULT CONTENT BLOCKER & RECOVERY TOOL
Main application launcher with GUI and recovery features
"""

import sys
import os
import tkinter as tk
from tkinter import ttk, messagebox
import threading
import json
from datetime import datetime
import subprocess

# Add project modules to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Handle imports for both standalone and package usage
try:
    from blocker.hosts_blocker import HostsBlocker
    from blocker.dns_config import DNSConfig
    from blocker.blocklist_updater import BlocklistUpdater
    from recovery.journaling import Journal
    from recovery.streak_tracker import StreakTracker
    from recovery.accountability import AccountabilityBot
    from utils.permissions import check_admin_rights
    from utils.logger import Logger
except ImportError as e:
    print(f"Import error: {e}")
    print("Please ensure all modules are in the correct location.")
    sys.exit(1)

# --- Centralized admin check using permissions utility ---
def ensure_admin_rights():
    try:
        from utils.permissions import ensure_admin_rights
        ensure_admin_rights()
    except ImportError:
        # Fallback: manual check
        import ctypes
        if not (ctypes.windll.shell32.IsUserAnAdmin()):
            print("Administrator privileges required! Relaunching as administrator...")
            params = ' '.join(['"{}"'.format(arg) for arg in sys.argv])
            ctypes.windll.shell32.ShellExecuteW(
                None, "runas", sys.executable, params, None, 1)
            sys.exit(0)

ensure_admin_rights()

class AdultBlockerApp:
    def __init__(self):
        self.logger = Logger()
        self.hosts_blocker = HostsBlocker()
        self.dns_config = DNSConfig()
        self.blocklist_updater = BlocklistUpdater()
        self.journal = Journal()
        self.streak_tracker = StreakTracker()
        self.accountability = AccountabilityBot()
        
        self.setup_gui()
        
        # Add modern theme to existing GUI (optional enhancement)
        try:
            from gui_simple_modern import add_modern_features_to_existing_app
            add_modern_features_to_existing_app(self.root, "CleanNet Shield")
        except ImportError:
            print("Modern theme not available - your app works fine without it!")
        
        self.logger.log("Application started")
    
    def setup_gui(self):
        """Setup the main GUI window"""
        self.root = tk.Tk()
        self.root.title("Adult Content Blocker & Recovery Tool")
        self.root.geometry("800x600")
        self.root.configure(bg='#2c3e50')
        
        # Style configuration
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'), background='#2c3e50', foreground='white')
        style.configure('Header.TLabel', font=('Arial', 12, 'bold'), background='#2c3e50', foreground='white')
        
        # Main title
        title_label = ttk.Label(self.root, text="🛡️ Adult Content Blocker & Recovery Tool", 
                               style='Title.TLabel')
        title_label.pack(pady=20)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Create tabs
        self.create_blocking_tab()
        self.create_recovery_tab()
        self.create_settings_tab()
        self.create_status_tab()
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Update status on startup
        self.update_status()
    
    def create_blocking_tab(self):
        """Create the blocking management tab"""
        blocking_frame = ttk.Frame(self.notebook)
        self.notebook.add(blocking_frame, text="Blocking")
        
        # Blocking controls
        ttk.Label(blocking_frame, text="Website Blocking Controls", style='Header.TLabel').pack(pady=10)
        
        btn_frame = ttk.Frame(blocking_frame)
        btn_frame.pack(pady=10)
        
        ttk.Button(btn_frame, text="🔒 Enable All Protection", 
                  command=self.enable_protection, width=25).pack(pady=5)
        ttk.Button(btn_frame, text="🔄 Update Blocklist", 
                  command=self.update_blocklist, width=25).pack(pady=5)
        ttk.Button(btn_frame, text="🛡️ Run PowerShell Ultimate Blocker", 
                  command=self.run_powershell_blocker, width=25).pack(pady=5)
        ttk.Button(btn_frame, text="❌ Disable Protection", 
                  command=self.disable_protection, width=25).pack(pady=5)
        
        # Blocklist info
        info_frame = ttk.LabelFrame(blocking_frame, text="Blocklist Information")
        info_frame.pack(fill='x', padx=20, pady=10)
        
        self.blocklist_info = tk.Text(info_frame, height=10, width=70)
        scrollbar = ttk.Scrollbar(info_frame, orient='vertical', command=self.blocklist_info.yview)
        self.blocklist_info.configure(yscrollcommand=scrollbar.set)
        
        self.blocklist_info.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
    
    def create_recovery_tab(self):
        """Create the recovery tools tab"""
        recovery_frame = ttk.Frame(self.notebook)
        self.notebook.add(recovery_frame, text="Recovery")
        
        ttk.Label(recovery_frame, text="Recovery & Self-Monitoring Tools", style='Header.TLabel').pack(pady=10)
        
        # Streak tracker
        streak_frame = ttk.LabelFrame(recovery_frame, text="Streak Tracker")
        streak_frame.pack(fill='x', padx=20, pady=10)
        
        self.streak_label = ttk.Label(streak_frame, text="", font=('Arial', 14, 'bold'))
        self.streak_label.pack(pady=10)
        
        streak_btn_frame = ttk.Frame(streak_frame)
        streak_btn_frame.pack(pady=5)
        
        ttk.Button(streak_btn_frame, text="✅ Mark Clean Day", 
                  command=self.mark_clean_day).pack(side='left', padx=5)
        ttk.Button(streak_btn_frame, text="❌ Reset Streak", 
                  command=self.reset_streak).pack(side='left', padx=5)
        
        # Journal
        journal_frame = ttk.LabelFrame(recovery_frame, text="Daily Journal")
        journal_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        ttk.Label(journal_frame, text="How are you feeling today?").pack(pady=5)
        
        self.journal_text = tk.Text(journal_frame, height=8, width=70)
        journal_scrollbar = ttk.Scrollbar(journal_frame, orient='vertical', command=self.journal_text.yview)
        self.journal_text.configure(yscrollcommand=journal_scrollbar.set)
        
        self.journal_text.pack(side='left', fill='both', expand=True)
        journal_scrollbar.pack(side='right', fill='y')
        
        ttk.Button(journal_frame, text="💾 Save Journal Entry", 
                  command=self.save_journal_entry).pack(pady=10)
        
        # Load today's journal entry if exists
        self.load_todays_journal()
    
    def create_settings_tab(self):
        """Create the settings tab"""
        settings_frame = ttk.Frame(self.notebook)
        self.notebook.add(settings_frame, text="Settings")
        
        ttk.Label(settings_frame, text="Application Settings", style='Header.TLabel').pack(pady=10)
        
        # DNS Settings
        dns_frame = ttk.LabelFrame(settings_frame, text="DNS Configuration")
        dns_frame.pack(fill='x', padx=20, pady=10)
        
        ttk.Label(dns_frame, text="Family-Safe DNS Servers:").pack(anchor='w', padx=10, pady=5)
        
        self.dns_var = tk.StringVar(value="CleanBrowsing")
        dns_options = ["CleanBrowsing", "OpenDNS Family", "Cloudflare for Families", "Custom"]
        ttk.OptionMenu(dns_frame, self.dns_var, *dns_options).pack(padx=10, pady=5)
        
        ttk.Button(dns_frame, text="Apply DNS Settings", 
                  command=self.apply_dns_settings).pack(padx=10, pady=10)
        
        # Accountability Settings
        account_frame = ttk.LabelFrame(settings_frame, text="Accountability Partner")
        account_frame.pack(fill='x', padx=20, pady=10)
        
        ttk.Label(account_frame, text="Email for notifications:").pack(anchor='w', padx=10, pady=5)
        self.email_var = tk.StringVar()
        ttk.Entry(account_frame, textvariable=self.email_var, width=40).pack(padx=10, pady=5)
        
        ttk.Button(account_frame, text="Test Email", 
                  command=self.test_accountability_email).pack(padx=10, pady=10)
    
    def create_status_tab(self):
        """Create the status monitoring tab"""
        status_frame = ttk.Frame(self.notebook)
        self.notebook.add(status_frame, text="Status")
        
        ttk.Label(status_frame, text="Protection Status", style='Header.TLabel').pack(pady=10)
        
        # Status display
        self.status_text = tk.Text(status_frame, height=20, width=80, font=('Consolas', 10))
        status_scrollbar = ttk.Scrollbar(status_frame, orient='vertical', command=self.status_text.yview)
        self.status_text.configure(yscrollcommand=status_scrollbar.set)
        
        self.status_text.pack(side='left', fill='both', expand=True, padx=20, pady=10)
        status_scrollbar.pack(side='right', fill='y')
        
        ttk.Button(status_frame, text="🔄 Refresh Status", 
                  command=self.update_status).pack(pady=10)
    
    def enable_protection(self):
        """Enable all protection measures"""
        def run_protection():
            try:
                self.status_var.set("Enabling protection...")
                
                # Update blocklist first
                self.blocklist_updater.update_from_sources()
                
                # Apply hosts blocking
                domains = self.blocklist_updater.get_domains()
                self.hosts_blocker.block_domains(domains)
                
                # Set family-safe DNS
                self.dns_config.set_family_safe_dns()
                
                # Log the action
                self.logger.log("Protection enabled", {"domains_count": len(domains)})
                
                self.status_var.set("Protection enabled successfully!")
                messagebox.showinfo("Success", f"Protection enabled with {len(domains)} blocked domains!")
                
                self.update_status()
                
            except Exception as e:
                self.logger.log("Failed to enable protection", {"error": str(e)})
                self.status_var.set("Failed to enable protection")
                messagebox.showerror("Error", f"Failed to enable protection: {str(e)}")
        
        # Run in background thread
        threading.Thread(target=run_protection, daemon=True).start()
    
    def update_blocklist(self):
        """Update the blocklist from external sources"""
        def run_update():
            try:
                self.status_var.set("Updating blocklist...")
                result = self.blocklist_updater.update_from_sources()
                
                if result:
                    self.status_var.set(f"Blocklist updated with {len(result)} domains")
                    self.update_blocklist_display()
                else:
                    self.status_var.set("Failed to update blocklist")
                    
            except Exception as e:
                self.status_var.set("Blocklist update failed")
                messagebox.showerror("Error", f"Failed to update blocklist: {str(e)}")
        
        threading.Thread(target=run_update, daemon=True).start()
    
    def run_powershell_blocker(self):
        """Run the existing PowerShell ultimate blocker"""
        try:
            ps_script = os.path.join(os.path.dirname(os.path.dirname(__file__)), 
                                   "SuperUltimateContentBlocker_AutoUpdate.ps1")
            
            if os.path.exists(ps_script):
                self.status_var.set("Running PowerShell blocker...")
                
                # Run PowerShell script with install option
                cmd = f'powershell.exe -ExecutionPolicy Bypass -File "{ps_script}" -Install'
                process = subprocess.Popen(cmd, shell=True, capture_output=True, text=True)
                
                self.status_var.set("PowerShell blocker completed")
                messagebox.showinfo("PowerShell Blocker", "Ultimate blocker executed successfully!")
                
                self.update_status()
            else:
                messagebox.showerror("Error", "PowerShell script not found!")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to run PowerShell blocker: {str(e)}")
    
    def disable_protection(self):
        """Disable all protection measures"""
        if messagebox.askyesno("Confirm", "Are you sure you want to disable protection?"):
            try:
                self.hosts_blocker.remove_blocks()
                self.dns_config.reset_dns()
                self.status_var.set("Protection disabled")
                messagebox.showinfo("Success", "Protection disabled")
                self.update_status()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to disable protection: {str(e)}")
    
    def mark_clean_day(self):
        """Mark today as a clean day"""
        self.streak_tracker.mark_clean_day()
        self.update_streak_display()
        self.logger.log("Clean day marked")
        messagebox.showinfo("Great job!", "Clean day marked! Keep up the good work!")
    
    def reset_streak(self):
        """Reset the streak counter"""
        if messagebox.askyesno("Reset Streak", "Are you sure you want to reset your streak?"):
            self.streak_tracker.reset_streak()
            self.update_streak_display()
            self.logger.log("Streak reset")
            messagebox.showinfo("Streak Reset", "Streak has been reset. Tomorrow is a new day!")
    
    def save_journal_entry(self):
        """Save the current journal entry"""
        entry = self.journal_text.get(1.0, tk.END).strip()
        if entry:
            self.journal.add_entry(entry)
            self.logger.log("Journal entry saved")
            messagebox.showinfo("Saved", "Journal entry saved successfully!")
        else:
            messagebox.showwarning("Empty Entry", "Please write something before saving.")
    
    def load_todays_journal(self):
        """Load today's journal entry if it exists"""
        entry = self.journal.get_todays_entry()
        if entry:
            self.journal_text.delete(1.0, tk.END)
            self.journal_text.insert(1.0, entry)
    
    def apply_dns_settings(self):
        """Apply the selected DNS settings"""
        try:
            dns_type = self.dns_var.get()
            self.dns_config.set_dns_by_type(dns_type)
            self.status_var.set(f"DNS set to {dns_type}")
            messagebox.showinfo("Success", f"DNS configured to {dns_type}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to set DNS: {str(e)}")
    
    def test_accountability_email(self):
        """Test the accountability email"""
        email = self.email_var.get()
        if email:
            try:
                self.accountability.set_email(email)
                self.accountability.send_test_email()
                messagebox.showinfo("Success", "Test email sent successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to send test email: {str(e)}")
        else:
            messagebox.showwarning("No Email", "Please enter an email address first.")
    
    def update_streak_display(self):
        """Update the streak display"""
        streak_days = self.streak_tracker.get_current_streak()
        last_clean = self.streak_tracker.get_last_clean_date()
        
        if streak_days > 0:
            streak_text = f"🔥 Current Streak: {streak_days} days!"
            if last_clean:
                streak_text += f"\nLast clean day: {last_clean.strftime('%Y-%m-%d')}"
        else:
            streak_text = "Start your streak by marking a clean day!"
        
        self.streak_label.config(text=streak_text)
    
    def update_blocklist_display(self):
        """Update the blocklist information display"""
        try:
            domains = self.blocklist_updater.get_domains()
            info = f"Total blocked domains: {len(domains)}\n\n"
            info += "Recent domains:\n"
            for domain in domains[:20]:  # Show first 20
                info += f"• {domain}\n"
            if len(domains) > 20:
                info += f"... and {len(domains) - 20} more"
            
            self.blocklist_info.delete(1.0, tk.END)
            self.blocklist_info.insert(1.0, info)
        except Exception as e:
            self.blocklist_info.delete(1.0, tk.END)
            self.blocklist_info.insert(1.0, f"Error loading blocklist: {str(e)}")
    
    def update_status(self):
        """Update the status display"""
        try:
            status_info = "=== ADULT CONTENT BLOCKER STATUS ===\n\n"
            
            # Check hosts file
            hosts_active = self.hosts_blocker.is_active()
            status_info += f"🛡️ Hosts File Blocking: {'✅ ACTIVE' if hosts_active else '❌ INACTIVE'}\n"
            
            # Check DNS
            dns_info = self.dns_config.get_current_dns()
            status_info += f"🌐 DNS Configuration: {dns_info}\n"
            
            # Check streak
            streak_days = self.streak_tracker.get_current_streak()
            status_info += f"🔥 Current Streak: {streak_days} days\n"
            
            # Check blocklist count
            try:
                domains = self.blocklist_updater.get_domains()
                status_info += f"📋 Blocked Domains: {len(domains)}\n"
            except:
                status_info += "📋 Blocked Domains: Unable to count\n"
            
            # Recent logs
            status_info += "\n=== RECENT ACTIVITY ===\n"
            recent_logs = self.logger.get_recent_logs(5)
            for log in recent_logs:
                status_info += f"{log['timestamp']}: {log['message']}\n"
            
            self.status_text.delete(1.0, tk.END)
            self.status_text.insert(1.0, status_info)
            
            # Update streak display
            self.update_streak_display()
            
            # Update blocklist display
            self.update_blocklist_display()
            
        except Exception as e:
            self.status_text.delete(1.0, tk.END)
            self.status_text.insert(1.0, f"Error updating status: {str(e)}")
    
    def run(self):
        """Start the application"""
        self.root.mainloop()

if __name__ == "__main__":
    app = AdultBlockerApp()
    app.run()
