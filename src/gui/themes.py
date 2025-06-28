"""
Modern Theme System for CleanNet Shield
Provides dark and light themes with professional styling
"""

from typing import Dict, Any
from enum import Enum

try:
    from PySide6.QtGui import QPalette, QColor
    from PySide6.QtCore import Qt
    PYSIDE6_AVAILABLE = True
except ImportError:
    PYSIDE6_AVAILABLE = False


class ThemeType(Enum):
    """Available theme types"""
    DARK = "dark"
    LIGHT = "light"
    AUTO = "auto"


class ModernTheme:
    """Modern theme system for PySide6 applications"""
    
    def __init__(self, theme_type: ThemeType = ThemeType.DARK):
        self.theme_type = theme_type
        self._setup_colors()
    
    def _setup_colors(self):
        """Setup color schemes for different themes"""
        if self.theme_type == ThemeType.DARK:
            self.colors = self._get_dark_colors()
        elif self.theme_type == ThemeType.LIGHT:
            self.colors = self._get_light_colors()
        else:
            # Auto theme - use dark for now
            self.colors = self._get_dark_colors()
    
    def _get_dark_colors(self) -> Dict[str, str]:
        """Get dark theme colors"""
        return {
            # Primary colors
            "primary": "#0078d4",
            "primary_hover": "#106ebe",
            "primary_pressed": "#005a9e",
            
            # Background colors
            "bg_main": "#2b2b2b",
            "bg_secondary": "#353535",
            "bg_tertiary": "#404040",
            "bg_elevated": "#4a4a4a",
            
            # Text colors
            "text_primary": "#ffffff",
            "text_secondary": "#cccccc",
            "text_muted": "#999999",
            "text_disabled": "#666666",
            
            # Border colors
            "border_primary": "#555555",
            "border_secondary": "#666666",
            "border_focus": "#0078d4",
            
            # Status colors
            "success": "#00ff00",
            "warning": "#ffaa00",
            "error": "#ff6b6b",
            "info": "#00aaff",
            
            # Gradient colors
            "gradient_start": "#2b2b2b",
            "gradient_end": "#404040",
            
            # Special colors
            "accent_blue": "#0078d4",
            "accent_green": "#00ff00",
            "accent_red": "#ff6b6b",
            "accent_yellow": "#ffaa00",
            "accent_purple": "#9b59b6"
        }
    
    def _get_light_colors(self) -> Dict[str, str]:
        """Get light theme colors"""
        return {
            # Primary colors
            "primary": "#0078d4",
            "primary_hover": "#106ebe",
            "primary_pressed": "#005a9e",
            
            # Background colors
            "bg_main": "#ffffff",
            "bg_secondary": "#f5f5f5",
            "bg_tertiary": "#e0e0e0",
            "bg_elevated": "#fafafa",
            
            # Text colors
            "text_primary": "#000000",
            "text_secondary": "#333333",
            "text_muted": "#666666",
            "text_disabled": "#999999",
            
            # Border colors
            "border_primary": "#cccccc",
            "border_secondary": "#dddddd",
            "border_focus": "#0078d4",
            
            # Status colors
            "success": "#28a745",
            "warning": "#ffc107",
            "error": "#dc3545",
            "info": "#17a2b8",
            
            # Gradient colors
            "gradient_start": "#ffffff",
            "gradient_end": "#f5f5f5",
            
            # Special colors
            "accent_blue": "#0078d4",
            "accent_green": "#28a745",
            "accent_red": "#dc3545",
            "accent_yellow": "#ffc107",
            "accent_purple": "#6f42c1"
        }
    
    def get_palette(self) -> QPalette:
        """Get QPalette for the current theme"""
        if not PYSIDE6_AVAILABLE:
            return QPalette()
        
        palette = QPalette()
        
        # Set color roles based on theme
        if self.theme_type == ThemeType.DARK:
            self._apply_dark_palette(palette)
        else:
            self._apply_light_palette(palette)
        
        return palette
    
    def _apply_dark_palette(self, palette: QPalette):
        """Apply dark theme to palette"""
        palette.setColor(QPalette.Window, QColor(self.colors["bg_main"]))
        palette.setColor(QPalette.WindowText, QColor(self.colors["text_primary"]))
        palette.setColor(QPalette.Base, QColor(self.colors["bg_secondary"]))
        palette.setColor(QPalette.AlternateBase, QColor(self.colors["bg_tertiary"]))
        palette.setColor(QPalette.ToolTipBase, QColor(self.colors["bg_elevated"]))
        palette.setColor(QPalette.ToolTipText, QColor(self.colors["text_primary"]))
        palette.setColor(QPalette.Text, QColor(self.colors["text_primary"]))
        palette.setColor(QPalette.Button, QColor(self.colors["bg_tertiary"]))
        palette.setColor(QPalette.ButtonText, QColor(self.colors["text_primary"]))
        palette.setColor(QPalette.BrightText, QColor(self.colors["accent_red"]))
        palette.setColor(QPalette.Link, QColor(self.colors["accent_blue"]))
        palette.setColor(QPalette.Highlight, QColor(self.colors["primary"]))
        palette.setColor(QPalette.HighlightedText, QColor(self.colors["text_primary"]))
    
    def _apply_light_palette(self, palette: QPalette):
        """Apply light theme to palette"""
        palette.setColor(QPalette.Window, QColor(self.colors["bg_main"]))
        palette.setColor(QPalette.WindowText, QColor(self.colors["text_primary"]))
        palette.setColor(QPalette.Base, QColor(self.colors["bg_secondary"]))
        palette.setColor(QPalette.AlternateBase, QColor(self.colors["bg_tertiary"]))
        palette.setColor(QPalette.ToolTipBase, QColor(self.colors["bg_elevated"]))
        palette.setColor(QPalette.ToolTipText, QColor(self.colors["text_primary"]))
        palette.setColor(QPalette.Text, QColor(self.colors["text_primary"]))
        palette.setColor(QPalette.Button, QColor(self.colors["bg_tertiary"]))
        palette.setColor(QPalette.ButtonText, QColor(self.colors["text_primary"]))
        palette.setColor(QPalette.BrightText, QColor(self.colors["accent_red"]))
        palette.setColor(QPalette.Link, QColor(self.colors["accent_blue"]))
        palette.setColor(QPalette.Highlight, QColor(self.colors["primary"]))
        palette.setColor(QPalette.HighlightedText, QColor(self.colors["text_primary"]))
    
    def get_stylesheet(self) -> str:
        """Get stylesheet for the current theme"""
        if self.theme_type == ThemeType.DARK:
            return self._get_dark_stylesheet()
        else:
            return self._get_light_stylesheet()
    
    def _get_dark_stylesheet(self) -> str:
        """Get dark theme stylesheet"""
        return f"""
        /* Main Window */
        QMainWindow {{
            background-color: {self.colors["bg_main"]};
            color: {self.colors["text_primary"]};
            font-family: 'Segoe UI', Arial, sans-serif;
        }}
        
        /* Tab Widget */
        QTabWidget::pane {{
            border: 1px solid {self.colors["border_primary"]};
            background-color: {self.colors["bg_secondary"]};
            border-radius: 5px;
        }}
        
        QTabBar::tab {{
            background-color: {self.colors["bg_main"]};
            color: {self.colors["text_primary"]};
            padding: 10px 20px;
            margin: 2px;
            border-radius: 5px;
            font-weight: bold;
        }}
        
        QTabBar::tab:selected {{
            background-color: {self.colors["primary"]};
        }}
        
        QTabBar::tab:hover {{
            background-color: {self.colors["bg_tertiary"]};
        }}
        
        /* Buttons */
        QPushButton {{
            background-color: {self.colors["primary"]};
            color: {self.colors["text_primary"]};
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            font-weight: bold;
        }}
        
        QPushButton:hover {{
            background-color: {self.colors["primary_hover"]};
        }}
        
        QPushButton:pressed {{
            background-color: {self.colors["primary_pressed"]};
        }}
        
        QPushButton:disabled {{
            background-color: {self.colors["bg_tertiary"]};
            color: {self.colors["text_disabled"]};
        }}
        
        /* Progress Bar */
        QProgressBar {{
            border: 2px solid {self.colors["border_primary"]};
            border-radius: 5px;
            text-align: center;
            background-color: {self.colors["bg_tertiary"]};
        }}
        
        QProgressBar::chunk {{
            background-color: {self.colors["primary"]};
            border-radius: 3px;
        }}
        
        /* Labels */
        QLabel {{
            color: {self.colors["text_primary"]};
        }}
        
        /* Text Edit */
        QTextEdit {{
            background-color: {self.colors["bg_tertiary"]};
            color: {self.colors["text_primary"]};
            border: 1px solid {self.colors["border_primary"]};
            border-radius: 5px;
            padding: 10px;
        }}
        
        /* Group Box */
        QGroupBox {{
            font-weight: bold;
            border: 2px solid {self.colors["border_primary"]};
            border-radius: 5px;
            margin-top: 10px;
            padding-top: 10px;
            color: {self.colors["text_primary"]};
        }}
        
        QGroupBox::title {{
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 5px 0 5px;
        }}
        
        /* List Widget */
        QListWidget {{
            background-color: {self.colors["bg_tertiary"]};
            color: {self.colors["text_primary"]};
            border: 1px solid {self.colors["border_primary"]};
            border-radius: 5px;
            padding: 10px;
        }}
        
        QListWidget::item {{
            padding: 10px;
            border-bottom: 1px solid {self.colors["border_primary"]};
        }}
        
        QListWidget::item:selected {{
            background-color: {self.colors["primary"]};
        }}
        
        /* Check Box */
        QCheckBox {{
            color: {self.colors["text_primary"]};
        }}
        
        QCheckBox::indicator {{
            width: 18px;
            height: 18px;
            border: 2px solid {self.colors["border_primary"]};
            border-radius: 3px;
            background-color: {self.colors["bg_tertiary"]};
        }}
        
        QCheckBox::indicator:checked {{
            background-color: {self.colors["primary"]};
            border-color: {self.colors["primary"]};
        }}
        
        /* Slider */
        QSlider::groove:horizontal {{
            border: 1px solid {self.colors["border_primary"]};
            height: 8px;
            background: {self.colors["bg_tertiary"]};
            border-radius: 4px;
        }}
        
        QSlider::handle:horizontal {{
            background: {self.colors["primary"]};
            border: 1px solid {self.colors["primary"]};
            width: 18px;
            margin: -2px 0;
            border-radius: 9px;
        }}
        
        /* Status Bar */
        QStatusBar {{
            background-color: {self.colors["bg_secondary"]};
            color: {self.colors["text_primary"]};
            border-top: 1px solid {self.colors["border_primary"]};
        }}
        
        /* Menu Bar */
        QMenuBar {{
            background-color: {self.colors["bg_main"]};
            color: {self.colors["text_primary"]};
            border-bottom: 1px solid {self.colors["border_primary"]};
        }}
        
        QMenuBar::item {{
            background-color: transparent;
            padding: 8px 12px;
        }}
        
        QMenuBar::item:selected {{
            background-color: {self.colors["bg_tertiary"]};
        }}
        
        /* Menu */
        QMenu {{
            background-color: {self.colors["bg_secondary"]};
            color: {self.colors["text_primary"]};
            border: 1px solid {self.colors["border_primary"]};
            padding: 5px;
        }}
        
        QMenu::item {{
            padding: 8px 20px;
        }}
        
        QMenu::item:selected {{
            background-color: {self.colors["primary"]};
        }}
        
        /* Tool Bar */
        QToolBar {{
            background-color: {self.colors["bg_main"]};
            border: none;
            spacing: 3px;
        }}
        
        QToolBar::separator {{
            background-color: {self.colors["border_primary"]};
            width: 1px;
            margin: 0 5px;
        }}
        
        /* Scroll Bar */
        QScrollBar:vertical {{
            background-color: {self.colors["bg_tertiary"]};
            width: 12px;
            border-radius: 6px;
        }}
        
        QScrollBar::handle:vertical {{
            background-color: {self.colors["border_primary"]};
            border-radius: 6px;
            min-height: 20px;
        }}
        
        QScrollBar::handle:vertical:hover {{
            background-color: {self.colors["border_secondary"]};
        }}
        """
    
    def _get_light_stylesheet(self) -> str:
        """Get light theme stylesheet"""
        return f"""
        /* Main Window */
        QMainWindow {{
            background-color: {self.colors["bg_main"]};
            color: {self.colors["text_primary"]};
            font-family: 'Segoe UI', Arial, sans-serif;
        }}
        
        /* Tab Widget */
        QTabWidget::pane {{
            border: 1px solid {self.colors["border_primary"]};
            background-color: {self.colors["bg_secondary"]};
            border-radius: 5px;
        }}
        
        QTabBar::tab {{
            background-color: {self.colors["bg_tertiary"]};
            color: {self.colors["text_primary"]};
            padding: 10px 20px;
            margin: 2px;
            border-radius: 5px;
            font-weight: bold;
        }}
        
        QTabBar::tab:selected {{
            background-color: {self.colors["primary"]};
            color: white;
        }}
        
        QTabBar::tab:hover {{
            background-color: {self.colors["border_secondary"]};
        }}
        
        /* Buttons */
        QPushButton {{
            background-color: {self.colors["primary"]};
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            font-weight: bold;
        }}
        
        QPushButton:hover {{
            background-color: {self.colors["primary_hover"]};
        }}
        
        QPushButton:pressed {{
            background-color: {self.colors["primary_pressed"]};
        }}
        
        QPushButton:disabled {{
            background-color: {self.colors["bg_tertiary"]};
            color: {self.colors["text_disabled"]};
        }}
        
        /* Progress Bar */
        QProgressBar {{
            border: 2px solid {self.colors["border_primary"]};
            border-radius: 5px;
            text-align: center;
            background-color: {self.colors["bg_secondary"]};
        }}
        
        QProgressBar::chunk {{
            background-color: {self.colors["primary"]};
            border-radius: 3px;
        }}
        
        /* Labels */
        QLabel {{
            color: {self.colors["text_primary"]};
        }}
        
        /* Text Edit */
        QTextEdit {{
            background-color: white;
            color: {self.colors["text_primary"]};
            border: 1px solid {self.colors["border_primary"]};
            border-radius: 5px;
            padding: 10px;
        }}
        
        /* Group Box */
        QGroupBox {{
            font-weight: bold;
            border: 2px solid {self.colors["border_primary"]};
            border-radius: 5px;
            margin-top: 10px;
            padding-top: 10px;
            color: {self.colors["text_primary"]};
        }}
        
        QGroupBox::title {{
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 5px 0 5px;
        }}
        
        /* List Widget */
        QListWidget {{
            background-color: white;
            color: {self.colors["text_primary"]};
            border: 1px solid {self.colors["border_primary"]};
            border-radius: 5px;
            padding: 10px;
        }}
        
        QListWidget::item {{
            padding: 10px;
            border-bottom: 1px solid {self.colors["border_secondary"]};
        }}
        
        QListWidget::item:selected {{
            background-color: {self.colors["primary"]};
            color: white;
        }}
        
        /* Check Box */
        QCheckBox {{
            color: {self.colors["text_primary"]};
        }}
        
        QCheckBox::indicator {{
            width: 18px;
            height: 18px;
            border: 2px solid {self.colors["border_primary"]};
            border-radius: 3px;
            background-color: white;
        }}
        
        QCheckBox::indicator:checked {{
            background-color: {self.colors["primary"]};
            border-color: {self.colors["primary"]};
        }}
        
        /* Slider */
        QSlider::groove:horizontal {{
            border: 1px solid {self.colors["border_primary"]};
            height: 8px;
            background: {self.colors["bg_secondary"]};
            border-radius: 4px;
        }}
        
        QSlider::handle:horizontal {{
            background: {self.colors["primary"]};
            border: 1px solid {self.colors["primary"]};
            width: 18px;
            margin: -2px 0;
            border-radius: 9px;
        }}
        
        /* Status Bar */
        QStatusBar {{
            background-color: {self.colors["bg_secondary"]};
            color: {self.colors["text_primary"]};
            border-top: 1px solid {self.colors["border_primary"]};
        }}
        
        /* Menu Bar */
        QMenuBar {{
            background-color: {self.colors["bg_main"]};
            color: {self.colors["text_primary"]};
            border-bottom: 1px solid {self.colors["border_primary"]};
        }}
        
        QMenuBar::item {{
            background-color: transparent;
            padding: 8px 12px;
        }}
        
        QMenuBar::item:selected {{
            background-color: {self.colors["bg_tertiary"]};
        }}
        
        /* Menu */
        QMenu {{
            background-color: white;
            color: {self.colors["text_primary"]};
            border: 1px solid {self.colors["border_primary"]};
            padding: 5px;
        }}
        
        QMenu::item {{
            padding: 8px 20px;
        }}
        
        QMenu::item:selected {{
            background-color: {self.colors["primary"]};
            color: white;
        }}
        
        /* Tool Bar */
        QToolBar {{
            background-color: {self.colors["bg_main"]};
            border: none;
            spacing: 3px;
        }}
        
        QToolBar::separator {{
            background-color: {self.colors["border_primary"]};
            width: 1px;
            margin: 0 5px;
        }}
        
        /* Scroll Bar */
        QScrollBar:vertical {{
            background-color: {self.colors["bg_secondary"]};
            width: 12px;
            border-radius: 6px;
        }}
        
        QScrollBar::handle:vertical {{
            background-color: {self.colors["border_primary"]};
            border-radius: 6px;
            min-height: 20px;
        }}
        
        QScrollBar::handle:vertical:hover {{
            background-color: {self.colors["border_secondary"]};
        }}
        """
    
    def get_color(self, color_name: str) -> str:
        """Get a specific color by name"""
        return self.colors.get(color_name, "#000000")
    
    def set_theme(self, theme_type: ThemeType):
        """Change the current theme"""
        self.theme_type = theme_type
        self._setup_colors()


# Global theme instance
current_theme = ModernTheme(ThemeType.DARK)


def get_current_theme() -> ModernTheme:
    """Get the current theme instance"""
    return current_theme


def set_theme(theme_type: ThemeType):
    """Set the global theme"""
    global current_theme
    current_theme = ModernTheme(theme_type)


def apply_theme_to_application(app):
    """Apply the current theme to a QApplication"""
    if not PYSIDE6_AVAILABLE:
        return
    
    theme = get_current_theme()
    
    # Apply palette
    app.setPalette(theme.get_palette())
    
    # Apply stylesheet
    app.setStyleSheet(theme.get_stylesheet())
    
    # Set application style
    app.setStyle("Fusion")
    
    # Set font
    from PySide6.QtGui import QFont
    font = QFont("Segoe UI", 9)
    app.setFont(font) 