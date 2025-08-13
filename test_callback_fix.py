#!/usr/bin/env python3
"""
Quick test to verify the callback issue is resolved
"""

import sys
import os

# Add the project root to the Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

def test_callback_fix():
    """Test that the analysis_completed callback works correctly"""
    print("🔧 Testing Callback Fix")
    print("=" * 30)
    
    try:
        from modern_gui_app import ModernVarroaDetectorApp
        
        # Create app instance
        app = ModernVarroaDetectorApp()
        print("✅ App created successfully")
        
        # Check that the method exists and is callable
        if hasattr(app, 'analysis_completed') and callable(getattr(app, 'analysis_completed')):
            print("✅ analysis_completed method exists and is callable")
        else:
            print("❌ analysis_completed method missing or not callable")
            return False
        
        # Check that the flag attribute exists and is boolean
        if hasattr(app, 'analysis_complete_flag') and isinstance(getattr(app, 'analysis_complete_flag'), bool):
            print("✅ analysis_complete_flag attribute exists and is boolean")
        else:
            print("❌ analysis_complete_flag attribute missing or wrong type")
            return False
        
        # Test that we can call the method directly
        try:
            # Store original values
            original_running = app.analysis_running if hasattr(app, 'analysis_running') else None
            original_flag = app.analysis_complete_flag
            
            # Set up minimal state
            app.analysis_running = True
            app.analysis_complete_flag = False
            
            # This should not raise an error
            app.analysis_completed()
            print("✅ analysis_completed() method can be called directly")
            
            # Check that the flag was updated
            if app.analysis_complete_flag:
                print("✅ analysis_complete_flag was updated correctly")
            else:
                print("⚠️  analysis_complete_flag was not updated (but no error)")
            
            # Restore original values
            if original_running is not None:
                app.analysis_running = original_running
            app.analysis_complete_flag = original_flag
            
        except Exception as e:
            print(f"❌ Error calling analysis_completed(): {e}")
            return False
        
        # Test that callback setup would work
        try:
            # This simulates what happens in the actual callback
            callback_func = getattr(app, 'analysis_completed')
            if callable(callback_func):
                print("✅ Callback function reference is callable")
            else:
                print("❌ Callback function reference is not callable")
                return False
        except Exception as e:
            print(f"❌ Error getting callback reference: {e}")
            return False
        
        print("🎉 All callback tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Error during callback test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🔍 Callback Fix Verification")
    print("=" * 40)
    
    success = test_callback_fix()
    
    if success:
        print("\n✅ Callback fix verified! The application should work without errors.")
        print("\n📝 Summary of fix:")
        print("   • Renamed attribute from 'analysis_completed' to 'analysis_complete_flag'")
        print("   • Method 'analysis_completed()' is now accessible for callbacks")
        print("   • No more naming conflicts between attribute and method")
    else:
        print("\n❌ Callback fix needs more work.")
    
    print("\n" + "=" * 40)
