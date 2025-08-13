# PowerShell script to launch the Varroa Detector GUI
Write-Host "Starting Varroa Detector GUI Application..." -ForegroundColor Green
Write-Host ""

# Change to script directory
Set-Location $PSScriptRoot

# Activate myenv and run the application
try {
    Write-Host "Activating myenv environment..." -ForegroundColor Yellow
    conda activate myenv
    
    Write-Host "Starting GUI application..." -ForegroundColor Yellow
    python launch_gui.py
}
catch {
    Write-Host "Error occurred: $_" -ForegroundColor Red
    Write-Host "Press any key to exit..."
    Read-Host
}
