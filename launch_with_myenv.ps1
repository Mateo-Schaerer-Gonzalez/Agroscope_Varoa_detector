# PowerShell script to launch the Varroa Detector with myenv environment
Write-Host "Activating myenv environment..." -ForegroundColor Green
conda activate myenv
Write-Host "Starting Varroa Detector GUI..." -ForegroundColor Green
python modern_gui_app.py
Read-Host "Press Enter to continue..."
