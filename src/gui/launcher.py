"""
Modern GUI Launcher for CleanNet Shield
Handles PySide6 and Tkinter fallback
"""

import sys
import os
from pathlib import Path
from typing import Optional
import traceback

print(f"[DEBUG] sys.executable: {sys.executable}")
print(f"[DEBUG] sys.path: {sys.path}")

def check_pyside6_availability() -> bool:
    """Check if PySide6 is available"""
    try:
        import PySide6
        return True
    except ImportError:
        return False

def check_customtkinter_availability() -> bool:
    """Check if customtkinter is available"""
    try:
        import customtkinter
        return True
    except ImportError:
        return False

def launch_modern_gui():
    """Launch the modern GUI with PySide6"""
    try:
        from .main_window import main
        main()
    except Exception as e:
        print(f"Error launching modern GUI: {e}")
        traceback.print_exc()
        return False
    return True

def launch_legacy_gui():
    """Launch the legacy GUI with Tkinter"""
    try:
        from .advanced_dashboard import main
        main()
    except Exception as e:
        print(f"Error launching legacy GUI: {e}")
        return False
    return True

def launch_fallback_gui():
    """Launch a simple fallback GUI"""
    try:
        import tkinter as tk
        from tkinter import messagebox
        
        root = tk.Tk()
        root.title("CleanNet Shield - Fallback Mode")
        root.geometry("400x300")
        
        # Simple message
        message = tk.Label(root, text="CleanNet Shield", font=("Arial", 16, "bold"))
        message.pack(pady=20)
        
        info = tk.Label(root, text="Running in fallback mode.\nPlease install PySide6 for the full experience.")
        info.pack(pady=10)
        
        # Install button
        def install_pyside6():
            import subprocess
            try:
                subprocess.run([sys.executable, "-m", "pip", "install", "PySide6"], check=True)
                messagebox.showinfo("Success", "PySide6 installed successfully!\nPlease restart the application.")
                root.destroy()
            except subprocess.CalledProcessError:
                messagebox.showerror("Error", "Failed to install PySide6. Please install manually:\npip install PySide6")
        
        install_btn = tk.Button(root, text="Install PySide6", command=install_pyside6)
        install_btn.pack(pady=10)
        
        # Continue button
        def continue_fallback():
            messagebox.showinfo("Info", "Continuing with basic functionality...")
            root.destroy()
        
        continue_btn = tk.Button(root, text="Continue with Basic Mode", command=continue_fallback)
        continue_btn.pack(pady=10)
        
        root.mainloop()
        
    except Exception as e:
        print(f"Error launching fallback GUI: {e}")
        return False
    return True

def main():
    """Main launcher function"""
    print("🚀 CleanNet Shield - GUI Launcher")
    print("=" * 40)
    
    # Check available GUI frameworks
    pyside6_available = check_pyside6_availability()
    customtkinter_available = check_customtkinter_availability()
    
    print(f"PySide6 available: {'✅' if pyside6_available else '❌'}")
    print(f"CustomTkinter available: {'✅' if customtkinter_available else '❌'}")
    print()
    
    # Try to launch the best available GUI
    if pyside6_available:
        print("🎨 Launching modern PySide6 GUI...")
        if launch_modern_gui():
            return
        else:
            print("⚠️ Modern GUI failed, trying legacy...")
    
    # Try legacy GUI
    print("🔄 Launching legacy Tkinter GUI...")
    if launch_legacy_gui():
        return
    
    # Fallback to simple GUI
    print("🛟 Launching fallback GUI...")
    if launch_fallback_gui():
        return
    
    # Last resort
    print("❌ All GUI options failed. Please check your installation.")
    print("\nTo install PySide6:")
    print("pip install PySide6")
    print("\nTo install CustomTkinter:")
    print("pip install customtkinter")

if __name__ == "__main__":
    main() 