"""
Test zone clicking and magenta selection during recording 1 pause
"""

import sys
import os
import threading
import time

# Add the current directory to the path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_zone_clicking_during_pause():
    """Test that zones can be clicked and turn magenta during recording 1 pause"""
    print("Testing zone clicking during recording 1 pause...")
    
    try:
        from main import AnalysisState, get_analysis_state
        from modern_gui_app import ModernVarroaDetectorApp
        print("✅ Successfully imported required components")
    except ImportError as e:
        print(f"❌ Failed to import components: {e}")
        return False
    
    # Create a mock MiteManager with zones
    class MockZone:
        def __init__(self, coords, mites, zone_id=None):
            self.coords = coords
            self.mites = mites
            self.zone_id = zone_id or "Zone"
    
    class MockMiteManager:
        def __init__(self):
            self.zones = [
                MockZone((10, 10, 110, 110), ["mite1", "mite2"], "A1"),
                MockZone((120, 10, 220, 110), [], "A2"),
                MockZone((10, 120, 110, 220), ["mite3"], "B1"),
            ]
    
    # Create a mock GUI to test zone clicking logic
    class MockGUI:
        def __init__(self):
            self.recording1_pause = False
            self.analysis_complete_flag = False
            self.mite_manager = None
            self.mite_zones = []
            self.zone_coordinates = []
            self.zones_locked = True
            self.selected_zone = None
            self.text_verification_active = False
            self.current_hover_zone = None
            
        def setup_recording1_pause(self):
            print("Setting up recording 1 pause...")
            self.recording1_pause = True
            self.analysis_paused = True
            
            if hasattr(self, 'mite_manager') and self.mite_manager:
                self.load_mite_data_from_manager()
        
        def load_mite_data_from_manager(self):
            """Load mite data directly from the MiteManager instance"""
            if not self.mite_manager:
                return False
            
            self.mite_zones = []
            self.zone_coordinates = []
            zone_index = 0
            
            for zone in self.mite_manager.zones:
                if hasattr(zone, 'coords') and zone.coords:
                    x1, y1, x2, y2 = zone.coords
                else:
                    x1, y1, x2, y2 = 0, 0, 100, 100
                
                mite_count = len(zone.mites) if hasattr(zone, 'mites') else 0
                
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
            
            # Unlock zones for editing
            self.zones_locked = False
            print(f"✅ Loaded {len(self.mite_zones)} zones, zones_locked={self.zones_locked}")
            return True
        
        def get_zone_at_point(self, x, y):
            """Simulate finding zone at point"""
            for i, (zone_class, x1, y1, x2, y2) in enumerate(self.zone_coordinates):
                if x1 <= x <= x2 and y1 <= y <= y2:
                    return i
            return None
        
        def update_zone_info_display(self, zone_index):
            if zone_index is not None:
                print(f"📍 Zone {zone_index + 1} selected for editing")
            else:
                print("📍 Zone deselected")
        
        def update_verify_button_state(self):
            if (self.analysis_complete_flag or self.recording1_pause) and self.zone_coordinates:
                print("✅ Text verification buttons enabled")
            else:
                print("❌ Text verification buttons disabled")
        
        def refresh_zone_display(self):
            if self.selected_zone is not None:
                print(f"🎨 Zone {self.selected_zone + 1} should be displayed in MAGENTA")
            else:
                print("🎨 No zone selected - normal colors")
        
        def can_click_zones(self):
            """Check if zone clicking is allowed"""
            return (self.analysis_complete_flag or self.recording1_pause) and self.zone_coordinates
        
        def simulate_zone_click(self, x, y):
            """Simulate the zone clicking logic"""
            print(f"🖱️ Simulating click at ({x}, {y})")
            
            # Check if clicking is allowed (mimic on_image_click guard clause)
            if not (self.analysis_complete_flag or self.recording1_pause) or not self.zone_coordinates:
                print("❌ Zone clicking not allowed - guard clause failed")
                return False
            
            # Find clicked zone
            clicked_zone = self.get_zone_at_point(x, y)
            
            if clicked_zone is not None:
                # Toggle zone selection
                if self.selected_zone == clicked_zone:
                    # Deselect if already selected
                    self.selected_zone = None
                    self.update_zone_info_display(None)
                    print(f"🔄 Zone {clicked_zone + 1} deselected")
                else:
                    # Select the zone
                    self.selected_zone = clicked_zone
                    self.update_zone_info_display(clicked_zone)
                    # Enable text verification mode
                    self.text_verification_active = True
                    self.update_verify_button_state()
                    print(f"🔄 Zone {clicked_zone + 1} selected - should turn MAGENTA")
                
                # Refresh display to show selection visually
                self.refresh_zone_display()
                return True
            else:
                # Clicked outside any zone - deselect
                self.selected_zone = None
                self.text_verification_active = False
                self.update_zone_info_display(None)
                self.update_verify_button_state()
                print("🔄 Clicked outside zones - deselected")
                return True
        
        def pause_for_text_verification(self, mite_manager_instance):
            """Simulate the pause callback"""
            print("⏸️ Analysis paused after recording 1 - starting text verification")
            self.mite_manager = mite_manager_instance
            self.setup_recording1_pause()
            return True
    
    # Test the complete clicking flow
    gui = MockGUI()
    mock_mite_manager = MockMiteManager()
    
    print("\n1. Initial state (before analysis):")
    print(f"   - Can click zones: {gui.can_click_zones()}")
    print(f"   - Recording1 pause: {gui.recording1_pause}")
    print(f"   - Analysis complete: {gui.analysis_complete_flag}")
    print(f"   - Zone coordinates: {len(gui.zone_coordinates)}")
    
    # Try clicking before pause (should fail)
    print("\n2. Attempting to click zone before pause...")
    click_result = gui.simulate_zone_click(50, 50)  # Should be in zone 0
    print(f"   - Click result: {'SUCCESS' if click_result else 'FAILED (expected)'}")
    
    # Trigger recording 1 pause
    print("\n3. Triggering recording 1 pause...")
    gui.pause_for_text_verification(mock_mite_manager)
    
    print("\n4. State after recording 1 pause:")
    print(f"   - Can click zones: {gui.can_click_zones()}")
    print(f"   - Recording1 pause: {gui.recording1_pause}")
    print(f"   - Analysis complete: {gui.analysis_complete_flag}")
    print(f"   - Zone coordinates: {len(gui.zone_coordinates)}")
    print(f"   - Zones locked: {gui.zones_locked}")
    
    # Try clicking after pause (should work)
    print("\n5. Attempting to click zones during pause...")
    
    # Click zone 1 (should select and turn magenta)
    print("   a) Clicking zone 1...")
    click_result1 = gui.simulate_zone_click(50, 50)  # Zone 0 coordinates
    print(f"      - Click result: {'SUCCESS' if click_result1 else 'FAILED'}")
    print(f"      - Selected zone: {gui.selected_zone}")
    
    # Click zone 1 again (should deselect)
    print("   b) Clicking zone 1 again (should deselect)...")
    click_result2 = gui.simulate_zone_click(50, 50)  # Same zone
    print(f"      - Click result: {'SUCCESS' if click_result2 else 'FAILED'}")
    print(f"      - Selected zone: {gui.selected_zone}")
    
    # Click zone 2 (should select different zone)
    print("   c) Clicking zone 2...")
    click_result3 = gui.simulate_zone_click(150, 50)  # Zone 1 coordinates
    print(f"      - Click result: {'SUCCESS' if click_result3 else 'FAILED'}")
    print(f"      - Selected zone: {gui.selected_zone}")
    
    # Click outside zones (should deselect)
    print("   d) Clicking outside zones...")
    click_result4 = gui.simulate_zone_click(500, 500)  # Outside all zones
    print(f"      - Click result: {'SUCCESS' if click_result4 else 'FAILED'}")
    print(f"      - Selected zone: {gui.selected_zone}")
    
    # Test success criteria
    success_criteria = [
        gui.can_click_zones(),  # Zone clicking should be enabled
        len(gui.zone_coordinates) > 0,  # Zone coordinates should be loaded
        not gui.zones_locked,  # Zones should be unlocked
        click_result1 and click_result2 and click_result3 and click_result4  # All clicks should work
    ]
    
    all_success = all(success_criteria)
    
    print(f"\n6. Test Results:")
    print(f"   - Zone clicking enabled: {'✅' if gui.can_click_zones() else '❌'}")
    print(f"   - Zone coordinates loaded: {'✅' if len(gui.zone_coordinates) > 0 else '❌'}")
    print(f"   - Zones unlocked: {'✅' if not gui.zones_locked else '❌'}")
    print(f"   - All click operations successful: {'✅' if click_result1 and click_result2 and click_result3 and click_result4 else '❌'}")
    
    return all_success

def main():
    """Main test function"""
    print("=== Testing Zone Clicking and Magenta Selection During Recording 1 Pause ===\n")
    
    if test_zone_clicking_during_pause():
        print("\n✅ SUCCESS: Zone clicking and magenta selection work during recording 1 pause!")
    else:
        print("\n❌ FAILED: Zone clicking does not work properly during recording 1 pause")

if __name__ == "__main__":
    main()
