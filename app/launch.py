#!/usr/bin/env python3
"""
Launch script for the Varroa Detector Application
"""

import sys
import os

# Add the project root to Python path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

def main():
    """Launch the Varroa Detector application"""
    try:
        from app.main_window import VarroaDetectorApp
        app = VarroaDetectorApp()
        app.run()
    except ImportError as e:
        print(f"Error importing dependencies: {e}")
        print("Please install required packages:")
        print("pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"Error launching application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
