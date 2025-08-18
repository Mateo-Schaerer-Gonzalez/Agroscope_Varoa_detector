#!/usr/bin/env python3
"""
Pytest: smoke test for recording-1 pause support without launching the GUI mainloop.
"""

import pytest
from modern_gui_app import ModernVarroaDetectorApp


@pytest.mark.skip(reason="Interactive GUI mainloop not suitable for CI; covered by integration tests.")
def test_recording1_pause():
    app = ModernVarroaDetectorApp()
    try:
        # Ensure attributes that drive the pause feature exist
        assert hasattr(app, 'recording1_pause') or hasattr(app, 'pause_for_text_verification')
    finally:
        if hasattr(app, 'root'):
            try:
                app.root.destroy()
            except Exception:
                pass
