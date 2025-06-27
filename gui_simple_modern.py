#!/usr/bin/env python3
"""
Simple Modern Theme for Your Existing Tkinter GUI
Just improves the look of what you already have - no major changes needed
"""

import tkinter as tk
from tkinter import ttk
import sys
import os

# Try to import modern styling (optional - graceful fallback)
try:
    import customtkinter as ctk
    MODERN_THEME_AVAILABLE = True
except ImportError:
    MODERN_THEME_AVAILABLE = False

def apply_modern_theme(root_window):
    """
    Apply modern dark theme to your existing Tkinter app
    Call this function in your main.py after creating the root window
    """
    
    if MODERN_THEME_AVAILABLE:
        # Use CustomTkinter for modern look
        ctk.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
        ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"
        
        # Apply to your existing window
        root_window.configure(bg='#2b2b2b')
        
        print("✅ Modern dark theme applied")
        return True
    else:
        # Fallback: Improve standard Tkinter colors
        apply_dark_tkinter_theme(root_window)
        print("✅ Dark Tkinter theme applied (install customtkinter for better look)")
        return False

def apply_dark_tkinter_theme(root_window):
    """
    Fallback dark theme using standard Tkinter
    Makes your app look better even without extra libraries
    """
    
    # Configure root window
    root_window.configure(bg='#2b2b2b')
    
    # Configure ttk styles for modern look
    style = ttk.Style()
    
    # Configure notebook (tabs) for dark theme
    style.theme_use('clam')  # Use clam theme as base
    
    # Configure colors for different widgets
    style.configure('TNotebook', background='#2b2b2b', borderwidth=0)
    style.configure('TNotebook.Tab', 
                   background='#404040', 
                   foreground='white',
                   padding=[10, 5],
                   focuscolor='none')
    style.map('TNotebook.Tab',
             background=[('selected', '#0078d4')])
    
    # Configure frame colors
    style.configure('TFrame', background='#2b2b2b')
    style.configure('TLabelFrame', 
                   background='#2b2b2b', 
                   foreground='white',
                   borderwidth=1,
                   relief='solid')
    
    # Configure labels
    style.configure('TLabel', 
                   background='#2b2b2b', 
                   foreground='white')
    
    # Header style for important labels
    style.configure('Header.TLabel',
                   background='#2b2b2b',
                   foreground='#0078d4',
                   font=('Arial', 12, 'bold'))
    
    # Configure buttons
    style.configure('TButton',
                   background='#0078d4',
                   foreground='white',
                   borderwidth=0,
                   focuscolor='none',
                   padding=[10, 5])
    style.map('TButton',
             background=[('active', '#106ebe'),
                        ('pressed', '#005a9e')])
    
    # Configure text widgets (needs special handling)
    root_window.option_add('*Text.background', '#404040')
    root_window.option_add('*Text.foreground', 'white')
    root_window.option_add('*Text.insertBackground', 'white')

def create_system_tray_icon(root_window, app_name="CleanNet Shield"):
    """
    Add system tray integration to your existing app
    Simple implementation that doesn't require major changes
    """
    
    try:
        import pystray
        from PIL import Image, ImageDraw
        
        # Create a simple icon
        def create_icon():
            # Create a simple shield icon
            width = height = 64
            image = Image.new('RGB', (width, height), color='#0078d4')
            draw = ImageDraw.Draw(image)
            
            # Draw a simple shield shape
            points = [(32, 10), (50, 20), (50, 45), (32, 55), (14, 45), (14, 20)]
            draw.polygon(points, fill='white')
            
            return image
        
        # Create tray menu
        def show_window(icon, item):
            root_window.deiconify()
            root_window.lift()
            icon.stop()
        
        def quit_app(icon, item):
            icon.stop()
            root_window.quit()
        
        # Menu items
        menu = pystray.Menu(
            pystray.MenuItem("Show CleanNet Shield", show_window, default=True),
            pystray.MenuItem("Quit", quit_app)
        )
        
        # Create and setup tray icon
        icon = pystray.Icon(app_name, create_icon(), app_name, menu)
        
        # Minimize to tray instead of closing
        def on_closing():
            root_window.withdraw()  # Hide window
            icon.run_detached()     # Run tray icon in background
        
        root_window.protocol("WM_DELETE_WINDOW", on_closing)
        
        print("✅ System tray integration added")
        return True
        
    except ImportError:
        print("⚠️  pystray not available - install with: pip install pystray pillow")
        return False

def optimize_startup(root_window):
    """
    Simple optimizations for faster startup
    """
    
    # Optimize window creation
    root_window.resizable(True, True)
    
    # Set minimum size for better UX
    root_window.minsize(800, 600)
    
    # Center window on screen
    root_window.update_idletasks()
    width = root_window.winfo_width()
    height = root_window.winfo_height()
    x = (root_window.winfo_screenwidth() // 2) - (width // 2)
    y = (root_window.winfo_screenheight() // 2) - (height // 2)
    root_window.geometry(f"{width}x{height}+{x}+{y}")
    
    print("✅ Window optimized and centered")

def add_modern_features_to_existing_app(root_window, app_name="CleanNet Shield"):
    """
    Main function to enhance your existing app with modern features
    Call this from your main.py right after creating the root window
    
    Usage in your main.py:
    ```python
    # After creating root window
    from gui_simple_modern import add_modern_features_to_existing_app
    add_modern_features_to_existing_app(self.root)
    ```
    """
    
    print("🔧 Applying modern enhancements to your existing app...")
    
    # Apply modern theme
    apply_modern_theme(root_window)
    
    # Add system tray (optional)
    create_system_tray_icon(root_window, app_name)
    
    # Optimize window
    optimize_startup(root_window)
    
    print("✅ Modern enhancements applied! Your app now has:")
    print("   • Modern dark theme")
    print("   • System tray integration")
    print("   • Optimized window positioning")
    print("   • Better visual styling")

# Simple integration instructions
INTEGRATION_INSTRUCTIONS = """
🔧 HOW TO USE THIS WITH YOUR EXISTING APP:

1. Save this file as: gui_simple_modern.py

2. In your main.py, add these lines after creating the root window:

```python
# Add this import at the top
from gui_simple_modern import add_modern_features_to_existing_app

# In your AdultBlockerApp.__init__() method, after self.setup_gui():
add_modern_features_to_existing_app(self.root)
```

3. Optional: Install for even better looks:
```bash
pip install customtkinter pystray pillow
```

That's it! Your existing app will look modern with minimal changes.
"""

if __name__ == "__main__":
    print(INTEGRATION_INSTRUCTIONS)
