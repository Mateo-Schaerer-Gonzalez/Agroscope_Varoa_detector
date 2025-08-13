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
        # Try the modern version first
        from modern_gui_app import main as modern_main
        print("🚀 Starting modern Varroa Detector GUI...")
        modern_main()
    except ImportError as e:
        print(f"Modern GUI not available: {e}")
        try:
            # Fallback to standard version
            from varroa_gui import main as standard_main
            print("Starting standard Varroa Detector GUI...")
            standard_main()
        except ImportError as e2:
            print(f"Error importing GUI applications: {e2}")
            print("Please make sure all required modules are available.")
            input("Press Enter to exit...")
    except Exception as e:
        print(f"Error starting application: {e}")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()
