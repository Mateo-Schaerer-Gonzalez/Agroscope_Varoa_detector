#!/usr/bin/env python3
"""
Pytest: verify the application starts and exposes the expected callbacks.
"""

import sys
import os

# Add the project root to the Python path (kept for robustness when running tests directly)
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)


def test_app_startup():
    from modern_gui_app import ModernVarroaDetectorApp

    app = ModernVarroaDetectorApp()
    try:
        assert hasattr(app, 'analysis_complete_flag') and isinstance(app.analysis_complete_flag, bool)
        assert hasattr(app, 'analysis_completed') and callable(app.analysis_completed)
    finally:
        # Ensure GUI resources are cleaned up
        if hasattr(app, 'root'):
            try:
                app.root.destroy()
            except Exception:
                pass
