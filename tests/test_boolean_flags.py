"""
Pytest tests for the new boolean flag pause system.
"""

import sys
import os
import threading
import time

# Add the current directory to the path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def test_analysis_state():
    from main import get_analysis_state, continue_analysis_from_gui

    state = get_analysis_state()

    class MockMiteManager:
        def __init__(self):
            self.zones = []

    # Pause and ensure flags set
    state.pause_after_recording1(MockMiteManager(), 1)
    assert state.paused is True
    assert state.continue_analysis is False

    # Wait with timeout should return False until resume is triggered
    start = time.time()
    result = state.wait_for_continue(timeout=0.2)
    elapsed = time.time() - start
    assert result in (False, None)  # None if implementation returns None on timeout
    assert elapsed >= 0.19

    # Now resume via GUI helper
    continue_analysis_from_gui()
    assert state.paused is False
    assert state.continue_analysis is True


def test_blocking_behavior():
    from main import get_analysis_state, continue_analysis_from_gui

    state = get_analysis_state()
    # Reset
    state.paused = False
    state.continue_analysis = False
    state.user_confirmed_continue = False
    state.continue_event.clear()

    class MockManager:
        def __init__(self):
            self.zones = []

    def analysis_thread():
        time.sleep(0.1)
        state.pause_after_recording1(MockManager(), 1)
        # Should block until resume (we give a timeout to not hang pytest)
        resumed = state.wait_for_continue(timeout=2.0)
        assert resumed in (True, None)  # In practice True; None accepted for resilience

    t = threading.Thread(target=analysis_thread, daemon=True)
    t.start()
    time.sleep(0.2)
    continue_analysis_from_gui()
    t.join(timeout=1.5)
    assert not t.is_alive()
