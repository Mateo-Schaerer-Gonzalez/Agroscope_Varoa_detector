import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import logging

import pytest
from classes.mite import Mite
from classes.Rect import MiteZone
logging.basicConfig(level=logging.DEBUG, format='[DEBUG TEST] %(message)s', force=True)


class DummyFrames:
    def __init__(self, num_frames=10, height=100, width=100, channels=3):
        import numpy as np
        self.frames = np.zeros((num_frames, height, width, channels), dtype=np.uint8)
    def __getitem__(self, idx):
        return self.frames[idx]
    def __len__(self):
        return self.frames.shape[0]
    @property
    def shape(self):
        return self.frames.shape


def test_mite_zone_id_integrity_after_reassignment():
    logging.debug("test_mite_zone_id_integrity_after_reassignment START")
    zone = MiteZone(0, 0, 50, 50, zone_id="Z")
    frames = DummyFrames().frames  # <-- FIXED
    mite = Mite([10, 10, 20, 20], frames)
    zone.assign_mites(mite)
    logging.debug(f"Mite assigned to zone: {mite.assigned_rect.zone_id}")
    assert mite.assigned_rect.zone_id == "Z"

    new_zone = MiteZone(0, 0, 50, 50, zone_id="Y")
    new_zone.assign_mites(mite)
    logging.debug(f"Mite reassigned to zone: {mite.assigned_rect.zone_id}")
    assert mite.assigned_rect.zone_id == "Y"
    logging.debug("test_mite_zone_id_integrity_after_reassignment END")

def test_zone_id_not_none_after_assignment():
    logging.debug("test_zone_id_not_none_after_assignment START")
    zone = MiteZone(0, 0, 50, 50, zone_id="TestZone")
    frames = DummyFrames().frames  # <-- FIXED
    mite = Mite([10, 10, 20, 20], frames)
    zone.assign_mites(mite)
    logging.debug(f"Assigned zone_id: {mite.assigned_rect.zone_id}")
    assert mite.assigned_rect.zone_id is not None
    logging.debug("test_zone_id_not_none_after_assignment END")

def test_no_zone_id_leakage_between_mites():
    logging.debug("test_no_zone_id_leakage_between_mites START")
    zone1 = MiteZone(0, 0, 50, 50, zone_id="Zone1")
    zone2 = MiteZone(51, 0, 100, 50, zone_id="Zone2")
    frames = DummyFrames().frames  # <-- FIXED
    mite1 = Mite([10, 10, 20, 20], frames)
    mite2 = Mite([60, 10, 70, 20], frames)
    zone1.assign_mites(mite1)
    zone2.assign_mites(mite2)
    logging.debug(f"mite1 zone_id: {mite1.assigned_rect.zone_id}, mite2 zone_id: {mite2.assigned_rect.zone_id}")
    assert mite1.assigned_rect.zone_id != mite2.assigned_rect.zone_id
    logging.debug("test_no_zone_id_leakage_between_mites END")

def test_mite_reflects_zone_id_change():
    logging.debug("test_mite_reflects_zone_id_change START")
    zone = MiteZone(0, 0, 50, 50, zone_id="InitialZone")
    frames = DummyFrames().frames  # <-- FIXED
    mite = Mite([10, 10, 20, 20], frames)
    zone.assign_mites(mite)
    logging.debug(f"Assigned zone_id: {mite.assigned_rect.zone_id}")
    assert mite.assigned_rect.zone_id == "InitialZone"

    # Change the zone_id of the zone object
    zone.zone_id = "UpdatedZone"
    logging.debug(f"Zone id changed to: {zone.zone_id}")
    # The mite's assigned_rect should reflect the new zone_id
    assert mite.assigned_rect.zone_id == "UpdatedZone"
    logging.debug(f"Mite now sees zone_id: {mite.assigned_rect.zone_id}")
    logging.debug("test_mite_reflects_zone_id_change END")

def test_mite_zone_color_assignment_and_change():
    frames = DummyFrames().frames
    zone1 = MiteZone(0, 0, 50, 50, zone_id="Zone1")
    zone2 = MiteZone(51, 0, 100, 50, zone_id="Zone2")
    mite = Mite([10, 10, 20, 20], frames)
    zone1.assign_mites(mite)
    assert mite.bbox.color == zone1.color
    zone2.assign_mites(mite)
    assert mite.bbox.color == zone2.color

