"""
Simple launcher for Modern GUI with proper environment activation
"""

import subprocess
import sys
import os

def launch_modern_gui():
    """Launch the Modern GUI application with myenv environment"""
    try:
        # Get the current directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Change to the project directory
        os.chdir(current_dir)
        
        # Command to activate conda environment and run the modern GUI
        if os.name == 'nt':  # Windows
            # Use PowerShell to activate conda environment
            cmd = [
                'powershell.exe', '-Command',
                'conda activate myenv; python modern_gui_app.py'
            ]
        else:  # Linux/Mac
            cmd = ['conda', 'run', '-n', 'myenv', 'python', 'modern_gui_app.py']
        
        # Launch the GUI
        print("🚀 Launching Varroa Detector Modern GUI...")
        print("📁 Working directory:", current_dir)
        print("🐍 Environment: myenv")
        print("🎯 Command:", ' '.join(cmd))
        
        subprocess.run(cmd, check=True)
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error launching GUI: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    launch_modern_gui()
