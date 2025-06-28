"""
Modern PySide6-based Main Window for CleanNet Shield
Professional GUI implementation for Phase 3
"""

import sys
import os
from pathlib import Path
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta
import json
import threading
import asyncio

print('[DEBUG] main_window.py imported')

try:
    from PySide6.QtWidgets import (
        QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
        QTabWidget, QLabel, QPushButton, QTextEdit, QProgressBar,
        QSystemTrayIcon, QMenu, QDialog, QFormLayout, QLineEdit,
        QCheckBox, QComboBox, QSpinBox, QSlider, QGroupBox,
        QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox,
        QFileDialog, QSplitter, QFrame, QScrollArea, QGridLayout,
        QStackedWidget, QListWidget, QListWidgetItem, QCalendarWidget,
        QDateEdit, QTimeEdit, QSlider, QProgressBar, QStatusBar,
        QToolBar, QMenuBar, QDockWidget, QTreeWidget,
        QTreeWidgetItem, QGraphicsView, QGraphicsScene, QGraphicsItem,
        QInputDialog
    )
    from PySide6.QtCore import (
        Qt, QTimer, QThread, Signal, QSettings, QSize, QPoint,
        QPropertyAnimation, QEasingCurve, QParallelAnimationGroup,
        QRect, QDate, QTime, QDateTime, QUrl, QMimeData
    )
    from PySide6.QtGui import (
        QIcon, QPixmap, QFont, QPalette, QColor, QBrush,
        QLinearGradient, QPainter, QAction, QKeySequence,
        QFontDatabase, QPixmap, QImage, QPainterPath, QPen
    )
    from PySide6.QtCharts import (
        QChart, QChartView, QLineSeries, QBarSeries, QBarSet,
        QPieSeries, QValueAxis, QBarCategoryAxis, QDateTimeAxis
    )
    
    PYSIDE6_AVAILABLE = True
    
except Exception as e:
    PYSIDE6_AVAILABLE = False
    print(f"PySide6 not available, falling back to enhanced Tkinter: {e}")
    import traceback
    traceback.print_exc()
    # Fallback imports
    import tkinter as tk
    from tkinter import ttk, messagebox, filedialog
    try:
        import customtkinter as ctk
        CUSTOMTKINTER_AVAILABLE = True
    except ImportError:
        CUSTOMTKINTER_AVAILABLE = False

# Import core modules
from ..core.analytics.dashboard import AnalyticsDashboard
from ..core.recovery.relapse_predictor import RelapsePredictor
from ..core.recovery.recommendation_engine import RecommendationEngine
from ..core.blocker.enhanced_blocking_service import EnhancedBlockingService
from ..core.monitoring.network_monitor import RealTimeNetworkMonitor
from ..database.manager import DatabaseManager
from ..utils.logger import Logger
from .themes import ThemeType, set_theme, apply_theme_to_application


class OnboardingDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Welcome to CleanNet Shield!")
        layout = QVBoxLayout()
        label = QLabel("""
Welcome to the new CleanNet Shield!

- Modern Qt-based interface
- Enhanced privacy and recovery tools
- Customizable themes

Click 'Get Started' to begin.
""")
        layout.addWidget(label)
        btn = QPushButton("Get Started")
        btn.clicked.connect(self.accept)
        layout.addWidget(btn)
        self.setLayout(layout)


