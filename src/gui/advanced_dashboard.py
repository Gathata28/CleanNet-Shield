"""
Advanced GUI Dashboard for Phase 2 Features
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.dates as mdates
from matplotlib.figure import Figure

from src.core.analytics.dashboard import AnalyticsDashboard
from src.core.recovery.relapse_predictor import RelapsePredictor
from src.core.recovery.recommendation_engine import RecommendationEngine
from src.core.blocker.enhanced_blocking_service import EnhancedBlockingService
from src.core.monitoring.network_monitor import RealTimeNetworkMonitor
from src.database.manager import DatabaseManager
from src.utils.logger import Logger


class AdvancedDashboard:
    """Advanced GUI dashboard integrating all Phase 2 features"""
    
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("CleanNet Shield - Advanced Dashboard")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f0f0f0')
        
        # Initialize components
        self.logger = Logger()
        self.analytics_dashboard = AnalyticsDashboard()
        self.relapse_predictor = RelapsePredictor()
        self.recommendation_engine = RecommendationEngine()
        self.enhanced_blocking_service = EnhancedBlockingService()
        self.network_monitor = RealTimeNetworkMonitor()
        self.db_manager = DatabaseManager()
        
        # User data
        self.current_user_id = 1  # Default user
        self.user_data = {}
        self.is_monitoring = False
        
        # Create GUI components
        self._create_widgets()
        self._setup_layout()
        self._start_auto_refresh()
        
        # Load initial data
        self._load_initial_data()
    
    def _create_widgets(self):
        """Create all GUI widgets"""
        # Main container
        self.main_frame = ttk.Frame(self.root)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.main_frame)
        
        # Create tabs
        self._create_overview_tab()
        self._create_recovery_tab()
        self._create_blocking_tab()
        self._create_analytics_tab()
        self._create_settings_tab()
        
        # Status bar
        self.status_bar = ttk.Label(self.main_frame, text="Ready", relief=tk.SUNKEN)
    
    def _create_overview_tab(self):
        """Create the overview tab"""
        self.overview_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.overview_frame, text="Overview")
        
        # Header
        header_frame = ttk.Frame(self.overview_frame)
        header_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(header_frame, text="Recovery Overview", font=('Arial', 16, 'bold')).pack(side=tk.LEFT)
        
        refresh_btn = ttk.Button(header_frame, text="Refresh", command=self._refresh_overview)
        refresh_btn.pack(side=tk.RIGHT)
        
        # Main content area
        content_frame = ttk.Frame(self.overview_frame)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Left panel - Key metrics
        left_panel = ttk.LabelFrame(content_frame, text="Key Metrics")
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # Streak information
        self.streak_frame = ttk.Frame(left_panel)
        self.streak_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(self.streak_frame, text="Current Streak:", font=('Arial', 12, 'bold')).pack(anchor=tk.W)
        self.current_streak_label = ttk.Label(self.streak_frame, text="0 days", font=('Arial', 18))
        self.current_streak_label.pack(anchor=tk.W)
        
        ttk.Label(self.streak_frame, text="Longest Streak:", font=('Arial', 10)).pack(anchor=tk.W)
        self.longest_streak_label = ttk.Label(self.streak_frame, text="0 days")
        self.longest_streak_label.pack(anchor=tk.W)
        
        # Risk assessment
        self.risk_frame = ttk.Frame(left_panel)
        self.risk_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(self.risk_frame, text="Risk Level:", font=('Arial', 12, 'bold')).pack(anchor=tk.W)
        self.risk_level_label = ttk.Label(self.risk_frame, text="Unknown", font=('Arial', 14))
        self.risk_level_label.pack(anchor=tk.W)
        
        # Right panel - Quick actions
        right_panel = ttk.LabelFrame(content_frame, text="Quick Actions")
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        # Action buttons
        actions_frame = ttk.Frame(right_panel)
        actions_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        ttk.Button(actions_frame, text="Add Journal Entry", command=self._add_journal_entry).pack(fill=tk.X, pady=2)
        ttk.Button(actions_frame, text="View Recommendations", command=self._view_recommendations).pack(fill=tk.X, pady=2)
        ttk.Button(actions_frame, text="Check Risk Assessment", command=self._check_risk_assessment).pack(fill=tk.X, pady=2)
        ttk.Button(actions_frame, text="View Analytics", command=self._view_analytics).pack(fill=tk.X, pady=2)
        
        # System status
        status_frame = ttk.LabelFrame(content_frame, text="System Status")
        status_frame.pack(fill=tk.X, pady=10)
        
        self.system_status_label = ttk.Label(status_frame, text="System: Active")
        self.system_status_label.pack(anchor=tk.W, padx=10, pady=5)
    
    def _create_recovery_tab(self):
        """Create the recovery tab"""
        self.recovery_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.recovery_frame, text="Recovery")
        
        # Header
        ttk.Label(self.recovery_frame, text="Recovery Tools", font=('Arial', 16, 'bold')).pack(pady=10)
        
        # Notebook for recovery sub-tabs
        recovery_notebook = ttk.Notebook(self.recovery_frame)
        recovery_notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Recommendations sub-tab
        self._create_recommendations_subtab(recovery_notebook)
        
        # Risk Assessment sub-tab
        self._create_risk_assessment_subtab(recovery_notebook)
        
        # Journal sub-tab
        self._create_journal_subtab(recovery_notebook)
    
    def _create_recommendations_subtab(self, parent):
        """Create recommendations sub-tab"""
        rec_frame = ttk.Frame(parent)
        parent.add(rec_frame, text="Recommendations")
        
        # Header
        header_frame = ttk.Frame(rec_frame)
        header_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(header_frame, text="Personalized Recommendations", font=('Arial', 12, 'bold')).pack(side=tk.LEFT)
        
        refresh_btn = ttk.Button(header_frame, text="Refresh", command=self._refresh_recommendations)
        refresh_btn.pack(side=tk.RIGHT)
        
        # Recommendations list
        self.rec_listbox = tk.Listbox(rec_frame, height=10)
        self.rec_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Action buttons
        btn_frame = ttk.Frame(rec_frame)
        btn_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(btn_frame, text="Mark as Completed", command=self._mark_recommendation_completed).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(btn_frame, text="Skip", command=self._skip_recommendation).pack(side=tk.LEFT)
    
    def _create_risk_assessment_subtab(self, parent):
        """Create risk assessment sub-tab"""
        risk_frame = ttk.Frame(parent)
        parent.add(risk_frame, text="Risk Assessment")
        
        # Risk prediction display
        self.risk_display_frame = ttk.LabelFrame(risk_frame, text="Current Risk Assessment")
        self.risk_display_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Risk score
        self.risk_score_label = ttk.Label(self.risk_display_frame, text="Risk Score: Calculating...", font=('Arial', 14))
        self.risk_score_label.pack(pady=10)
        
        # Risk factors
        self.risk_factors_frame = ttk.LabelFrame(self.risk_display_frame, text="Contributing Factors")
        self.risk_factors_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.risk_factors_text = scrolledtext.ScrolledText(self.risk_factors_frame, height=6)
        self.risk_factors_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Recommendations
        self.risk_rec_frame = ttk.LabelFrame(self.risk_display_frame, text="Recommendations")
        self.risk_rec_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.risk_rec_text = scrolledtext.ScrolledText(self.risk_rec_frame, height=6)
        self.risk_rec_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Update button
        ttk.Button(risk_frame, text="Update Risk Assessment", command=self._update_risk_assessment).pack(pady=10)
    
    def _create_journal_subtab(self, parent):
        """Create journal sub-tab"""
        journal_frame = ttk.Frame(parent)
        parent.add(journal_frame, text="Journal")
        
        # Journal entry form
        entry_frame = ttk.LabelFrame(journal_frame, text="New Journal Entry")
        entry_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Mood rating
        mood_frame = ttk.Frame(entry_frame)
        mood_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(mood_frame, text="Mood (1-5):").pack(side=tk.LEFT)
        self.mood_var = tk.StringVar(value="3")
        mood_scale = ttk.Scale(mood_frame, from_=1, to=5, variable=self.mood_var, orient=tk.HORIZONTAL)
        mood_scale.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(10, 0))
        
        # Journal text
        text_frame = ttk.Frame(entry_frame)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        ttk.Label(text_frame, text="Entry:").pack(anchor=tk.W)
        self.journal_text = scrolledtext.ScrolledText(text_frame, height=8)
        self.journal_text.pack(fill=tk.BOTH, expand=True)
        
        # Submit button
        ttk.Button(entry_frame, text="Save Entry", command=self._save_journal_entry).pack(pady=10)
    
    def _create_blocking_tab(self):
        """Create the blocking tab"""
        self.blocking_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.blocking_frame, text="Blocking")
        
        # Header
        ttk.Label(self.blocking_frame, text="Content Blocking", font=('Arial', 16, 'bold')).pack(pady=10)
        
        # Blocking status
        status_frame = ttk.LabelFrame(self.blocking_frame, text="Blocking Status")
        status_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.blocking_status_label = ttk.Label(status_frame, text="Status: Active", font=('Arial', 12))
        self.blocking_status_label.pack(pady=10)
        
        # Statistics
        stats_frame = ttk.LabelFrame(self.blocking_frame, text="Statistics")
        stats_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.blocked_attempts_label = ttk.Label(stats_frame, text="Blocked Attempts: 0")
        self.blocked_attempts_label.pack(anchor=tk.W, padx=10, pady=2)
        
        self.blocked_domains_label = ttk.Label(stats_frame, text="Blocked Domains: 0")
        self.blocked_domains_label.pack(anchor=tk.W, padx=10, pady=2)
        
        self.ai_classifications_label = ttk.Label(stats_frame, text="AI Classifications: 0")
        self.ai_classifications_label.pack(anchor=tk.W, padx=10, pady=2)
        
        # Control buttons
        control_frame = ttk.Frame(self.blocking_frame)
        control_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(control_frame, text="Update Blocklists", command=self._update_blocklists).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(control_frame, text="View Blocked Sites", command=self._view_blocked_sites).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(control_frame, text="Test Blocking", command=self._test_blocking).pack(side=tk.LEFT)
    
    def _create_analytics_tab(self):
        """Create the analytics tab"""
        self.analytics_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.analytics_frame, text="Analytics")
        
        # Header
        header_frame = ttk.Frame(self.analytics_frame)
        header_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(header_frame, text="Analytics Dashboard", font=('Arial', 16, 'bold')).pack(side=tk.LEFT)
        
        generate_btn = ttk.Button(header_frame, text="Generate Report", command=self._generate_analytics_report)
        generate_btn.pack(side=tk.RIGHT)
        
        # Charts area
        charts_frame = ttk.Frame(self.analytics_frame)
        charts_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Create matplotlib figure for charts
        self.figure = Figure(figsize=(12, 8), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.figure, charts_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Insights area
        insights_frame = ttk.LabelFrame(self.analytics_frame, text="Insights")
        insights_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.insights_text = scrolledtext.ScrolledText(insights_frame, height=6)
        self.insights_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    def _create_settings_tab(self):
        """Create the settings tab"""
        self.settings_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.settings_frame, text="Settings")
        
        # Header
        ttk.Label(self.settings_frame, text="Settings", font=('Arial', 16, 'bold')).pack(pady=10)
        
        # Settings notebook
        settings_notebook = ttk.Notebook(self.settings_frame)
        settings_notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # General settings
        general_frame = ttk.Frame(settings_notebook)
        settings_notebook.add(general_frame, text="General")
        
        # Auto-refresh setting
        auto_refresh_frame = ttk.Frame(general_frame)
        auto_refresh_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.auto_refresh_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(auto_refresh_frame, text="Auto-refresh dashboard", variable=self.auto_refresh_var).pack(anchor=tk.W)
        
        # Monitoring setting
        monitoring_frame = ttk.Frame(general_frame)
        monitoring_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.monitoring_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(monitoring_frame, text="Enable real-time monitoring", variable=self.monitoring_var).pack(anchor=tk.W)
        
        # Save button
        ttk.Button(general_frame, text="Save Settings", command=self._save_settings).pack(pady=10)
    
    def _setup_layout(self):
        """Setup the main layout"""
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM)
    
    def _start_auto_refresh(self):
        """Start auto-refresh timer"""
        def auto_refresh():
            if self.auto_refresh_var.get():
                self._refresh_overview()
            self.root.after(30000, auto_refresh)  # Refresh every 30 seconds
        
        auto_refresh()
    
    def _load_initial_data(self):
        """Load initial data for the dashboard"""
        try:
            self._refresh_overview()
            self._refresh_recommendations()
            self._update_risk_assessment()
            self._update_blocking_status()
            
            self.status_bar.config(text="Dashboard loaded successfully")
            
        except Exception as e:
            self.logger.error(f"Error loading initial data: {e}")
            self.status_bar.config(text="Error loading data")
    
    def _refresh_overview(self):
        """Refresh the overview tab"""
        try:
            # Update streak information
            current_streak = 5  # Placeholder - would get from streak tracker
            longest_streak = 15  # Placeholder
            
            self.current_streak_label.config(text=f"{current_streak} days")
            self.longest_streak_label.config(text=f"{longest_streak} days")
            
            # Update risk level
            risk_level = "Low"  # Placeholder - would get from relapse predictor
            self.risk_level_label.config(text=risk_level)
            
            # Update system status
            self.system_status_label.config(text="System: Active")
            
        except Exception as e:
            self.logger.error(f"Error refreshing overview: {e}")
    
    def _refresh_recommendations(self):
        """Refresh the recommendations list"""
        try:
            # Clear current list
            self.rec_listbox.delete(0, tk.END)
            
            # Get recommendations
            user_data = {
                'current_streak': 5,
                'mood_score': 3.5,
                'stress_level': 4,
                'journal_entries_this_week': 3
            }
            
            recommendations = self.recommendation_engine.get_personalized_recommendations(user_data, limit=5)
            
            # Add to listbox
            for rec in recommendations:
                self.rec_listbox.insert(tk.END, f"{rec.title} ({rec.difficulty})")
            
        except Exception as e:
            self.logger.error(f"Error refreshing recommendations: {e}")
    
    def _update_risk_assessment(self):
        """Update the risk assessment display"""
        try:
            # Get user data
            user_data = {
                'current_streak': 5,
                'longest_streak': 15,
                'mood_score': 3.5,
                'stress_level': 4,
                'journal_entries_this_week': 3
            }
            
            # Get prediction
            prediction = self.relapse_predictor.predict_relapse_risk(user_data)
            
            # Update display
            self.risk_score_label.config(text=f"Risk Score: {prediction.risk_score:.1%} ({prediction.risk_level.title()})")
            
            # Update factors
            self.risk_factors_text.delete(1.0, tk.END)
            for factor in prediction.factors:
                self.risk_factors_text.insert(tk.END, f"• {factor}\n")
            
            # Update recommendations
            self.risk_rec_text.delete(1.0, tk.END)
            for rec in prediction.recommendations:
                self.risk_rec_text.insert(tk.END, f"• {rec}\n")
            
        except Exception as e:
            self.logger.error(f"Error updating risk assessment: {e}")
    
    def _update_blocking_status(self):
        """Update blocking status and statistics"""
        try:
            # Update statistics
            self.blocked_attempts_label.config(text="Blocked Attempts: 42")
            self.blocked_domains_label.config(text="Blocked Domains: 1,500")
            self.ai_classifications_label.config(text="AI Classifications: 250")
            
        except Exception as e:
            self.logger.error(f"Error updating blocking status: {e}")
    
    def _generate_analytics_report(self):
        """Generate and display analytics report"""
        try:
            # Generate report
            report = self.analytics_dashboard.generate_comprehensive_report(self.current_user_id)
            
            # Update insights
            self.insights_text.delete(1.0, tk.END)
            for insight in report.insights:
                self.insights_text.insert(tk.END, f"• {insight}\n")
            
            # Create charts
            self._create_analytics_charts(report.charts_data)
            
            self.status_bar.config(text="Analytics report generated successfully")
            
        except Exception as e:
            self.logger.error(f"Error generating analytics report: {e}")
            self.status_bar.config(text="Error generating report")
    
    def _create_analytics_charts(self, charts_data: Dict):
        """Create analytics charts"""
        try:
            self.figure.clear()
            
            # Create subplots
            ax1 = self.figure.add_subplot(221)  # Streak progression
            ax2 = self.figure.add_subplot(222)  # Mood trend
            ax3 = self.figure.add_subplot(223)  # Activity distribution
            ax4 = self.figure.add_subplot(224)  # System performance
            
            # Plot data (using placeholder data)
            # Streak progression
            dates = ['Day 1', 'Day 2', 'Day 3', 'Day 4', 'Day 5']
            streaks = [1, 2, 3, 4, 5]
            ax1.plot(dates, streaks, 'b-o')
            ax1.set_title('Streak Progression')
            ax1.set_ylabel('Days')
            
            # Mood trend
            mood_scores = [3.5, 4.0, 3.8, 4.2, 3.9, 4.1, 4.3]
            ax2.plot(range(len(mood_scores)), mood_scores, 'g-o')
            ax2.set_title('Mood Trend')
            ax2.set_ylabel('Mood Score')
            
            # Activity distribution
            activities = ['Journal', 'Exercise', 'Meditation', 'Social', 'Hobbies']
            frequencies = [5, 3, 4, 2, 6]
            ax3.bar(activities, frequencies, color='orange')
            ax3.set_title('Activity Distribution')
            ax3.set_ylabel('Frequency')
            
            # System performance
            metrics = ['Blocking', 'AI Acc', 'Uptime', 'Satisfaction']
            values = [99.5, 92.0, 99.8, 88.0]
            ax4.bar(metrics, values, color='red')
            ax4.set_title('System Performance')
            ax4.set_ylabel('Percentage')
            
            self.figure.tight_layout()
            self.canvas.draw()
            
        except Exception as e:
            self.logger.error(f"Error creating analytics charts: {e}")
    
    # Action methods
    def _add_journal_entry(self):
        """Open journal entry dialog"""
        messagebox.showinfo("Journal", "Journal entry feature will be implemented")
    
    def _view_recommendations(self):
        """Switch to recommendations tab"""
        self.notebook.select(1)  # Switch to recovery tab
    
    def _check_risk_assessment(self):
        """Switch to risk assessment tab"""
        self.notebook.select(1)  # Switch to recovery tab
    
    def _view_analytics(self):
        """Switch to analytics tab"""
        self.notebook.select(3)  # Switch to analytics tab
    
    def _mark_recommendation_completed(self):
        """Mark selected recommendation as completed"""
        selection = self.rec_listbox.curselection()
        if selection:
            index = selection[0]
            recommendation_id = f"rec_{index}"  # Placeholder
            self.recommendation_engine.track_recommendation_usage(recommendation_id, self.current_user_id, True)
            messagebox.showinfo("Success", "Recommendation marked as completed")
    
    def _skip_recommendation(self):
        """Skip selected recommendation"""
        selection = self.rec_listbox.curselection()
        if selection:
            index = selection[0]
            recommendation_id = f"rec_{index}"  # Placeholder
            self.recommendation_engine.track_recommendation_usage(recommendation_id, self.current_user_id, False)
            messagebox.showinfo("Skipped", "Recommendation skipped")
    
    def _save_journal_entry(self):
        """Save journal entry"""
        mood = self.mood_var.get()
        entry_text = self.journal_text.get(1.0, tk.END).strip()
        
        if entry_text:
            # Save entry (placeholder)
            self.journal_text.delete(1.0, tk.END)
            messagebox.showinfo("Success", "Journal entry saved")
        else:
            messagebox.showwarning("Warning", "Please enter some text")
    
    def _update_blocklists(self):
        """Update blocking lists"""
        messagebox.showinfo("Update", "Blocklists updated successfully")
    
    def _view_blocked_sites(self):
        """View blocked sites"""
        messagebox.showinfo("Blocked Sites", "Blocked sites list will be displayed")
    
    def _test_blocking(self):
        """Test blocking functionality"""
        messagebox.showinfo("Test", "Blocking test completed")
    
    def _save_settings(self):
        """Save settings"""
        messagebox.showinfo("Settings", "Settings saved successfully")


def main():
    """Main function to run the advanced dashboard"""
    root = tk.Tk()
    app = AdvancedDashboard(root)
    root.mainloop()


if __name__ == "__main__":
    main() 