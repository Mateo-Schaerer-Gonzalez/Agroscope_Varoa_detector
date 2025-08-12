import sys
import os
import numpy as np
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from classes.mite import Mite
from classes.Rect import MiteZone, TextZone

class DummyFrames:
    """Creates dummy frames as a 4D numpy array (N, H, W, C)."""
    def __init__(self, num_frames=5, height=100, width=100, channels=3):
        self.frames = np.zeros((num_frames, height, width, channels), dtype=np.uint8)
    def __getitem__(self, idx):
        return self.frames[idx]
    def __len__(self):
        return self.frames.shape[0]
    @property
    def shape(self):
        return self.frames.shape

def test_mite_inside_mitezone_assignment():
    frames = DummyFrames().frames
    zone = MiteZone(10, 10, 30, 30, zone_id="zoneA")
    mite = Mite([15, 15, 25, 25], frames)
    assigned = zone.assign_mites(mite)
    assert assigned, "Mite should be assigned to zone"
    assert mite.assigned_rect == zone, "Mite's assigned_rect should be the zone"
    assert mite in zone.mites, "Mite should be in zone's mites list"

def test_mite_outside_mitezone_not_assigned():
    frames = DummyFrames().frames
    zone = MiteZone(10, 10, 30, 30, zone_id="zoneA")
    mite = Mite([35, 35, 45, 45], frames)
    assigned = zone.assign_mites(mite)
    assert not assigned, "Mite outside zone should not be assigned"
    assert mite.assigned_rect != zone, "Mite's assigned_rect should not be the zone"
    assert mite not in zone.mites, "Mite should not be in zone's mites list"

def test_multiple_mites_assignment():
    frames = DummyFrames().frames
    zone = MiteZone(10, 10, 30, 30, zone_id="zoneA")
    mites = [Mite([12, 12, 18, 18], frames), Mite([20, 20, 28, 28], frames)]
    for mite in mites:
        assert zone.assign_mites(mite), "Each mite should be assigned"
    assert all(m.assigned_rect == zone for m in mites), "All mites should have correct assigned_rect"
    assert all(m in zone.mites for m in mites), "All mites should be in zone's mites list"
    assert len(zone.mites) == 2, "Zone should have two mites"

def test_textzone_inside_mitezone():
    zone = MiteZone(10, 10, 30, 30, zone_id="zoneA")
    tz = TextZone(12, 12, 18, 18, text="T1", parent_rect=zone)
    zone.add_text_zone(tz)
    assert tz in zone.text_zones, "TextZone should be added to zone"
    assert zone.zone_id == "T1", "Zone id should update to text zone's text"

def test_textzone_outside_mitezone_raises():
    zone = MiteZone(10, 10, 30, 30, zone_id="zoneA")
    with pytest.raises(ValueError):
        tz = TextZone(35, 35, 45, 45, text="T2", parent_rect=zone)

def test_mitezone_draw_runs(monkeypatch):
    frames = DummyFrames().frames
    zone = MiteZone(10, 10, 30, 30, zone_id="zoneA")
    mite = Mite([15, 15, 25, 25], frames)
    zone.assign_mites(mite)
    tz = TextZone(12, 12, 18, 18, text="T1", parent_rect=zone)
    zone.add_text_zone(tz)
    # Patch cv2.rectangle and cv2.putText to avoid GUI errors
    monkeypatch.setattr("cv2.rectangle", lambda *a, **kw: None)
    monkeypatch.setattr("cv2.putText", lambda *a, **kw: None)
    img = np.zeros((100, 100, 3), dtype=np.uint8)
    zone.draw(img)  # Should not raise
