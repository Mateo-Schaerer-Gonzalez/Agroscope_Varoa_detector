#!/usr/bin/env python3
"""
Debug Zone Display - Check zone IDs and mite counts

This script helps debug why zone IDs and mite counts aren't showing correctly.
"""

import tkinter as tk
import sys
import os

# Add the project root to the Python path
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

def debug_zone_data():
    """Debug the zone data and display information"""
    print("🐛 Debugging Zone Display Issues")
    print("=" * 50)
    
    try:
        from modern_gui_app import ModernVarroaDetectorApp
        
        # Create app instance
        app = ModernVarroaDetectorApp()
        app.root.withdraw()  # Hide window
        
        print("1. Checking app initialization...")
        print(f"   Analysis complete: {getattr(app, 'analysis_complete_flag', 'Not set')}")
        print(f"   Zones locked: {getattr(app, 'zones_locked', 'Not set')}")
        print(f"   MiteManager: {getattr(app, 'mite_manager', 'Not set')}")
        
        print("\n2. Loading analysis results (this will create dummy data if no MiteManager)...")
        app.load_analysis_results()
        
        print(f"   MiteManager after loading: {'Available' if app.mite_manager else 'Not available'}")
        print(f"   Mite zones count: {len(app.mite_zones) if hasattr(app, 'mite_zones') else 'Not set'}")
        print(f"   Zone coordinates count: {len(app.zone_coordinates) if hasattr(app, 'zone_coordinates') else 'Not set'}")
        
        if hasattr(app, 'mite_zones') and app.mite_zones:
            print("\n3. Sample mite zone data:")
            for i, mite in enumerate(app.mite_zones[:3]):
                print(f"   Mite {i}: {mite}")
                
        if hasattr(app, 'zone_coordinates') and app.zone_coordinates:
            print(f"\n4. Zone coordinates: {len(app.zone_coordinates)} zones")
            for i, coords in enumerate(app.zone_coordinates[:3]):
                print(f"   Zone {i}: {coords}")
        
        # Test hover info method directly
        print(f"\n5. Testing hover info for zones 0-2...")
        for zone_idx in range(min(3, len(app.zone_coordinates) if hasattr(app, 'zone_coordinates') else 0)):
            print(f"\n   Testing zone {zone_idx}:")
            
            # Check what data is available for this zone
            if app.mite_manager and hasattr(app.mite_manager, 'zones'):
                if zone_idx < len(app.mite_manager.zones):
                    mite_zone = app.mite_manager.zones[zone_idx]
                    mite_count = len(mite_zone.mites) if hasattr(mite_zone, 'mites') else 0
                    zone_label = getattr(mite_zone, 'zone_id', f'Zone_{zone_idx}')
                    print(f"     MiteManager - Zone: {zone_label}, Mites: {mite_count}")
                else:
                    print(f"     Zone {zone_idx} not found in MiteManager")
            
            # Check mite_zones data
            zone_mites = [mite for mite in app.mite_zones if mite.get('zone_id') == zone_idx]
            print(f"     Mite zones data - Count: {len(zone_mites)}")
            
            if zone_mites:
                for mite in zone_mites:
                    print(f"       - {mite.get('mite_id', 'no_id')} in zone {mite.get('zone_id', 'no_zone')}")
        
        # Test MiteManager loading specifically
        if os.path.exists(os.path.join("classes", "mite_manager.plk")):
            print(f"\n6. MiteManager file exists - trying to load directly...")
            try:
                import pickle
                with open(os.path.join("classes", "mite_manager.plk"), 'rb') as f:
                    mite_manager = pickle.load(f)
                    print(f"   Loaded MiteManager with {len(mite_manager.zones)} zones")
                    
                    for i, zone in enumerate(mite_manager.zones[:3]):
                        zone_id = getattr(zone, 'zone_id', 'no_id')
                        mite_count = len(zone.mites) if hasattr(zone, 'mites') else 0
                        print(f"   Zone {i}: ID='{zone_id}', Mites={mite_count}")
                        
            except Exception as e:
                print(f"   Error loading MiteManager: {e}")
        else:
            print(f"\n6. No MiteManager file found at classes/mite_manager.plk")
        
        app.root.destroy()
        
    except Exception as e:
        print(f"❌ Debug failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_zone_data()
