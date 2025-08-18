"""
Pytest: verify pause integration (imports and pause callback flow).
"""

import sys
import os
import threading
import time

# Add the current directory to the path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def test_imports():
    from main import predict, reanalyze_recording, continue_reanalyze_from_recording2
    from modern_gui_app import ModernVarroaDetectorApp
    # Basic smoke assertions that imports give us callables/classes
    assert callable(predict)
    assert callable(reanalyze_recording)
    assert callable(continue_reanalyze_from_recording2)
    assert ModernVarroaDetectorApp is not None


def test_pause_callback():
    class MockMiteManager:
        def __init__(self):
            self.zones = []

    class MockGUI:
        def __init__(self):
            self.recording1_pause = False
            self.analysis_paused = False
            self.continue_event = None
            self.mite_manager = None

        def update_progress(self, value, message):
            pass

        def setup_recording1_pause(self):
            self.recording1_pause = True
            self.analysis_paused = True

        def pause_for_text_verification(self, mite_manager_instance):
            self.mite_manager = mite_manager_instance
            self.update_progress(60, "paused")
            self.setup_recording1_pause()
            self.continue_event = threading.Event()
            # wait a bit for test to set it
            self.continue_event.wait(timeout=1.0)
            return True

    gui = MockGUI()
    mock_mite_manager = MockMiteManager()

    def run_callback():
        return gui.pause_for_text_verification(mock_mite_manager)

    t = threading.Thread(target=run_callback, daemon=True)
    t.start()
    time.sleep(0.2)
    assert gui.continue_event is not None
    gui.continue_event.set()
    t.join(timeout=1.5)
    assert not t.is_alive()
