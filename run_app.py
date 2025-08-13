#!/usr/bin/env python3
"""
Simple launcher for the Varroa Detector Application
Run this script to start the GUI application.
"""

import sys
import os

# Ensure we can find the app module
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

def main():
    """Launch the application"""
    try:
        from app.launch import main as launch_app
        launch_app()
    except Exception as e:
        print(f"Failed to launch application: {e}")
        print("\nTrying to install dependencies...")
        import subprocess
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
            print("Dependencies installed. Please run the script again.")
        except subprocess.CalledProcessError:
            print("Failed to install dependencies. Please install manually:")
            print("pip install -r requirements.txt")

if __name__ == "__main__":
    main()
