@echo off
echo Starting Varroa Detector GUI Application...
echo.

REM Change to the script directory
cd /d "%~dp0"

REM Run the GUI application using myenv environment
conda activate myenv && python launch_gui.py

REM Keep the window open if there's an error
if errorlevel 1 (
    echo.
    echo An error occurred. Press any key to exit...
    pause >nul
)
