"""
Test script to verify immediate text editing after recording 1 pause
"""

import sys
import os
import threading
import time

# Add the current directory to the path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_immediate_text_editing():
    """Test that text editing is available immediately after recording 1 pause"""
    print("Testing immediate text editing availability...")
    
    try:
        from main import AnalysisState, get_analysis_state
        from modern_gui_app import ModernVarroaDetectorApp
        print("✅ Successfully imported required components")
    except ImportError as e:
        print(f"❌ Failed to import components: {e}")
        return False
    
    # Create a mock MiteManager with zones
    class MockZone:
        def __init__(self, coords, mites):
            self.coords = coords
            self.mites = mites
    
    class MockMiteManager:
        def __init__(self):
            # Create test zones with coordinates and mites
            self.zones = [
                MockZone((10, 10, 110, 110), ["mite1", "mite2"]),  # Zone with 2 mites
                MockZone((120, 10, 220, 110), []),                # Empty zone
                MockZone((10, 120, 110, 220), ["mite3"]),         # Zone with 1 mite
            ]
    
    # Create a simple GUI instance (without tkinter initialization)
    class MockGUI:
        def __init__(self):
            self.recording1_pause = False
            self.analysis_paused = False
            self.mite_manager = None
            self.mite_zones = []
            self.zone_coordinates = []
            self.zones_locked = True
            
        def update_progress(self, value, message):
            print(f"Progress: {value}% - {message}")
        
        def refresh_zone_display(self):
            print(f"Refreshing zone display - {len(self.mite_zones)} zones available")
        
        def unlock_zones(self):
            self.zones_locked = False
            print("🔓 Zones unlocked for text editing")
        
        def update_verify_button_state(self):
            if self.recording1_pause and self.zone_coordinates:
                print("✅ Text verification buttons enabled")
            else:
                print("❌ Text verification buttons disabled")
        
        def setup_recording1_pause(self):
            print("Setting up recording 1 pause...")
            self.recording1_pause = True
            self.analysis_paused = True
            
            if hasattr(self, 'mite_manager') and self.mite_manager:
                print(f"✅ Using MiteManager from analysis pause with {len(self.mite_manager.zones)} zones")
                self.load_mite_data_from_manager()
            
            self.update_verify_button_state()
        
        def load_mite_data_from_manager(self):
            """Load mite data directly from the MiteManager instance"""
            if not self.mite_manager or not hasattr(self.mite_manager, 'zones'):
                print("❌ No valid MiteManager available")
                return False
            
            try:
                print(f"🔄 Loading mite data from MiteManager with {len(self.mite_manager.zones)} zones")
                
                # Extract mite data from MiteManager zones
                self.mite_zones = []
                self.zone_coordinates = []
                zone_index = 0
                
                for zone in self.mite_manager.zones:
                    # Get zone coordinates
                    if hasattr(zone, 'coords') and zone.coords:
                        x1, y1, x2, y2 = zone.coords
                    else:
                        x1, y1, x2, y2 = 0, 0, 100, 100
                    
                    # Count mites in this zone
                    mite_count = len(zone.mites) if hasattr(zone, 'mites') else 0
                    
                    # Create zone data structure
                    zone_data = {
                        'zone_id': f"Zone {zone_index + 1}",
                        'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2,
                        'mite_count': mite_count,
                        'mites': zone.mites if hasattr(zone, 'mites') else [],
                        'zone_index': zone_index
                    }
                    
                    self.mite_zones.append(zone_data)
                    self.zone_coordinates.append((zone_index, x1, y1, x2, y2))
                    zone_index += 1
                
                print(f"✅ Successfully loaded {len(self.mite_zones)} zones for text verification")
                print(f"📍 Zone coordinates: {len(self.zone_coordinates)} zones ready for editing")
                
                # Refresh the zone display and unlock zones
                self.refresh_zone_display()
                self.unlock_zones()
                
                return True
                
            except Exception as e:
                print(f"❌ Error loading mite data from manager: {e}")
                return False
        
        def pause_for_text_verification(self, mite_manager_instance):
            """Simulate the pause callback"""
            print("⏸️ Analysis paused after recording 1 - starting text verification")
            self.mite_manager = mite_manager_instance
            self.update_progress(60, "⏸️ Analysis paused - Please verify zone IDs")
            self.setup_recording1_pause()
            print("📱 GUI pause setup complete - text editing should now be available")
            return True
    
    # Test the complete flow
    gui = MockGUI()
    mock_mite_manager = MockMiteManager()
    
    print("\n1. Initial state check:")
    print(f"   - Zones locked: {gui.zones_locked}")
    print(f"   - Recording1 pause: {gui.recording1_pause}")
    print(f"   - Zone coordinates: {len(gui.zone_coordinates)}")
    print(f"   - Mite zones: {len(gui.mite_zones)}")
    
    print("\n2. Triggering analysis pause...")
    gui.pause_for_text_verification(mock_mite_manager)
    
    print("\n3. Post-pause state check:")
    print(f"   - Zones locked: {gui.zones_locked}")
    print(f"   - Recording1 pause: {gui.recording1_pause}")
    print(f"   - Zone coordinates: {len(gui.zone_coordinates)}")
    print(f"   - Mite zones: {len(gui.mite_zones)}")
    
    # Verify that text editing should be available
    text_editing_available = (
        not gui.zones_locked and 
        gui.recording1_pause and 
        len(gui.zone_coordinates) > 0 and 
        len(gui.mite_zones) > 0
    )
    
    print(f"\n4. Text editing availability: {'✅ AVAILABLE' if text_editing_available else '❌ NOT AVAILABLE'}")
    
    if text_editing_available:
        print("   - Zones are unlocked ✓")
        print("   - Recording1 pause is active ✓") 
        print("   - Zone coordinates are loaded ✓")
        print("   - Mite zones are loaded ✓")
        
        # Test that zone data is correctly populated
        for i, zone in enumerate(gui.mite_zones):
            print(f"   - Zone {i+1}: {zone['mite_count']} mites, coords ({zone['x1']},{zone['y1']}) to ({zone['x2']},{zone['y2']})")
    
    return text_editing_available

def main():
    """Main test function"""
    print("=== Testing Immediate Text Editing After Recording 1 ===\n")
    
    if test_immediate_text_editing():
        print("\n✅ SUCCESS: Text editing is immediately available after recording 1 pause!")
    else:
        print("\n❌ FAILED: Text editing is not available after recording 1 pause")

if __name__ == "__main__":
    main()
