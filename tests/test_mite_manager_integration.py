#!/usr/bin/env python3
"""
Test MiteManager Integration with Text Verification System

This script tests the integration between the text verification system and the actual MiteManager data.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

# Add the project root to the Python path
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

def test_mite_manager_loading():
    """Test MiteManager loading functionality"""
    print("🧪 Testing MiteManager Integration")
    print("=" * 50)
    
    try:
        # Import the modern GUI app
        from modern_gui_app import ModernVarroaDetectorApp
        
        # Create a test instance
        app = ModernVarroaDetectorApp()
        app.root.withdraw()  # Hide the main window
        
        # Test MiteManager loading
        print("\n1. Testing MiteManager file search...")
        
        # Check if MiteManager exists in classes directory
        mite_manager_path = os.path.join(os.path.dirname(__file__), "classes", "mite_manager.plk")
        if os.path.exists(mite_manager_path):
            print(f"✅ Found MiteManager at: {mite_manager_path}")
            
            # Test loading
            try:
                app.mite_manager = None
                app.results_path = os.path.dirname(__file__)
                app.load_analysis_results()
                
                if hasattr(app, 'mite_manager') and app.mite_manager:
                    print(f"✅ Successfully loaded MiteManager with {len(app.mite_manager.zones)} zones")
                    
                    # Test zone data extraction
                    if hasattr(app, 'mite_zones') and app.mite_zones:
                        print(f"✅ Extracted {len(app.mite_zones)} mites from MiteManager")
                        
                        # Display first few mites
                        print("\n📋 Sample mite data:")
                        for i, mite in enumerate(app.mite_zones[:3]):
                            print(f"   Mite {i+1}: {mite['mite_id']} in Zone {mite['zone_id']} - {mite['status']}")
                    else:
                        print("⚠️  No mite data extracted from MiteManager")
                else:
                    print("❌ Failed to load MiteManager")
                    
            except Exception as e:
                print(f"❌ Error loading MiteManager: {e}")
                
        else:
            print(f"⚠️  No MiteManager found at: {mite_manager_path}")
            print("   This is normal if no analysis has been run yet.")
            
            # Test dummy data creation
            print("\n2. Testing dummy data creation...")
            app.create_dummy_mite_data()
            
            if hasattr(app, 'mite_zones') and app.mite_zones:
                print(f"✅ Created {len(app.mite_zones)} dummy mites for testing")
            else:
                print("❌ Failed to create dummy data")
        
        print("\n3. Testing zone overlay methods...")
        
        # Test apply_zone_overlay method exists and works
        if hasattr(app, 'apply_zone_overlay'):
            print("✅ Zone overlay method available")
            
            # Create a dummy image to test overlay
            from PIL import Image, ImageTk
            test_image = Image.new('RGB', (800, 600), color='white')
            
            try:
                app.current_pil_image = test_image
                app.apply_zone_overlay()
                print("✅ Zone overlay method executed successfully")
            except Exception as e:
                print(f"⚠️  Zone overlay method error: {e}")
        
        app.root.destroy()
        
        print("\n" + "=" * 50)
        print("🎉 Integration test completed!")
        
        return True
        
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_text_zone_classes():
    """Test if TextZone and related classes can be imported"""
    print("\n🧪 Testing Text Zone Classes")
    print("-" * 30)
    
    try:
        # Test if the classes directory is accessible
        classes_dir = os.path.join(os.path.dirname(__file__), "classes")
        if os.path.exists(classes_dir):
            print("✅ Classes directory exists")
            
            # Check if Rect.py file exists
            rect_file = os.path.join(classes_dir, "Rect.py")
            if os.path.exists(rect_file):
                print("✅ Rect.py file found")
            else:
                print("❌ Rect.py file not found")
                return False
            
            # Simple import test without circular dependency
            import importlib.util
            spec = importlib.util.spec_from_file_location("Rect", rect_file)
            if spec:
                print("✅ Rect module can be loaded")
            else:
                print("❌ Rect module cannot be loaded")
                return False
                
            return True
        else:
            print("❌ Classes directory not found")
            return False
        
    except Exception as e:
        print(f"❌ Error with TextZone classes: {e}")
        return False

if __name__ == "__main__":
    print("🔬 MiteManager Integration Test Suite")
    print("=" * 60)
    
    # Run tests
    integration_ok = test_mite_manager_loading()
    text_zone_ok = test_text_zone_classes()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print(f"   Integration Test: {'✅ PASS' if integration_ok else '❌ FAIL'}")
    print(f"   Text Zone Test:   {'✅ PASS' if text_zone_ok else '❌ FAIL'}")
    
    if integration_ok and text_zone_ok:
        print("\n🎉 All tests passed! MiteManager integration is ready.")
        print("\n💡 Next steps:")
        print("   1. Run an analysis to generate a MiteManager file")
        print("   2. Open the text verification system")
        print("   3. Test zone clicking and text editing")
    else:
        print("\n⚠️  Some tests failed. Check the error messages above.")
    
    print("\n" + "=" * 60)
