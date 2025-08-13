"""
Create a desktop shortcut for the Varroa Detector GUI application.
Run this script once to create a desktop shortcut.
"""

import os
import sys

def create_desktop_shortcut():
    """Create a desktop shortcut for the application"""
    try:
        import winshell
        from win32com.client import Dispatch
        
        desktop = winshell.desktop()
        path = os.path.join(desktop, "Varroa Detector.lnk")
        target = os.path.join(os.getcwd(), "launch_gui.bat")
        wdir = os.getcwd()
        icon = os.path.join(os.getcwd(), "app", "icons", "app_icon.ico")
        
        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(path)
        shortcut.Targetpath = target
        shortcut.WorkingDirectory = wdir
        if os.path.exists(icon):
            shortcut.IconLocation = icon
        shortcut.save()
        
        print(f"Desktop shortcut created: {path}")
        
    except ImportError:
        print("Windows-specific modules not available. Creating manual instructions instead.")
        print("\nTo create a desktop shortcut manually:")
        print("1. Right-click on your desktop")
        print("2. Select 'New' > 'Shortcut'")
        print(f"3. Enter this path: {os.path.join(os.getcwd(), 'launch_gui.bat')}")
        print("4. Name it 'Varroa Detector'")
        print("5. Right-click the shortcut > Properties > Change Icon (optional)")
    
    except Exception as e:
        print(f"Error creating shortcut: {e}")
        print("You can manually double-click 'launch_gui.bat' to start the application")

if __name__ == "__main__":
    create_desktop_shortcut()
    input("Press Enter to continue...")
