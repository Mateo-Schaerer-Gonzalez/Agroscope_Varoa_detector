"""
Simple launcher script for the Varroa Detector GUI application.
This script ensures the application runs in the correct environment.
"""

import sys
import os

# Add the project root to the Python path
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

def main():
    """Launch the Varroa Detector GUI application"""
    try:
        from varroa_gui import main as gui_main
        gui_main()
    except ImportError as e:
        print(f"Error importing GUI application: {e}")
        print("Please make sure all required modules are available.")
        input("Press Enter to exit...")
    except Exception as e:
        print(f"Error starting application: {e}")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()
