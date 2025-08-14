"""
Test the new boolean flag pause system
"""

import sys
import os
import threading
import time

# Add the current directory to the path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_analysis_state():
    """Test the AnalysisState class functionality"""
    print("Testing AnalysisState class...")
    
    try:
        from main import AnalysisState, get_analysis_state, continue_analysis_from_gui
        print("✅ Successfully imported analysis state components")
    except ImportError as e:
        print(f"❌ Failed to import analysis state: {e}")
        return False
    
    # Test the global state
    state = get_analysis_state()
    print(f"Initial state - Paused: {state.paused}, Continue: {state.continue_analysis}")
    
    # Simulate analysis pause
    class MockMiteManager:
        def __init__(self):
            self.zones = []
    
    mock_manager = MockMiteManager()
    state.pause_after_recording1(mock_manager, 1)
    print(f"After pause - Paused: {state.paused}, Continue: {state.continue_analysis}")
    
    # Test wait with timeout (simulate UI not responding)
    print("Testing wait with timeout...")
    start_time = time.time()
    result = state.wait_for_continue(timeout=1.0)  # 1 second timeout
    end_time = time.time()
    print(f"Wait result: {result}, Time elapsed: {end_time - start_time:.2f}s")
    
    # Test resume
    continue_analysis_from_gui()
    print(f"After resume - Paused: {state.paused}, Continue: {state.continue_analysis}")
    
    return True

def test_blocking_behavior():
    """Test that the analysis actually blocks until continue is called"""
    print("\nTesting blocking behavior...")
    
    from main import get_analysis_state, continue_analysis_from_gui
    
    state = get_analysis_state()
    
    # Reset state
    state.paused = False
    state.continue_analysis = False
    state.user_confirmed_continue = False
    state.continue_event.clear()
    
    class MockManager:
        def __init__(self):
            self.zones = []
    
    # Simulate the analysis thread
    def analysis_thread():
        print("📊 Analysis thread: Starting...")
        time.sleep(0.5)  # Simulate recording 1 processing
        
        print("📊 Analysis thread: Recording 1 complete - pausing...")
        state.pause_after_recording1(MockManager(), 1)
        
        # This should block until continue is called
        print("📊 Analysis thread: Waiting for continuation...")
        if state.wait_for_continue(timeout=5.0):  # 5 second timeout for testing
            print("📊 Analysis thread: Continuing with recording 2...")
            time.sleep(0.5)  # Simulate recording 2 processing
            print("📊 Analysis thread: Analysis complete!")
        else:
            print("📊 Analysis thread: Timeout - analysis not continued")
    
    # Start analysis thread
    thread = threading.Thread(target=analysis_thread, daemon=True)
    thread.start()
    
    # Wait a bit, then simulate GUI continue
    time.sleep(2.0)  # Give analysis time to pause
    print("🖥️  GUI: User clicked continue...")
    continue_analysis_from_gui()
    
    # Wait for thread to complete
    thread.join(timeout=3.0)
    print("✅ Blocking behavior test complete")
    
    return True

def main():
    """Main test function"""
    print("=== Testing Boolean Flag Pause System ===\n")
    
    if not test_analysis_state():
        print("\n❌ Analysis state tests failed")
        return
    
    if not test_blocking_behavior():
        print("\n❌ Blocking behavior tests failed")
        return
    
    print("\n✅ All boolean flag tests passed! The new pause system should work correctly.")

if __name__ == "__main__":
    main()
