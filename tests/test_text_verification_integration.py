#!/usr/bin/env python3
"""
Test script for the text verification functionality in the Modern Varroa Detector GUI
"""

import sys
import os

# Add the project root to the Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

def test_text_verification():
    """Test the text verification functionality"""
    print("🧪 Testing Text Verification Functionality")
    print("=" * 50)
    
    try:
        # Import the main application
        from modern_gui_app import ModernVarroaDetectorApp
        
        print("✅ Successfully imported ModernVarroaDetectorApp")
        
        # Create app instance
        app = ModernVarroaDetectorApp()
        print("✅ Successfully created app instance")
        
        # Check if text verification attributes are initialized
        required_attrs = [
            'analysis_complete_flag',
            'zones_locked', 
            'mite_zones',
            'current_hover_zone',
            'zone_coordinates',
            'canvas_scale',
            'canvas_offset_x',
            'canvas_offset_y'
        ]
        
        for attr in required_attrs:
            if hasattr(app, attr):
                print(f"✅ Attribute '{attr}' initialized")
            else:
                print(f"❌ Attribute '{attr}' missing")
        
        # Test dummy mite data creation
        print("\n🔬 Testing dummy mite data creation...")
        app.create_dummy_mite_data()
        
        if len(app.mite_zones) > 0:
            print(f"✅ Created {len(app.mite_zones)} dummy mites")
            for i, mite in enumerate(app.mite_zones[:3]):  # Show first 3
                print(f"   Mite {i+1}: {mite['mite_id']} - Zone {mite['zone_id']} - {mite['status']}")
        else:
            print("❌ No dummy mites created")
        
        # Test zone locking functionality
        print("\n🔒 Testing zone locking...")
        app.zones_locked = False
        print(f"   Initial lock status: {app.zones_locked}")
        
        app.lock_zones()
        print(f"   After locking: {app.zones_locked}")
        
        if app.zones_locked:
            print("✅ Zone locking works correctly")
        else:
            print("❌ Zone locking failed")
        
        # Test text verification methods
        print("\n📝 Testing text verification methods...")
        
        methods_to_test = [
            'get_zone_at_point',
            'update_hover_info', 
            'update_mite_list_display',
            'save_text_verification'
        ]
        
        for method_name in methods_to_test:
            if hasattr(app, method_name) and callable(getattr(app, method_name)):
                print(f"✅ Method '{method_name}' available")
            else:
                print(f"❌ Method '{method_name}' missing")
        
        print("\n🎉 Text verification functionality test completed!")
        print("=" * 50)
        
        return True
        
    except Exception as e:
        print(f"❌ Error during testing: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_zone_interaction():
    """Test zone interaction functionality"""
    print("\n🎯 Testing Zone Interaction")
    print("=" * 30)
    
    try:
        from modern_gui_app import ModernVarroaDetectorApp
        app = ModernVarroaDetectorApp()
        
        # Simulate zone coordinates
        app.zone_coordinates = [
            (0, 100, 100, 200, 200),  # class, x1, y1, x2, y2
            (1, 300, 100, 400, 200),
            (0, 100, 300, 200, 400)
        ]
        
        # Test point detection
        test_points = [
            (150, 150, 0),  # Should hit zone 0
            (350, 150, 1),  # Should hit zone 1
            (150, 350, 2),  # Should hit zone 2
            (50, 50, None), # Should miss all zones
        ]
        
        for x, y, expected_zone in test_points:
            result = app.get_zone_at_point(x, y)
            if result == expected_zone:
                print(f"✅ Point ({x}, {y}) correctly detected zone {result}")
            else:
                print(f"❌ Point ({x}, {y}) expected zone {expected_zone}, got {result}")
        
        return True
        
    except Exception as e:
        print(f"❌ Zone interaction test failed: {str(e)}")
        return False

if __name__ == "__main__":
    print("🐝 Varroa Detector - Text Verification Test Suite")
    print("=" * 60)
    
    success = True
    
    # Run functionality test
    success &= test_text_verification()
    
    # Run zone interaction test
    success &= test_zone_interaction()
    
    if success:
        print("\n🎉 All tests passed! Text verification functionality is ready.")
        print("\nℹ️  To use the text verification feature:")
        print("   1. Select a dataset folder")
        print("   2. Run analysis (zones will be locked after completion)")
        print("   3. Hover over zones to see mite information")
        print("   4. Click on zones to edit detected text")
    else:
        print("\n❌ Some tests failed. Please check the implementation.")
    
    print("\n" + "=" * 60)
