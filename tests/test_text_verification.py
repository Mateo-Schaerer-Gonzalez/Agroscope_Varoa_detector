#!/usr/bin/env python3
"""
Test script for the enhanced text verification functionality
"""

import tkinter as tk
from modern_gui_app import ModernVarroaDetectorApp

def test_text_verification():
    """Test the text verification functionality"""
    try:
        print("🚀 Starting Varroa Detector with enhanced text verification...")
        
        # Create and run the application
        app = ModernVarroaDetectorApp()
        
        print("✅ Application initialized successfully")
        print("📝 New text verification features:")
        print("   - Click zones to select/deselect them")
        print("   - Edit zone IDs inline on the right panel")
        print("   - Use 'Verify All Texts' button to pause analysis")
        print("   - Selected zones are highlighted in bright magenta")
        
        # Start the GUI main loop
        app.root.mainloop()
        
    except Exception as e:
        print(f"❌ Error starting application: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_text_verification()
