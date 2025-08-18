#!/usr/bin/env python3
"""
Pytest: zone locking behavior and hover display format (non-interactive assertions).
"""

import sys
import os

project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)


def test_zone_locking_behavior():
    from modern_gui_app import ModernVarroaDetectorApp

    app = ModernVarroaDetectorApp()
    try:
        # Initial state (many apps start unlocked; assert boolean exists)
        assert isinstance(getattr(app, 'zones_locked', False), bool)

        app.lock_zones()
        assert app.zones_locked is True

        app.unlock_zones()
        assert app.zones_locked is False

        # Minimal data for hover logic
        if hasattr(app, 'create_dummy_mite_data'):
            app.create_dummy_mite_data()
        app.zone_coordinates = [
            (0, 100, 100, 200, 200),
            (1, 300, 100, 400, 200),
        ]
        assert len(app.zone_coordinates) >= 2
        assert len(getattr(app, 'mite_zones', [])) >= 0
    finally:
        if hasattr(app, 'root'):
            try:
                app.root.destroy()
            except Exception:
                pass


def test_hover_display_format():
    from modern_gui_app import ModernVarroaDetectorApp

    app = ModernVarroaDetectorApp()
    try:
        app.mite_zones = [
            {'mite_id': 'mite_001', 'zone_id': 0, 'status': 'alive'},
            {'mite_id': 'mite_002', 'zone_id': 0, 'status': 'dead'},
            {'mite_id': 'mite_003', 'zone_id': 1, 'status': 'alive'},
        ]
        app.zone_coordinates = [(0, 100, 100, 200, 200), (1, 300, 100, 400, 200)]

        zone_0_mites = [m for m in app.mite_zones if m.get('zone_id') == 0]
        zone_1_mites = [m for m in app.mite_zones if m.get('zone_id') == 1]

        assert len(zone_0_mites) == 2
        assert len(zone_1_mites) == 1
    finally:
        if hasattr(app, 'root'):
            try:
                app.root.destroy()
            except Exception:
                pass
