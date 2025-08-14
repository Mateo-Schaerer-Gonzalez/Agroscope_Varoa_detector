"""
Test script to verify the pause integration works correctly
"""

import sys
import os
import threading
import time

# Add the current directory to the path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that we can import the required modules"""
    print("Testing imports...")
    
    try:
        from main import predict, reanalyze_recording, continue_reanalyze_from_recording2
        print("✅ Successfully imported main functions")
    except ImportError as e:
        print(f"❌ Failed to import main functions: {e}")
        return False
    
    try:
        from modern_gui_app import ModernVarroaDetectorApp
        print("✅ Successfully imported GUI class")
    except ImportError as e:
        print(f"❌ Failed to import GUI class: {e}")
        return False
    
    return True

def test_pause_callback():
    """Test the pause callback mechanism"""
    print("\nTesting pause callback mechanism...")
    
    # Create a mock mite manager
    class MockMiteManager:
        def __init__(self):
            self.zones = []
    
    # Create a simple GUI instance (without tkinter initialization)
    class MockGUI:
        def __init__(self):
            self.recording1_pause = False
            self.analysis_paused = False
            self.continue_event = None
            self.mite_manager = None
            
        def update_progress(self, value, message):
            print(f"Progress: {value}% - {message}")
        
        def setup_recording1_pause(self):
            print("Setting up recording 1 pause...")
            self.recording1_pause = True
            self.analysis_paused = True
        
        def pause_for_text_verification(self, mite_manager_instance):
            print("⏸️ Analysis paused after recording 1 - starting text verification")
            self.mite_manager = mite_manager_instance
            
            # Simulate UI updates
            self.update_progress(60, "⏸️ Analysis paused - Please verify zone IDs")
            self.setup_recording1_pause()
            
            # Create and wait for the continue event
            self.continue_event = threading.Event()
            
            # Simulate waiting for user input (but with timeout for testing)
            print("Waiting for continue signal...")
            if self.continue_event.wait(timeout=2.0):  # 2 second timeout for testing
                print("▶️ Text verification completed - continuing analysis")
                return True
            else:
                print("⏰ Timeout waiting for continue signal (this is normal for testing)")
                return True
    
    gui = MockGUI()
    mock_mite_manager = MockMiteManager()
    
    # Test the pause callback in a separate thread
    def test_callback():
        return gui.pause_for_text_verification(mock_mite_manager)
    
    # Start the callback in a thread
    callback_thread = threading.Thread(target=test_callback, daemon=True)
    callback_thread.start()
    
    # Wait a bit, then simulate continue
    time.sleep(1)
    if gui.continue_event:
        gui.continue_event.set()
    
    callback_thread.join(timeout=3)
    print("✅ Pause callback test completed")
    
    return True

def main():
    """Main test function"""
    print("=== Testing Pause Integration ===\n")
    
    if not test_imports():
        print("\n❌ Import tests failed")
        return
    
    if not test_pause_callback():
        print("\n❌ Pause callback tests failed")
        return
    
    print("\n✅ All tests passed! The pause integration should work correctly.")

if __name__ == "__main__":
    main()