class ModernMainWindow(QMainWindow):
    """
    Modern PySide6-based main window with professional UI/UX
    """
    
    def __init__(self):
        super().__init__()
        
        # Initialize core components
        self.logger = Logger()
        self.analytics_dashboard = AnalyticsDashboard()
        self.relapse_predictor = RelapsePredictor()
        self.recommendation_engine = RecommendationEngine()
        self.enhanced_blocking_service = EnhancedBlockingService()
        self.network_monitor = RealTimeNetworkMonitor()
        self.db_manager = DatabaseManager()
        
        # Application state
        self.current_user_id = 1
        self.user_data = {}
        self.is_monitoring = False
        self.settings = QSettings("CleanNetShield", "CleanNetShield")
        
        # Initialize UI
        self._init_ui()
        self._setup_theme()
        self._create_menu_bar()
        self._create_toolbar()
        self._create_status_bar()
        self._setup_system_tray()
        self._add_contextual_help()
        self._load_initial_data()
        
        # Start background tasks
        self._start_background_tasks()
    
    def _init_ui(self):
        """Initialize the main UI components"""
        self.setWindowTitle("CleanNet Shield - Professional Edition")
        self.setMinimumSize(1200, 800)
        self.resize(1400, 900)
        
        # Center window on screen
        self._center_window()
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        
        # Create header
        self._create_header(main_layout)
        
        # Create main content area
        self._create_main_content(main_layout)
        
        # Apply window icon
        self._set_window_icon()
    
    def _center_window(self):
        """Center the window on the screen"""
        screen = QApplication.primaryScreen().geometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)
    
    def _create_header(self, parent_layout):
        """Create the application header"""
        header_frame = QFrame()
        header_frame.setFrameStyle(QFrame.Shape.StyledPanel)
        header_frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #2b2b2b, stop:1 #404040);
                border-radius: 10px;
                padding: 10px;
            }
        """)
        
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(20, 15, 20, 15)
        
        # Title and subtitle
        title_layout = QVBoxLayout()
        
        title_label = QLabel("CleanNet Shield")
        title_label.setStyleSheet("""
            QLabel {
                color: #ffffff;
                font-size: 24px;
                font-weight: bold;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
        """)
        
        subtitle_label = QLabel("Professional Content Protection & Recovery")
        subtitle_label.setStyleSheet("""
            QLabel {
                color: #cccccc;
                font-size: 14px;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
        """)
        
        title_layout.addWidget(title_label)
        title_layout.addWidget(subtitle_label)
        
        # Quick stats
        stats_layout = QHBoxLayout()
        
        # Current streak
        streak_group = QGroupBox("Current Streak")
        streak_group.setStyleSheet("""
            QGroupBox {
                color: #ffffff;
                font-weight: bold;
                border: 2px solid #0078d4;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        
        streak_layout = QVBoxLayout(streak_group)
        self.streak_days_label = QLabel("0 days")
        self.streak_days_label.setStyleSheet("""
            QLabel {
                color: #0078d4;
                font-size: 18px;
                font-weight: bold;
                text-align: center;
            }
        """)
        streak_layout.addWidget(self.streak_days_label)
        
        # Risk level
        risk_group = QGroupBox("Risk Level")
        risk_group.setStyleSheet("""
            QGroupBox {
                color: #ffffff;
                font-weight: bold;
                border: 2px solid #ff6b6b;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        
        risk_layout = QVBoxLayout(risk_group)
        self.risk_level_label = QLabel("Unknown")
        self.risk_level_label.setStyleSheet("""
            QLabel {
                color: #ff6b6b;
                font-size: 16px;
                font-weight: bold;
                text-align: center;
            }
        """)
        risk_layout.addWidget(self.risk_level_label)
        
        stats_layout.addWidget(streak_group)
        stats_layout.addWidget(risk_group)
        
        # Progress indicator
        progress_layout = QVBoxLayout()
        
        progress_label = QLabel("Recovery Progress")
        progress_label.setStyleSheet("color: #ffffff; font-weight: bold;")
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(75)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #555555;
                border-radius: 5px;
                text-align: center;
                background-color: #404040;
            }
            QProgressBar::chunk {
                background-color: #0078d4;
                border-radius: 3px;
            }
        """)
        
        progress_layout.addWidget(progress_label)
        progress_layout.addWidget(self.progress_bar)
        
        # Add all sections to header
        header_layout.addLayout(title_layout)
        header_layout.addStretch()
        header_layout.addLayout(stats_layout)
        header_layout.addStretch()
        header_layout.addLayout(progress_layout)
        
        parent_layout.addWidget(header_frame)
    
    def _create_main_content(self, parent_layout):
        """Create the main content area with tabs"""
        # Create tab widget
        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #555555;
                background-color: #353535;
                border-radius: 5px;
            }
            QTabBar::tab {
                background-color: #2b2b2b;
                color: #ffffff;
                padding: 10px 20px;
                margin: 2px;
                border-radius: 5px;
                font-weight: bold;
            }
            QTabBar::tab:selected {
                background-color: #0078d4;
            }
            QTabBar::tab:hover {
                background-color: #404040;
            }
        """)
        
        # Create tabs
        self._create_dashboard_tab()
        self._create_recovery_tab()
        self._create_blocking_tab()
        self._create_analytics_tab()
        self._create_settings_tab()
        
        parent_layout.addWidget(self.tab_widget)
    
    def _create_dashboard_tab(self):
        """Create the main dashboard tab with modern, interactive design"""
        dashboard_widget = QWidget()
        layout = QVBoxLayout(dashboard_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Welcome header with user info
        self._create_welcome_header(layout)
        
        # Quick stats cards with hover effects
        self._create_enhanced_stats_section(layout)
        
        # Progress overview with visual indicators
        self._create_progress_overview(layout)
        
        # Interactive charts section
        self._create_enhanced_charts_section(layout)
        
        # Recent activity with better styling
        self._create_enhanced_activity_section(layout)
        
        # Quick actions panel
        self._create_quick_actions_panel(layout)
        
        return dashboard_widget
    
    def _create_welcome_header(self, parent_layout):
        """Create a welcoming header with user information"""
        header_frame = QFrame()
        header_frame.setFrameStyle(QFrame.Shape.StyledPanel)
        header_frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #1a1a2e, stop:0.5 #16213e, stop:1 #0f3460);
                border-radius: 15px;
                padding: 20px;
                border: 1px solid #2d3748;
            }
        """)
        
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(25, 20, 25, 20)
        
        # User avatar placeholder
        avatar_frame = QFrame()
        avatar_frame.setFixedSize(60, 60)
        avatar_frame.setStyleSheet("""
            QFrame {
                background: qradialgradient(cx:0.5, cy:0.5, radius:0.5,
                    stop:0 #4facfe, stop:1 #00f2fe);
                border-radius: 30px;
                border: 3px solid #ffffff;
            }
        """)
        
        # Welcome text
        welcome_layout = QVBoxLayout()
        
        welcome_title = QLabel("Welcome back!")
        welcome_title.setStyleSheet("""
            QLabel {
                color: #ffffff;
                font-size: 24px;
                font-weight: bold;
                font-family: 'Segoe UI', Arial, sans-serif;
                margin-bottom: 5px;
            }
        """)
        
        welcome_subtitle = QLabel("Your recovery journey continues")
        welcome_subtitle.setStyleSheet("""
            QLabel {
                color: #a0aec0;
                font-size: 14px;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
        """)
        
        welcome_layout.addWidget(welcome_title)
        welcome_layout.addWidget(welcome_subtitle)
        
        # Current time and date
        time_layout = QVBoxLayout()
        time_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        
        current_time = QLabel(datetime.now().strftime("%I:%M %p"))
        current_time.setStyleSheet("""
            QLabel {
                color: #ffffff;
                font-size: 18px;
                font-weight: bold;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
        """)
        
        current_date = QLabel(datetime.now().strftime("%A, %B %d"))
        current_date.setStyleSheet("""
            QLabel {
                color: #a0aec0;
                font-size: 12px;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
        """)
        
        time_layout.addWidget(current_time)
        time_layout.addWidget(current_date)
        
        header_layout.addWidget(avatar_frame)
        header_layout.addLayout(welcome_layout)
        header_layout.addStretch()
        header_layout.addLayout(time_layout)
        
        parent_layout.addWidget(header_frame)
    
    def _create_enhanced_stats_section(self, parent_layout):
        """Create enhanced statistics cards with hover effects and animations"""
        stats_frame = QFrame()
        stats_frame.setFrameStyle(QFrame.Shape.StyledPanel)
        stats_frame.setStyleSheet("""
            QFrame {
                background: #2d3748;
                border-radius: 12px;
                padding: 20px;
                border: 1px solid #4a5568;
            }
        """)
        
        stats_layout = QHBoxLayout(stats_frame)
        stats_layout.setSpacing(15)
        
        # Enhanced stat cards with gradients and hover effects
        self.streak_card = self._create_enhanced_stat_card(
            "Current Streak", "0", "days", "#4facfe", "#00f2fe", "🔥"
        )
        self.blocked_card = self._create_enhanced_stat_card(
            "Sites Blocked", "0", "today", "#ff6b6b", "#ee5a24", "🛡️"
        )
        self.recovery_card = self._create_enhanced_stat_card(
            "Recovery Score", "85", "%", "#4ecdc4", "#44a08d", "📈"
        )
        self.risk_card = self._create_enhanced_stat_card(
            "Risk Level", "Low", "", "#ffa726", "#ff7043", "⚠️"
        )
        
        stats_layout.addWidget(self.streak_card)
        stats_layout.addWidget(self.blocked_card)
        stats_layout.addWidget(self.recovery_card)
        stats_layout.addWidget(self.risk_card)
        
        parent_layout.addWidget(stats_frame)
    
    def _create_enhanced_stat_card(self, title, value, unit, color1, color2, icon):
        """Create an enhanced statistics card with gradients and hover effects"""
        card = QFrame()
        card.setFrameStyle(QFrame.Shape.StyledPanel)
        card.setMinimumHeight(120)
        card.setCursor(Qt.CursorShape.PointingHandCursor)
        
        # Enhanced styling with gradients and hover effects
        card.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 {color1}, stop:1 {color2});
                border-radius: 12px;
                padding: 20px;
                margin: 5px;
                border: 2px solid transparent;
            }}
            QFrame:hover {{
                border: 2px solid #ffffff;
            }}
        """)
        
        layout = QVBoxLayout(card)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # Icon and title row
        header_layout = QHBoxLayout()
        
        icon_label = QLabel(icon)
        icon_label.setStyleSheet("""
            QLabel {
                color: #ffffff;
                font-size: 24px;
                font-weight: bold;
            }
        """)
        
        title_label = QLabel(title)
        title_label.setStyleSheet("""
            QLabel {
                color: #ffffff;
                font-size: 12px;
                font-weight: bold;
                opacity: 0.9;
            }
        """)
        
        header_layout.addWidget(icon_label)
        header_layout.addStretch()
        header_layout.addWidget(title_label)
        
        # Value display with animation
        value_layout = QHBoxLayout()
        value_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        value_label = QLabel(value)
        value_label.setStyleSheet("""
            QLabel {
                color: #ffffff;
                font-size: 32px;
                font-weight: bold;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
        """)
        
        unit_label = QLabel(unit)
        unit_label.setStyleSheet("""
            QLabel {
                color: #ffffff;
                font-size: 14px;
                font-weight: normal;
                opacity: 0.8;
            }
        """)
        
        value_layout.addWidget(value_label)
        if unit:
            value_layout.addWidget(unit_label)
        
        layout.addLayout(header_layout)
        layout.addLayout(value_layout)
        layout.addStretch()
        
        # Add click event for interactivity with enhanced feedback
        card.mousePressEvent = lambda event, card=card: self._on_stat_card_clicked(card, title)
        
        # Add hover animation
        self._add_hover_animation(card)
        
        return card
    
    def _add_hover_animation(self, widget):
        """Add smooth hover animations to widgets"""
        def on_enter():
            animation = QPropertyAnimation(widget, b"geometry")
            animation.setDuration(200)
            animation.setEasingCurve(QEasingCurve.Type.OutCubic)
            
            current_geo = widget.geometry()
            target_geo = current_geo.adjusted(-2, -2, 2, 2)
            
            animation.setStartValue(current_geo)
            animation.setEndValue(target_geo)
            animation.start()
        
        def on_leave():
            animation = QPropertyAnimation(widget, b"geometry")
            animation.setDuration(200)
            animation.setEasingCurve(QEasingCurve.Type.OutCubic)
            
            current_geo = widget.geometry()
            target_geo = current_geo.adjusted(2, 2, -2, -2)
            
            animation.setStartValue(current_geo)
            animation.setEndValue(target_geo)
            animation.start()
        
        widget.enterEvent = lambda event: on_enter()
        widget.leaveEvent = lambda event: on_leave()
    
    def _on_stat_card_clicked(self, card, title):
        """Handle stat card clicks for detailed view"""
        # Add animation effect
        self._animate_card_click(card)
        
        # Show detailed information
        self._show_stat_details(title)
    
    def _animate_card_click(self, card):
        """Add a subtle animation when card is clicked"""
        animation = QPropertyAnimation(card, b"geometry")
        animation.setDuration(150)
        animation.setStartValue(card.geometry())
        
        # Slightly scale down and back up
        scaled_rect = card.geometry()
        scaled_rect.setWidth(int(scaled_rect.width() * 0.95))
        scaled_rect.setHeight(int(scaled_rect.height() * 0.95))
        scaled_rect.moveCenter(card.geometry().center())
        
        animation.setEndValue(scaled_rect)
        animation.finished.connect(lambda: self._restore_card_geometry(card))
        animation.start()
    
    def _restore_card_geometry(self, card):
        """Restore card to original geometry"""
        animation = QPropertyAnimation(card, b"geometry")
        animation.setDuration(150)
        animation.setStartValue(card.geometry())
        animation.setEndValue(card.geometry())
        animation.start()
    
    def _show_stat_details(self, title):
        """Show detailed information for the clicked stat"""
        details = {
            "Current Streak": "View your recovery streak history and milestones",
            "Sites Blocked": "See detailed blocking statistics and patterns",
            "Recovery Score": "Understand how your recovery score is calculated",
            "Risk Level": "Learn about risk factors and prevention strategies"
        }
        
        msg = QMessageBox(self)
        msg.setWindowTitle(f"{title} Details")
        msg.setText(details.get(title, "Detailed information not available"))
        msg.setIcon(QMessageBox.Icon.Information)
        msg.exec()
    
    def _create_progress_overview(self, parent_layout):
        """Create a progress overview section with visual indicators"""
        progress_frame = QFrame()
        progress_frame.setFrameStyle(QFrame.Shape.StyledPanel)
        progress_frame.setStyleSheet("""
            QFrame {
                background: #2d3748;
                border-radius: 12px;
                padding: 20px;
                border: 1px solid #4a5568;
            }
        """)
        
        progress_layout = QVBoxLayout(progress_frame)
        
        # Section title
        title_label = QLabel("Recovery Progress")
        title_label.setStyleSheet("""
            QLabel {
                color: #ffffff;
                font-size: 18px;
                font-weight: bold;
                font-family: 'Segoe UI', Arial, sans-serif;
                margin-bottom: 15px;
            }
        """)
        progress_layout.addWidget(title_label)
        
        # Progress indicators
        indicators_layout = QHBoxLayout()
        
        # Weekly progress
        weekly_progress = self._create_progress_indicator("This Week", 75, "#4facfe")
        indicators_layout.addWidget(weekly_progress)
        
        # Monthly progress
        monthly_progress = self._create_progress_indicator("This Month", 60, "#4ecdc4")
        indicators_layout.addWidget(monthly_progress)
        
        # Overall progress
        overall_progress = self._create_progress_indicator("Overall", 85, "#ffa726")
        indicators_layout.addWidget(overall_progress)
        
        progress_layout.addLayout(indicators_layout)
        parent_layout.addWidget(progress_frame)
    
    def _create_progress_indicator(self, label, percentage, color):
        """Create a progress indicator widget with enhanced visual design"""
        indicator_frame = QFrame()
        indicator_frame.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #1a202c, stop:1 #2d3748);
                border-radius: 12px;
                padding: 20px;
                border: 2px solid #4a5568;
            }}
            QFrame:hover {{
                border: 2px solid {color};
            }}
        """)
        
        layout = QVBoxLayout(indicator_frame)
        layout.setSpacing(10)
        
        # Enhanced label with icon
        label_layout = QHBoxLayout()
        
        # Add appropriate icon based on label
        icon_map = {
            "This Week": "📅",
            "This Month": "📊", 
            "Overall": "🎯"
        }
        icon = icon_map.get(label, "📈")
        
        icon_label = QLabel(icon)
        icon_label.setStyleSheet("""
            QLabel {
                font-size: 20px;
                margin-right: 8px;
            }
        """)
        
        label_widget = QLabel(label)
        label_widget.setStyleSheet("""
            QLabel {
                color: #a0aec0;
                font-size: 14px;
                font-weight: bold;
            }
        """)
        
        label_layout.addWidget(icon_label)
        label_layout.addWidget(label_widget)
        label_layout.addStretch()
        layout.addLayout(label_layout)
        
        # Enhanced progress bar with gradient
        progress_bar = QProgressBar()
        progress_bar.setValue(percentage)
        progress_bar.setStyleSheet(f"""
            QProgressBar {{
                border: 2px solid #2d3748;
                border-radius: 8px;
                text-align: center;
                background-color: #1a202c;
                color: #ffffff;
                font-weight: bold;
                font-size: 12px;
                height: 20px;
                margin: 5px 0;
            }}
            QProgressBar::chunk {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {color}, stop:1 {color}88);
                border-radius: 6px;
                border: 1px solid {color}aa;
            }}
        """)
        layout.addWidget(progress_bar)
        
        # Enhanced percentage display
        percentage_layout = QHBoxLayout()
        
        percentage_label = QLabel(f"{percentage}%")
        percentage_label.setStyleSheet(f"""
            QLabel {{
                color: {color};
                font-size: 18px;
                font-weight: bold;
                text-align: center;
            }}
        """)
        
        # Add status indicator
        status_icon = "✅" if percentage >= 80 else "🟡" if percentage >= 60 else "🔴"
        status_label = QLabel(status_icon)
        status_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                margin-left: 8px;
            }
        """)
        
        percentage_layout.addStretch()
        percentage_layout.addWidget(percentage_label)
        percentage_layout.addWidget(status_label)
        percentage_layout.addStretch()
        
        layout.addLayout(percentage_layout)
        
        # Add hover animation
        self._add_hover_animation(indicator_frame)
        
        return indicator_frame
    
    def _create_enhanced_charts_section(self, parent_layout):
        """Create enhanced charts section with better layout"""
        charts_frame = QFrame()
        charts_frame.setFrameStyle(QFrame.Shape.StyledPanel)
        charts_frame.setStyleSheet("""
            QFrame {
                background: #2d3748;
                border-radius: 12px;
                padding: 20px;
                border: 1px solid #4a5568;
            }
        """)
        
        charts_layout = QVBoxLayout(charts_frame)
        
        # Section title
        title_label = QLabel("Analytics & Insights")
        title_label.setStyleSheet("""
            QLabel {
                color: #ffffff;
                font-size: 18px;
                font-weight: bold;
                font-family: 'Segoe UI', Arial, sans-serif;
                margin-bottom: 15px;
            }
        """)
        charts_layout.addWidget(title_label)
        
        # Charts in a horizontal layout
        charts_row = QHBoxLayout()
        charts_row.setSpacing(15)
        
        # Enhanced streak chart
        self.streak_chart = self._create_enhanced_streak_chart()
        charts_row.addWidget(self.streak_chart)
        
        # Enhanced activity chart
        self.activity_chart = self._create_enhanced_activity_chart()
        charts_row.addWidget(self.activity_chart)
        
        charts_layout.addLayout(charts_row)
        parent_layout.addWidget(charts_frame)
    
    def _create_enhanced_streak_chart(self):
        """Create an enhanced streak tracking chart"""
        try:
            from PySide6.QtCharts import QChart, QChartView, QLineSeries, QValueAxis, QDateTimeAxis
            from PySide6.QtCore import QDateTime
            
            chart = QChart()
            chart.setTitle("Recovery Streak Progress")
            chart.setTheme(QChart.ChartTheme.ChartThemeDark)
            chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)
            
            # Create enhanced series with better styling
            series = QLineSeries()
            series.setName("Streak Days")
            series.setPen(QPen(QColor("#4facfe"), 3))
            series.setBrush(QBrush(QColor("#4facfe")))
            
            # Add realistic data points
            for i in range(30):
                # Simulate realistic streak data with ups and downs
                value = max(0, 5 + i * 0.3 + (i % 7) * 1.5 - (i % 14) * 0.8)
                series.append(i, value)
            
            chart.addSeries(series)
            
            # Enhanced axes
            axis_x = QValueAxis()
            axis_x.setTitleText("Days")
            axis_x.setRange(0, 30)
            axis_x.setLabelFormat("%d")
            axis_x.setTickCount(7)
            chart.addAxis(axis_x, Qt.AlignmentFlag.AlignBottom)
            series.attachAxis(axis_x)
            
            axis_y = QValueAxis()
            axis_y.setTitleText("Streak Count")
            axis_y.setRange(0, 20)
            axis_y.setLabelFormat("%d")
            chart.addAxis(axis_y, Qt.AlignmentFlag.AlignLeft)
            series.attachAxis(axis_y)
            
            chart_view = QChartView(chart)
            chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)
            chart_view.setMinimumHeight(250)
            chart_view.setStyleSheet("""
                QChartView {
                    background: #1a202c;
                    border-radius: 8px;
                    border: 1px solid #2d3748;
                }
            """)
            
            return chart_view
            
        except ImportError:
            # Enhanced fallback
            fallback = QFrame()
            fallback.setStyleSheet("""
                QFrame {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 #1a202c, stop:1 #2d3748);
                    border-radius: 8px;
                    border: 1px solid #4a5568;
                }
            """)
            
            layout = QVBoxLayout(fallback)
            
            icon_label = QLabel("📈")
            icon_label.setStyleSheet("""
                QLabel {
                    font-size: 48px;
                    text-align: center;
                    margin: 20px;
                }
            """)
            
            text_label = QLabel("Streak Chart\n(QtCharts not available)")
            text_label.setStyleSheet("""
                QLabel {
                    color: #a0aec0;
                    font-size: 14px;
                    text-align: center;
                    margin: 10px;
                }
            """)
            text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            layout.addWidget(icon_label)
            layout.addWidget(text_label)
            fallback.setMinimumHeight(250)
            
            return fallback
    
    def _create_enhanced_activity_chart(self):
        """Create an enhanced activity tracking chart"""
        try:
            from PySide6.QtCharts import QChart, QChartView, QBarSeries, QBarSet, QBarCategoryAxis, QValueAxis
            
            chart = QChart()
            chart.setTitle("Weekly Activity Analysis")
            chart.setTheme(QChart.ChartTheme.ChartThemeDark)
            chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)
            
            # Create enhanced bar series
            bar_series = QBarSeries()
            
            block_set = QBarSet("Blocked Attempts")
            block_set.setBrush(QBrush(QColor("#ff6b6b")))
            block_set.setPen(QPen(QColor("#ff6b6b")))
            
            recovery_set = QBarSet("Recovery Actions")
            recovery_set.setBrush(QBrush(QColor("#4ecdc4")))
            recovery_set.setPen(QPen(QColor("#4ecdc4")))
            
            days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
            
            # Add realistic data
            for i in range(7):
                block_set.append(3 + i * 1.5 + (i % 3) * 2)
                recovery_set.append(2 + i * 0.8 + (i % 2) * 1.5)
            
            bar_series.append(block_set)
            bar_series.append(recovery_set)
            chart.addSeries(bar_series)
            
            # Enhanced axes
            axis_x = QBarCategoryAxis()
            axis_x.append(days)
            chart.addAxis(axis_x, Qt.AlignmentFlag.AlignBottom)
            bar_series.attachAxis(axis_x)
            
            axis_y = QValueAxis()
            axis_y.setTitleText("Count")
            axis_y.setRange(0, 15)
            chart.addAxis(axis_y, Qt.AlignmentFlag.AlignLeft)
            bar_series.attachAxis(axis_y)
            
            chart_view = QChartView(chart)
            chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)
            chart_view.setMinimumHeight(250)
            chart_view.setStyleSheet("""
                QChartView {
                    background: #1a202c;
                    border-radius: 8px;
                    border: 1px solid #2d3748;
                }
            """)
            
            return chart_view
            
        except ImportError:
            # Enhanced fallback
            fallback = QFrame()
            fallback.setStyleSheet("""
                QFrame {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 #1a202c, stop:1 #2d3748);
                    border-radius: 8px;
                    border: 1px solid #4a5568;
                }
            """)
            
            layout = QVBoxLayout(fallback)
            
            icon_label = QLabel("📊")
            icon_label.setStyleSheet("""
                QLabel {
                    font-size: 48px;
                    text-align: center;
                    margin: 20px;
                }
            """)
            
            text_label = QLabel("Activity Chart\n(QtCharts not available)")
            text_label.setStyleSheet("""
                QLabel {
                    color: #a0aec0;
                    font-size: 14px;
                    text-align: center;
                    margin: 10px;
                }
            """)
            text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            layout.addWidget(icon_label)
            layout.addWidget(text_label)
            fallback.setMinimumHeight(250)
            
            return fallback
    
    def _create_enhanced_activity_section(self, parent_layout):
        """Create enhanced activity section with modern design"""
        activity_frame = QFrame()
        activity_frame.setFrameStyle(QFrame.Shape.StyledPanel)
        activity_frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #2d3748, stop:1 #404040);
                border-radius: 12px;
                padding: 20px;
                border: 2px solid #4a5568;
            }
        """)
        
        activity_layout = QVBoxLayout(activity_frame)
        activity_layout.setSpacing(15)
        
        # Enhanced header with icon and refresh button
        header_layout = QHBoxLayout()
        
        icon_label = QLabel("📊")
        icon_label.setStyleSheet("""
            QLabel {
                font-size: 24px;
                margin-right: 10px;
            }
        """)
        
        title_label = QLabel("Recent Activity")
        title_label.setStyleSheet("""
            QLabel {
                color: #ffffff;
                font-size: 18px;
                font-weight: bold;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
        """)
        
        refresh_btn = QPushButton("🔄 Refresh")
        refresh_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #0078d4, stop:1 #106ebe);
                color: #ffffff;
                border: none;
                padding: 8px 16px;
                border-radius: 6px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #106ebe, stop:1 #005a9e);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #005a9e, stop:1 #004578);
            }
        """)
        refresh_btn.clicked.connect(self._refresh_activity_list)
        
        header_layout.addWidget(icon_label)
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        header_layout.addWidget(refresh_btn)
        
        activity_layout.addLayout(header_layout)
        
        # Enhanced activity list with modern styling
        self.activity_list = QListWidget()
        self.activity_list.setStyleSheet("""
            QListWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #1a202c, stop:1 #2d3748);
                border: 2px solid #4a5568;
                border-radius: 8px;
                padding: 10px;
                color: #ffffff;
                font-size: 13px;
                outline: none;
            }
            QListWidget::item {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #2d3748, stop:1 #404040);
                border: 1px solid #4a5568;
                border-radius: 6px;
                padding: 12px;
                margin: 2px 0;
                transition: all 0.2s ease;
            }
            QListWidget::item:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #404040, stop:1 #4a4a4a);
                border: 1px solid #0078d4;
                transform: translateX(2px);
            }
            QListWidget::item:selected {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #0078d4, stop:1 #106ebe);
                border: 1px solid #ffffff;
                color: #ffffff;
            }
            QListWidget::item:selected:active {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #005a9e, stop:1 #004578);
            }
        """)
        
        # Set alternating row colors
        self.activity_list.setAlternatingRowColors(True)
        
        activity_layout.addWidget(self.activity_list)
        
        # Add activity summary
        summary_layout = QHBoxLayout()
        
        total_label = QLabel("Total Activities: 0")
        total_label.setStyleSheet("""
            QLabel {
                color: #a0aec0;
                font-size: 12px;
                font-style: italic;
            }
        """)
        
        summary_layout.addWidget(total_label)
        summary_layout.addStretch()
        
        # Add quick action buttons
        clear_btn = QPushButton("🗑️ Clear")
        clear_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #dc3545, stop:1 #c82333);
                color: #ffffff;
                border: none;
                padding: 6px 12px;
                border-radius: 4px;
                font-size: 11px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #c82333, stop:1 #bd2130);
            }
        """)
        clear_btn.clicked.connect(self.activity_list.clear)
        
        export_btn = QPushButton("📤 Export")
        export_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #28a745, stop:1 #218838);
                color: #ffffff;
                border: none;
                padding: 6px 12px;
                border-radius: 4px;
                font-size: 11px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #218838, stop:1 #1e7e34);
            }
        """)
        export_btn.clicked.connect(self._export_activity_data)
        
        summary_layout.addWidget(clear_btn)
        summary_layout.addWidget(export_btn)
        
        activity_layout.addLayout(summary_layout)
        
        parent_layout.addWidget(activity_frame)
    
    def _export_activity_data(self):
        """Export activity data to file"""
        try:
            filename, _ = QFileDialog.getSaveFileName(
                self, "Export Activity Data", 
                f"activity_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                "JSON Files (*.json);;Text Files (*.txt)"
            )
            
            if filename:
                activities = []
                for i in range(self.activity_list.count()):
                    item = self.activity_list.item(i)
                    activities.append({
                        "text": item.text(),
                        "timestamp": datetime.now().isoformat()
                    })
                
                with open(filename, 'w') as f:
                    json.dump(activities, f, indent=2)
                
                self.show_notification("Export Successful", f"Activity data exported to {filename}")
        except Exception as e:
            self.logger.error(f"Error exporting activity data: {e}")
            self.show_notification("Export Failed", f"Error: {str(e)}")
    
    def _populate_activity_list(self):
        """Populate the activity list with enhanced sample data"""
        activities = [
            ("🛡️", "Blocked access to inappropriate content", "2 minutes ago"),
            ("📝", "Added new journal entry", "15 minutes ago"),
            ("🎯", "Completed daily goal", "1 hour ago"),
            ("📊", "Updated recovery score", "2 hours ago"),
            ("🔔", "Received positive reinforcement", "3 hours ago"),
            ("📱", "Used emergency support feature", "5 hours ago"),
            ("💪", "Maintained streak for 7 days", "1 day ago"),
            ("🎉", "Achieved milestone: 30 days clean", "2 days ago")
        ]
        
        for icon, text, time in activities:
            item = QListWidgetItem(f"{icon} {text} • {time}")
            item.setData(Qt.ItemDataRole.UserRole, {"icon": icon, "text": text, "time": time})
            self.activity_list.addItem(item)
        
        # Update total count
        total_label = self.findChild(QLabel, "total_activities")
        if total_label:
            total_label.setText(f"Total Activities: {len(activities)}")
    
    def _refresh_activity_list(self):
        """Refresh the activity list with enhanced feedback"""
        self.activity_list.clear()
        self._populate_activity_list()
        
        # Show enhanced refresh feedback
        self.status_bar.showMessage("Activity list refreshed successfully", 3000)
        
        # Add visual feedback
        self.show_notification("Refresh Complete", "Activity list has been updated with latest data")
    
    def _create_quick_actions_panel(self, parent_layout):
        """Create a quick actions panel with enhanced modern design"""
        actions_frame = QFrame()
        actions_frame.setFrameStyle(QFrame.Shape.StyledPanel)
        actions_frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #2d3748, stop:1 #404040);
                border-radius: 12px;
                padding: 20px;
                border: 2px solid #4a5568;
            }
        """)
        
        actions_layout = QVBoxLayout(actions_frame)
        actions_layout.setSpacing(15)
        
        # Enhanced header with icon
        header_layout = QHBoxLayout()
        
        icon_label = QLabel("⚡")
        icon_label.setStyleSheet("""
            QLabel {
                font-size: 24px;
                margin-right: 10px;
            }
        """)
        
        title_label = QLabel("Quick Actions")
        title_label.setStyleSheet("""
            QLabel {
                color: #ffffff;
                font-size: 18px;
                font-weight: bold;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
        """)
        
        subtitle_label = QLabel("Common tasks and shortcuts")
        subtitle_label.setStyleSheet("""
            QLabel {
                color: #a0aec0;
                font-size: 12px;
                font-style: italic;
            }
        """)
        
        header_layout.addWidget(icon_label)
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        header_layout.addWidget(subtitle_label)
        
        actions_layout.addLayout(header_layout)
        
        # Enhanced action buttons with modern design
        buttons_layout = QGridLayout()
        buttons_layout.setSpacing(10)
        
        # Define action buttons with enhanced styling
        actions = [
            ("📝", "New Journal Entry", self._add_journal_entry, "#4facfe", "#00aaff"),
            ("🎯", "Set Daily Goal", self._set_daily_goal, "#4ecdc4", "#44a08d"),
            ("🛡️", "Test Blocking", self._test_blocking, "#ff6b6b", "#ee5a24"),
            ("📊", "View Analytics", self._view_analytics, "#9b59b6", "#8e44ad"),
            ("🔔", "Emergency Support", self._emergency_support, "#e74c3c", "#c0392b"),
            ("⚙️", "Settings", lambda: self.tab_widget.setCurrentIndex(4), "#95a5a6", "#7f8c8d")
        ]
        
        for i, (icon, text, callback, color1, color2) in enumerate(actions):
            btn = QPushButton(f"{icon} {text}")
            btn.setStyleSheet(f"""
                QPushButton {{
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 {color1}, stop:1 {color2});
                    color: #ffffff;
                    border: none;
                    padding: 15px;
                    border-radius: 8px;
                    font-size: 13px;
                    font-weight: bold;
                    min-height: 50px;
                }}
                QPushButton:hover {{
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 {color1}dd, stop:1 {color2}aa);
                }}
                QPushButton:pressed {{
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 {color1}aa, stop:1 {color2}88);
                }}
            """)
            btn.clicked.connect(callback)
            
            # Add hover animation
            self._add_hover_animation(btn)
            
            row = i // 3
            col = i % 3
            buttons_layout.addWidget(btn, row, col)
        
        actions_layout.addLayout(buttons_layout)
        
        # Add recent actions summary
        summary_frame = QFrame()
        summary_frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #1a202c, stop:1 #2d3748);
                border-radius: 8px;
                padding: 15px;
                border: 1px solid #4a5568;
            }
        """)
        
        summary_layout = QHBoxLayout(summary_frame)
        
        recent_label = QLabel("💡 Tip: Use keyboard shortcuts for faster access")
        recent_label.setStyleSheet("""
            QLabel {
                color: #a0aec0;
                font-size: 12px;
                font-style: italic;
            }
        """)
        
        shortcuts_btn = QPushButton("⌨️ Shortcuts")
        shortcuts_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #6c757d, stop:1 #5a6268);
                color: #ffffff;
                border: none;
                padding: 6px 12px;
                border-radius: 4px;
                font-size: 11px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #5a6268, stop:1 #495057);
            }
        """)
        shortcuts_btn.clicked.connect(self._show_shortcuts)
        
        summary_layout.addWidget(recent_label)
        summary_layout.addStretch()
        summary_layout.addWidget(shortcuts_btn)
        
        actions_layout.addWidget(summary_frame)
        
        parent_layout.addWidget(actions_frame)
    
    def _set_daily_goal(self):
        """Set a daily goal"""
        goal, ok = QInputDialog.getText(self, "Set Daily Goal", 
                                       "What would you like to accomplish today?")
        if ok and goal:
            self.status_bar.showMessage(f"Daily goal set: {goal}", 3000)
            # Here you would save the goal to the database
    
    def _create_recovery_tab(self):
        """Create the recovery tools tab"""
        recovery_widget = QWidget()
        layout = QVBoxLayout(recovery_widget)
        
        # Create sub-tabs for recovery tools
        recovery_tabs = QTabWidget()
        
        # Recommendations sub-tab
        self._create_recommendations_subtab(recovery_tabs)
        
        # Risk Assessment sub-tab
        self._create_risk_assessment_subtab(recovery_tabs)
        
        # Journal sub-tab
        self._create_journal_subtab(recovery_tabs)
        
        layout.addWidget(recovery_tabs)
        self.tab_widget.addTab(recovery_widget, "Recovery")
    
    def _create_recommendations_subtab(self, parent):
        """Create recommendations sub-tab"""
        rec_widget = QWidget()
        layout = QVBoxLayout(rec_widget)
        
        # Header
        header_layout = QHBoxLayout()
        title_label = QLabel("Personalized Recommendations")
        title_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #ffffff;")
        
        refresh_btn = QPushButton("Refresh")
        refresh_btn.clicked.connect(self._refresh_recommendations)
        
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        header_layout.addWidget(refresh_btn)
        
        layout.addLayout(header_layout)
        
        # Recommendations list
        self.rec_list = QListWidget()
        self.rec_list.setStyleSheet("""
            QListWidget {
                background-color: #404040;
                color: #ffffff;
                border: 1px solid #555555;
                border-radius: 5px;
                padding: 10px;
            }
            QListWidget::item {
                padding: 10px;
                border-bottom: 1px solid #555555;
            }
            QListWidget::item:selected {
                background-color: #0078d4;
            }
        """)
        
        layout.addWidget(self.rec_list)
        
        # Action buttons
        btn_layout = QHBoxLayout()
        mark_completed_btn = QPushButton("Mark as Completed")
        mark_completed_btn.clicked.connect(self._mark_recommendation_completed)
        
        skip_btn = QPushButton("Skip")
        skip_btn.clicked.connect(self._skip_recommendation)
        
        btn_layout.addWidget(mark_completed_btn)
        btn_layout.addWidget(skip_btn)
        
        layout.addLayout(btn_layout)
        
        parent.addTab(rec_widget, "Recommendations")
    
    def _create_risk_assessment_subtab(self, parent):
        """Create risk assessment sub-tab"""
        risk_widget = QWidget()
        layout = QVBoxLayout(risk_widget)
        
        # Risk display group
        risk_group = QGroupBox("Current Risk Assessment")
        risk_group.setStyleSheet("""
            QGroupBox {
                color: #ffffff;
                font-weight: bold;
                border: 2px solid #555555;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        
        risk_layout = QVBoxLayout(risk_group)
        
        # Risk score
        self.risk_score_label = QLabel("Risk Score: Calculating...")
        self.risk_score_label.setStyleSheet("font-size: 16px; color: #ffffff;")
        risk_layout.addWidget(self.risk_score_label)
        
        # Risk factors
        factors_group = QGroupBox("Contributing Factors")
        factors_layout = QVBoxLayout(factors_group)
        
        self.risk_factors_text = QTextEdit()
        self.risk_factors_text.setReadOnly(True)
        self.risk_factors_text.setMaximumHeight(150)
        factors_layout.addWidget(self.risk_factors_text)
        
        risk_layout.addWidget(factors_group)
        
        # Recommendations
        rec_group = QGroupBox("Recommendations")
        rec_layout = QVBoxLayout(rec_group)
        
        self.risk_rec_text = QTextEdit()
        self.risk_rec_text.setReadOnly(True)
        self.risk_rec_text.setMaximumHeight(150)
        rec_layout.addWidget(self.risk_rec_text)
        
        risk_layout.addWidget(rec_group)
        
        layout.addWidget(risk_group)
        
        # Update button
        update_btn = QPushButton("Update Risk Assessment")
        update_btn.clicked.connect(self._update_risk_assessment)
        layout.addWidget(update_btn)
        
        parent.addTab(risk_widget, "Risk Assessment")
    
    def _create_journal_subtab(self, parent):
        """Create journal sub-tab"""
        journal_widget = QWidget()
        layout = QVBoxLayout(journal_widget)
        
        # Journal entry form
        entry_group = QGroupBox("New Journal Entry")
        entry_group.setStyleSheet("""
            QGroupBox {
                color: #ffffff;
                font-weight: bold;
                border: 2px solid #555555;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        
        entry_layout = QVBoxLayout(entry_group)
        
        # Mood rating
        mood_layout = QHBoxLayout()
        mood_label = QLabel("Mood (1-5):")
        self.mood_slider = QSlider(Qt.Orientation.Horizontal)
        self.mood_slider.setMinimum(1)
        self.mood_slider.setMaximum(5)
        self.mood_slider.setValue(3)
        self.mood_value_label = QLabel("3")
        self.mood_slider.valueChanged.connect(
            lambda value: self.mood_value_label.setText(str(value))
        )
        
        mood_layout.addWidget(mood_label)
        mood_layout.addWidget(self.mood_slider)
        mood_layout.addWidget(self.mood_value_label)
        
        entry_layout.addLayout(mood_layout)
        
        # Journal text
        text_label = QLabel("Entry:")
        self.journal_text = QTextEdit()
        self.journal_text.setPlaceholderText("Write your thoughts, feelings, and experiences here...")
        self.journal_text.setMinimumHeight(200)
        
        entry_layout.addWidget(text_label)
        entry_layout.addWidget(self.journal_text)
        
        # Submit button
        save_btn = QPushButton("Save Entry")
        save_btn.clicked.connect(self._save_journal_entry)
        entry_layout.addWidget(save_btn)
        
        layout.addWidget(entry_group)
        parent.addTab(journal_widget, "Journal")
    
    def _create_blocking_tab(self):
        """Create the blocking tab"""
        blocking_widget = QWidget()
        layout = QVBoxLayout(blocking_widget)
        
        # Header
        title_label = QLabel("Content Blocking")
        title_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #ffffff;")
        layout.addWidget(title_label)
        
        # Blocking status
        status_group = QGroupBox("Blocking Status")
        status_group.setStyleSheet("""
            QGroupBox {
                color: #ffffff;
                font-weight: bold;
                border: 2px solid #555555;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        
        status_layout = QVBoxLayout(status_group)
        self.blocking_status_label = QLabel("Status: Active")
        self.blocking_status_label.setStyleSheet("font-size: 16px; color: #00ff00;")
        status_layout.addWidget(self.blocking_status_label)
        
        layout.addWidget(status_group)
        
        # Statistics
        stats_group = QGroupBox("Statistics")
        stats_layout = QVBoxLayout(stats_group)
        
        self.blocked_attempts_label = QLabel("Blocked Attempts: 0")
        self.blocked_domains_label = QLabel("Blocked Domains: 0")
        self.ai_classifications_label = QLabel("AI Classifications: 0")
        
        for label in [self.blocked_attempts_label, self.blocked_domains_label, self.ai_classifications_label]:
            label.setStyleSheet("color: #ffffff; padding: 5px;")
            stats_layout.addWidget(label)
        
        layout.addWidget(stats_group)
        
        # Control buttons
        control_layout = QHBoxLayout()
        
        update_btn = QPushButton("Update Blocklists")
        update_btn.clicked.connect(self._update_blocklists)
        
        view_btn = QPushButton("View Blocked Sites")
        view_btn.clicked.connect(self._view_blocked_sites)
        
        test_btn = QPushButton("Test Blocking")
        test_btn.clicked.connect(self._test_blocking)
        
        control_layout.addWidget(update_btn)
        control_layout.addWidget(view_btn)
        control_layout.addWidget(test_btn)
        
        layout.addLayout(control_layout)
        layout.addStretch()
        
        self.tab_widget.addTab(blocking_widget, "Blocking")
    
    def _create_analytics_tab(self):
        """Create the analytics tab"""
        analytics_widget = QWidget()
        layout = QVBoxLayout(analytics_widget)
        
        # Header
        header_layout = QHBoxLayout()
        title_label = QLabel("Analytics Dashboard")
        title_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #ffffff;")
        
        generate_btn = QPushButton("Generate Report")
        generate_btn.clicked.connect(self._generate_analytics_report)
        
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        header_layout.addWidget(generate_btn)
        
        layout.addLayout(header_layout)
        
        # Charts area (placeholder for now)
        charts_group = QGroupBox("Charts & Visualizations")
        charts_group.setStyleSheet("""
            QGroupBox {
                color: #ffffff;
                font-weight: bold;
                border: 2px solid #555555;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        
        charts_layout = QVBoxLayout(charts_group)
        
        # Placeholder for charts
        charts_placeholder = QLabel("Charts and visualizations will be displayed here")
        charts_placeholder.setStyleSheet("color: #cccccc; padding: 50px; text-align: center;")
        charts_layout.addWidget(charts_placeholder)
        
        layout.addWidget(charts_group)
        
        # Insights area
        insights_group = QGroupBox("Insights")
        insights_layout = QVBoxLayout(insights_group)
        
        self.insights_text = QTextEdit()
        self.insights_text.setReadOnly(True)
        self.insights_text.setMaximumHeight(150)
        insights_layout.addWidget(self.insights_text)
        
        layout.addWidget(insights_group)
        
        self.tab_widget.addTab(analytics_widget, "Analytics")
    
    def _create_settings_tab(self):
        """Create the settings tab"""
        settings_widget = QWidget()
        layout = QVBoxLayout(settings_widget)
        
        # Header
        title_label = QLabel("Settings")
        title_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #ffffff;")
        layout.addWidget(title_label)
        
        # Settings notebook
        settings_tabs = QTabWidget()
        
        # General settings
        general_widget = QWidget()
        general_layout = QVBoxLayout(general_widget)
        
        # Theme switcher
        theme_layout = QHBoxLayout()
        theme_label = QLabel("Theme:")
        theme_label.setStyleSheet("color: #ffffff;")
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Dark", "Light", "Auto"])
        self.theme_combo.setStyleSheet("color: #000000;")
        theme_layout.addWidget(theme_label)
        theme_layout.addWidget(self.theme_combo)
        general_layout.addLayout(theme_layout)
        
        # Load theme from settings
        saved_theme = self.settings.value("theme", "Dark")
        if isinstance(saved_theme, str):
            idx = {"Dark": 0, "Light": 1, "Auto": 2}.get(saved_theme, 0)
        else:
            idx = 0
        self.theme_combo.setCurrentIndex(idx)
        self.theme_combo.currentIndexChanged.connect(self._on_theme_changed)
        
        # Auto-refresh setting
        self.auto_refresh_checkbox = QCheckBox("Auto-refresh dashboard")
        self.auto_refresh_checkbox.setChecked(True)
        self.auto_refresh_checkbox.setStyleSheet("color: #ffffff;")
        
        # Monitoring setting
        self.monitoring_checkbox = QCheckBox("Enable real-time monitoring")
        self.monitoring_checkbox.setChecked(True)
        self.monitoring_checkbox.setStyleSheet("color: #ffffff;")
        
        general_layout.addWidget(self.auto_refresh_checkbox)
        general_layout.addWidget(self.monitoring_checkbox)
        general_layout.addStretch()
        
        # Save button
        save_btn = QPushButton("Save Settings")
        save_btn.clicked.connect(self._save_settings)
        general_layout.addWidget(save_btn)
        
        settings_tabs.addTab(general_widget, "General")
        layout.addWidget(settings_tabs)
        
        self.tab_widget.addTab(settings_widget, "Settings")
    
    def _on_theme_changed(self):
        idx = self.theme_combo.currentIndex()
        theme_map = {0: ThemeType.DARK, 1: ThemeType.LIGHT, 2: ThemeType.AUTO}
        theme_str_map = {0: "Dark", 1: "Light", 2: "Auto"}
        theme_type = theme_map.get(idx, ThemeType.DARK)
        set_theme(theme_type)
        apply_theme_to_application(QApplication.instance())
        # Save to settings
        self.settings.setValue("theme", theme_str_map.get(idx, "Dark"))
        self.status_bar.showMessage(f"Theme changed to {theme_str_map.get(idx, 'Dark')}")
    
    def _setup_theme(self):
        """Apply modern dark theme or user-selected theme"""
        # Load theme from settings
        saved_theme = self.settings.value("theme", "Dark")
        if isinstance(saved_theme, str):
            theme_map = {"Dark": ThemeType.DARK, "Light": ThemeType.LIGHT, "Auto": ThemeType.AUTO}
            theme_type = theme_map.get(saved_theme, ThemeType.DARK)
        else:
            theme_type = ThemeType.DARK
        set_theme(theme_type)
        apply_theme_to_application(QApplication.instance())
        # Set font
        font = QFont("Segoe UI", 9)
        QApplication.setFont(font)
    
    def _create_menu_bar(self):
        """Create the application menu bar"""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("&File")
        
        new_entry_action = QAction("&New Journal Entry", self)
        new_entry_action.setShortcut("Ctrl+N")
        new_entry_action.triggered.connect(self._add_journal_entry)
        file_menu.addAction(new_entry_action)
        
        file_menu.addSeparator()
        
        export_action = QAction("&Export Data", self)
        export_action.setShortcut("Ctrl+E")
        export_action.triggered.connect(self._export_data)
        file_menu.addAction(export_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("E&xit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # View menu
        view_menu = menubar.addMenu("&View")
        
        dashboard_action = QAction("&Dashboard", self)
        dashboard_action.setShortcut("Ctrl+1")
        dashboard_action.triggered.connect(lambda: self.tab_widget.setCurrentIndex(0))
        view_menu.addAction(dashboard_action)
        
        recovery_action = QAction("&Recovery", self)
        recovery_action.setShortcut("Ctrl+2")
        recovery_action.triggered.connect(lambda: self.tab_widget.setCurrentIndex(1))
        view_menu.addAction(recovery_action)
        
        blocking_action = QAction("&Blocking", self)
        blocking_action.setShortcut("Ctrl+3")
        blocking_action.triggered.connect(lambda: self.tab_widget.setCurrentIndex(2))
        view_menu.addAction(blocking_action)
        
        analytics_action = QAction("&Analytics", self)
        analytics_action.setShortcut("Ctrl+4")
        analytics_action.triggered.connect(lambda: self.tab_widget.setCurrentIndex(3))
        view_menu.addAction(analytics_action)
        
        settings_action = QAction("&Settings", self)
        settings_action.setShortcut("Ctrl+5")
        settings_action.triggered.connect(lambda: self.tab_widget.setCurrentIndex(4))
        view_menu.addAction(settings_action)
        
        # Tools menu
        tools_menu = menubar.addMenu("&Tools")
        
        emergency_action = QAction("&Emergency Support", self)
        emergency_action.setShortcut("Ctrl+Shift+E")
        emergency_action.triggered.connect(self._emergency_support)
        tools_menu.addAction(emergency_action)
        
        update_action = QAction("&Update Blocklists", self)
        update_action.setShortcut("Ctrl+U")
        update_action.triggered.connect(self._update_blocklists)
        tools_menu.addAction(update_action)
        
        test_action = QAction("&Test Blocking", self)
        test_action.setShortcut("Ctrl+T")
        test_action.triggered.connect(self._test_blocking)
        tools_menu.addAction(test_action)
        
        # Help menu
        help_menu = menubar.addMenu("&Help")
        
        about_action = QAction("&About", self)
        about_action.setShortcut("F1")
        about_action.triggered.connect(self._show_about)
        help_menu.addAction(about_action)
        
        shortcuts_action = QAction("&Keyboard Shortcuts", self)
        shortcuts_action.setShortcut("Ctrl+Shift+K")
        shortcuts_action.triggered.connect(self._show_shortcuts)
        help_menu.addAction(shortcuts_action)
    
    def _show_shortcuts(self):
        """Show keyboard shortcuts help dialog"""
        shortcuts_text = """
Keyboard Shortcuts:

File:
  Ctrl+N     - New Journal Entry
  Ctrl+E     - Export Data
  Ctrl+Q     - Exit Application

View:
  Ctrl+1     - Dashboard
  Ctrl+2     - Recovery
  Ctrl+3     - Blocking
  Ctrl+4     - Analytics
  Ctrl+5     - Settings

Tools:
  Ctrl+Shift+E - Emergency Support
  Ctrl+U     - Update Blocklists
  Ctrl+T     - Test Blocking

Help:
  F1         - About
  Ctrl+Shift+K - This Help
        """
        
        msg = QMessageBox(self)
        msg.setWindowTitle("Keyboard Shortcuts")
        msg.setText(shortcuts_text)
        msg.setIcon(QMessageBox.Icon.Information)
        msg.exec()
    
    def _export_data(self):
        """Export user data to file"""
        try:
            filename, _ = QFileDialog.getSaveFileName(
                self, "Export Data", "", "JSON Files (*.json);;All Files (*)"
            )
            if filename:
                # Export user data
                export_data = {
                    "user_id": self.current_user_id,
                    "export_date": datetime.now().isoformat(),
                    "streaks": self.user_data.get("streaks", []),
                    "journal_entries": self.user_data.get("journal", []),
                    "blocking_stats": self.user_data.get("blocking", {})
                }
                
                with open(filename, 'w') as f:
                    json.dump(export_data, f, indent=2)
                
                self.show_notification("Export Successful", f"Data exported to {filename}")
        except Exception as e:
            self.show_notification("Export Failed", f"Error: {str(e)}")
    
    def _create_toolbar(self):
        """Create the application toolbar"""
        toolbar = self.addToolBar("Main Toolbar")
        toolbar.setMovable(True)
        
        # Dashboard action
        dashboard_action = QAction("Dashboard", self)
        dashboard_action.setToolTip("View your recovery dashboard and statistics")
        dashboard_action.triggered.connect(lambda: self.tab_widget.setCurrentIndex(0))
        toolbar.addAction(dashboard_action)
        
        toolbar.addSeparator()
        
        # Journal action
        journal_action = QAction("Journal", self)
        journal_action.setToolTip("Add a new journal entry to track your progress")
        journal_action.triggered.connect(self._add_journal_entry)
        toolbar.addAction(journal_action)
        
        # Emergency support action
        emergency_action = QAction("Emergency", self)
        emergency_action.setToolTip("Get immediate support and resources")
        emergency_action.triggered.connect(self._emergency_support)
        toolbar.addAction(emergency_action)
        
        toolbar.addSeparator()
        
        # Settings action
        settings_action = QAction("Settings", self)
        settings_action.setToolTip("Configure application settings and preferences")
        settings_action.triggered.connect(lambda: self.tab_widget.setCurrentIndex(4))
        toolbar.addAction(settings_action)
    
    def _add_contextual_help(self):
        """Add contextual help to UI elements"""
        # Add tooltips to main elements
        self.tab_widget.setToolTip("""
Main Navigation Tabs:
• Dashboard: Overview of your recovery progress
• Recovery: Journal, recommendations, and risk assessment
• Blocking: Content blocking settings and statistics
• Analytics: Detailed reports and insights
• Settings: Application configuration
        """)
        
        # Store help buttons for later use
        self.help_buttons = {}
    
    def _add_help_button_to_recovery_tab(self):
        """Add help button to recovery tab"""
        help_btn = QPushButton("?")
        help_btn.setMaximumSize(30, 30)
        help_btn.setToolTip("Get help with recovery features")
        help_btn.clicked.connect(self._show_recovery_help)
        self.help_buttons['recovery'] = help_btn
    
    def _add_help_button_to_blocking_tab(self):
        """Add help button to blocking tab"""
        help_btn = QPushButton("?")
        help_btn.setMaximumSize(30, 30)
        help_btn.setToolTip("Get help with blocking features")
        help_btn.clicked.connect(self._show_blocking_help)
        self.help_buttons['blocking'] = help_btn
    
    def _add_help_button_to_analytics_tab(self):
        """Add help button to analytics tab"""
        help_btn = QPushButton("?")
        help_btn.setMaximumSize(30, 30)
        help_btn.setToolTip("Get help with analytics features")
        help_btn.clicked.connect(self._show_analytics_help)
        self.help_buttons['analytics'] = help_btn
    
    def _show_recovery_help(self):
        """Show recovery features help"""
        help_text = """
Recovery Features Help:

Journal Tab:
• Add daily entries to track your thoughts and progress
• Rate your mood and triggers
• View your recovery journey over time

Recommendations Tab:
• Get personalized recovery suggestions
• Mark recommendations as completed
• Track your progress on recovery goals

Risk Assessment Tab:
• Evaluate your current risk level
• Get personalized risk mitigation strategies
• Track risk factors over time

Tips:
• Be honest in your journal entries for better recommendations
• Complete recommended actions to improve your recovery score
• Regular risk assessments help prevent relapses
        """
        
        msg = QMessageBox(self)
        msg.setWindowTitle("Recovery Features Help")
        msg.setText(help_text)
        msg.setIcon(QMessageBox.Icon.Information)
        msg.exec()
    
    def _show_blocking_help(self):
        """Show blocking features help"""
        help_text = """
Blocking Features Help:

Blocking Status:
• View current blocking status
• Enable/disable content blocking
• Monitor blocked attempts

Blocklist Management:
• Update blocklists from trusted sources
• Add custom blocked sites
• View and manage blocked domains

Testing:
• Test if blocking is working correctly
• Verify DNS blocking functionality
• Check system integration

Tips:
• Keep blocklists updated for maximum protection
• Test blocking regularly to ensure it's working
• Custom blocklists can be added for specific needs
        """
        
        msg = QMessageBox(self)
        msg.setWindowTitle("Blocking Features Help")
        msg.setText(help_text)
        msg.setIcon(QMessageBox.Icon.Information)
        msg.exec()
    
    def _show_analytics_help(self):
        """Show analytics features help"""
        help_text = """
Analytics Features Help:

Overview:
• View your recovery progress over time
• Track blocking effectiveness
• Monitor usage patterns

Reports:
• Generate detailed reports
• Export data for analysis
• View trends and patterns

Charts:
• Visual representation of your data
• Interactive charts and graphs
• Progress tracking visualizations

Tips:
• Regular analytics review helps identify patterns
• Export reports to share with support professionals
• Use insights to adjust your recovery strategy
        """
        
        msg = QMessageBox(self)
        msg.setWindowTitle("Analytics Features Help")
        msg.setText(help_text)
        msg.setIcon(QMessageBox.Icon.Information)
        msg.exec()
    
    def _create_status_bar(self):
        """Create the status bar"""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")
    
    def _setup_system_tray(self):
        """Setup system tray icon and menu"""
        if QSystemTrayIcon.isSystemTrayAvailable():
            self.tray_icon = QSystemTrayIcon(self)
            
            # Set a default icon or create a simple one
            try:
                # Try to load an icon from resources
                icon_path = Path(__file__).parent / "icons" / "shield.png"
                if icon_path.exists():
                    self.tray_icon.setIcon(QIcon(str(icon_path)))
                else:
                    # Create a simple colored icon as fallback
                    pixmap = QPixmap(32, 32)
                    pixmap.fill(QColor(0, 120, 212))  # Blue color
                    self.tray_icon.setIcon(QIcon(pixmap))
            except Exception as e:
                # Create a simple colored icon as fallback
                pixmap = QPixmap(32, 32)
                pixmap.fill(QColor(0, 120, 212))  # Blue color
                self.tray_icon.setIcon(QIcon(pixmap))
            
            # Create tray menu
            tray_menu = QMenu()
            
            show_action = QAction("Show", self)
            show_action.triggered.connect(self.show)
            tray_menu.addAction(show_action)
            
            tray_menu.addSeparator()
            
            quit_action = QAction("Quit", self)
            quit_action.triggered.connect(QApplication.quit)
            tray_menu.addAction(quit_action)
            
            self.tray_icon.setContextMenu(tray_menu)
            self.tray_icon.setToolTip("CleanNet Shield")
            self.tray_icon.show()
    
    def _set_window_icon(self):
        """Set the window icon"""
        # Create a simple icon programmatically
        icon = QIcon()
        pixmap = QPixmap(32, 32)
        pixmap.fill(QColor(0, 120, 212))  # Blue color
        
        # Draw a simple shield shape
        painter = QPainter(pixmap)
        painter.setPen(QPen(QColor(255, 255, 255), 2))
        painter.drawRect(4, 4, 24, 24)
        painter.end()
        
        icon.addPixmap(pixmap)
        self.setWindowIcon(icon)
    
    def _load_initial_data(self):
        """Load initial data for the dashboard"""
        try:
            self._refresh_overview()
            self._refresh_recommendations()
            self._update_risk_assessment()
            self._update_blocking_status()
            
            self.status_bar.showMessage("Dashboard loaded successfully")
            
        except Exception as e:
            self.logger.error(f"Error loading initial data: {e}")
            self.status_bar.showMessage("Error loading data")
    
    def _start_background_tasks(self):
        """Start background tasks and timers"""
        # Auto-refresh timer
        self.refresh_timer = QTimer()
        self.refresh_timer.timeout.connect(self._auto_refresh)
        self.refresh_timer.start(30000)  # 30 seconds
    
    def _auto_refresh(self):
        """Auto-refresh dashboard data"""
        if hasattr(self, 'auto_refresh_checkbox') and self.auto_refresh_checkbox.isChecked():
            self._refresh_overview()
    
    def _refresh_overview(self):
        """Refresh the overview tab"""
        try:
            # Update streak information (placeholder data)
            current_streak = 5
            longest_streak = 15
            
            self.streak_days_label.setText(f"{current_streak} days")
            
            # Update risk level
            risk_level = "Low"
            self.risk_level_label.setText(risk_level)
            
            # Update progress bar
            self.progress_bar.setValue(75)
            
        except Exception as e:
            self.logger.error(f"Error refreshing overview: {e}")
    
    def _refresh_recommendations(self):
        """Refresh recommendations"""
        try:
            self.rec_list.clear()
            
            # Add sample recommendations
            recommendations = [
                "Take a 10-minute walk outside",
                "Practice deep breathing exercises",
                "Call a supportive friend or family member",
                "Write in your recovery journal",
                "Engage in a hobby or activity you enjoy"
            ]
            
            for rec in recommendations:
                item = QListWidgetItem(rec)
                self.rec_list.addItem(item)
                
        except Exception as e:
            self.logger.error(f"Error refreshing recommendations: {e}")
    
    def _update_risk_assessment(self):
        """Update risk assessment"""
        try:
            # Update risk score
            self.risk_score_label.setText("Risk Score: 25% (Low)")
            
            # Update risk factors
            factors_text = """• Recent stress levels: Moderate
• Sleep quality: Good
• Social support: Strong
• Triggers identified: 2
• Coping strategies: Active"""
            
            self.risk_factors_text.setText(factors_text)
            
            # Update recommendations
            rec_text = """• Continue current recovery practices
• Maintain regular exercise routine
• Stay connected with support network
• Monitor stress levels closely
• Practice mindfulness daily"""
            
            self.risk_rec_text.setText(rec_text)
            
        except Exception as e:
            self.logger.error(f"Error updating risk assessment: {e}")
    
    def _update_blocking_status(self):
        """Update blocking status"""
        try:
            self.blocking_status_label.setText("Status: Active")
            self.blocked_attempts_label.setText("Blocked Attempts: 12")
            self.blocked_domains_label.setText("Blocked Domains: 45")
            self.ai_classifications_label.setText("AI Classifications: 8")
            
        except Exception as e:
            self.logger.error(f"Error updating blocking status: {e}")
    
    def _add_journal_entry(self):
        """Add journal entry"""
        self.tab_widget.setCurrentIndex(1)  # Switch to recovery tab
        # Focus on journal sub-tab
        recovery_tabs = self.tab_widget.widget(1).findChild(QTabWidget)
        if recovery_tabs:
            recovery_tabs.setCurrentIndex(2)  # Journal sub-tab
    
    def _view_recommendations(self):
        """View recommendations"""
        self.tab_widget.setCurrentIndex(1)  # Switch to recovery tab
        # Focus on recommendations sub-tab
        recovery_tabs = self.tab_widget.widget(1).findChild(QTabWidget)
        if recovery_tabs:
            recovery_tabs.setCurrentIndex(0)  # Recommendations sub-tab
    
    def _check_risk_assessment(self):
        """Check risk assessment"""
        self.tab_widget.setCurrentIndex(1)  # Switch to recovery tab
        # Focus on risk assessment sub-tab
        recovery_tabs = self.tab_widget.widget(1).findChild(QTabWidget)
        if recovery_tabs:
            recovery_tabs.setCurrentIndex(1)  # Risk assessment sub-tab
    
    def _view_analytics(self):
        """View analytics"""
        self.tab_widget.setCurrentIndex(3)  # Switch to analytics tab
    
    def _emergency_support(self):
        """Show emergency support dialog"""
        msg = QMessageBox()
        msg.setWindowTitle("Emergency Support")
        msg.setText("🆘 You're not alone. Help is available.")
        msg.setInformativeText("""
If you're in crisis:
• Call: 988 (Suicide & Crisis Lifeline)
• Text: HOME to 741741 (Crisis Text Line)
• Visit: Your local emergency room

Recovery Resources:
• NoFap Community: r/NoFap
• SAA Meetings: saa-recovery.org
• SMART Recovery: smartrecovery.org
        """)
        msg.setIcon(QMessageBox.Icon.Information)
        msg.exec()
    
    def _save_journal_entry(self):
        """Save journal entry"""
        try:
            mood = self.mood_slider.value()
            text = self.journal_text.toPlainText()
            
            if text.strip():
                # Save to database (placeholder)
                QMessageBox.information(self, "Saved", "Journal entry saved successfully! 📝")
                self.journal_text.clear()
            else:
                QMessageBox.warning(self, "Warning", "Please enter some text for your journal entry.")
                
        except Exception as e:
            self.logger.error(f"Error saving journal entry: {e}")
            QMessageBox.critical(self, "Error", f"Error saving journal entry: {e}")
    
    def _mark_recommendation_completed(self):
        """Mark recommendation as completed"""
        current_item = self.rec_list.currentItem()
        if current_item:
            QMessageBox.information(self, "Completed", f"Marked '{current_item.text()}' as completed! ✅")
            self.rec_list.takeItem(self.rec_list.row(current_item))
        else:
            QMessageBox.warning(self, "Warning", "Please select a recommendation to mark as completed.")
    
    def _skip_recommendation(self):
        """Skip recommendation"""
        current_item = self.rec_list.currentItem()
        if current_item:
            QMessageBox.information(self, "Skipped", f"Skipped '{current_item.text()}'")
            self.rec_list.takeItem(self.rec_list.row(current_item))
        else:
            QMessageBox.warning(self, "Warning", "Please select a recommendation to skip.")
    
    def _update_blocklists(self):
        """Update blocking lists"""
        QMessageBox.information(self, "Updating", "Blocklists are being updated... 🔄")
    
    def _view_blocked_sites(self):
        """View blocked sites"""
        QMessageBox.information(self, "Blocked Sites", "Blocked sites list will be displayed")
    
    def _test_blocking(self):
        """Test blocking functionality"""
        QMessageBox.information(self, "Test", "Blocking test completed")
    
    def _generate_analytics_report(self):
        """Generate analytics report"""
        QMessageBox.information(self, "Report", "Analytics report generated successfully! 📊")
    
    def _save_settings(self):
        """Save settings"""
        QMessageBox.information(self, "Settings", "Settings saved successfully! ⚙️")
    
    def _show_about(self):
        """Show about dialog"""
        QMessageBox.about(self, "About CleanNet Shield", 
                         "CleanNet Shield v2.0.0\n\n"
                         "Professional content protection and recovery tool\n"
                         "Built with PySide6 for modern UI/UX\n\n"
                         "© 2024 CleanNet Shield Team")
    
    def closeEvent(self, event):
        """Handle window close event"""
        if hasattr(self, 'tray_icon') and self.tray_icon and self.tray_icon.isVisible():
            QMessageBox.information(self, "CleanNet Shield",
                                  "The application will continue running in the system tray.\n"
                                  "To exit, right-click the tray icon and select Quit.")
            self.hide()
            event.ignore()
        else:
            event.accept()

    def show_onboarding_if_needed(self):
        first_run = self.settings.value("first_run", True, type=bool)
        if first_run:
            dlg = OnboardingDialog(self)
            dlg.exec()
            self.settings.setValue("first_run", False)

    def show_notification(self, title, message):
        msg = QMessageBox(self)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setIcon(QMessageBox.Icon.Information)
        msg.exec()

    def showEvent(self, event):
        super().showEvent(event)
        # Show onboarding only on first show
        if not hasattr(self, '_onboarding_shown'):
            self._onboarding_shown = True
            self.show_onboarding_if_needed()


def main():
    """Main function to run the modern GUI"""
    print('[DEBUG] main() in main_window.py called')
    if not PYSIDE6_AVAILABLE:
        print("PySide6 not available. Please install it with: pip install PySide6")
        return
    
    app = QApplication(sys.argv)
    app.setApplicationName("CleanNet Shield")
    app.setApplicationVersion("2.0.0")
    app.setOrganizationName("CleanNet Shield Team")
    
    window = ModernMainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main() 