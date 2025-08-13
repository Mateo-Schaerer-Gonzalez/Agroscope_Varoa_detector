# Launch Varroa Detector Modern GUI
# This script activates the myenv environment and launches the modern GUI

Write-Host "Activating myenv environment..." -ForegroundColor Green
conda activate myenv

Write-Host "Launching Varroa Detector Modern GUI..." -ForegroundColor Green
python modern_gui_app.py

Write-Host "Application closed." -ForegroundColor Yellow
pause
