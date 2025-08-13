# Environment Setup - Varroa Detector

## Current Environment: myenv

The project has been successfully configured to run in the `myenv` conda environment with all required dependencies.

### Quick Start

1. **Activate the environment:**
   ```bash
   conda activate myenv
   ```

2. **Launch the Modern GUI:**
   ```bash
   python modern_gui_app.py
   ```

   Or use the PowerShell launcher:
   ```bash
   .\launch_modern_gui.ps1
   ```

### Environment Files

- `env.yaml` - Main environment file with all dependencies
- `environment.yml` - Alternative format environment file
- `env_updated.yaml` - Updated environment export
- `env_backup.yaml` - Backup of the environment

### Key Dependencies Installed

- **Deep Learning:** torch, torchvision, torchaudio, ultralytics
- **Computer Vision:** opencv-python, pillow
- **GUI:** customtkinter, tkinterdnd2 (for drag & drop)
- **Data Processing:** pandas, numpy, openpyxl
- **Text Recognition:** transformers, tokenizers
- **Other:** matplotlib, requests, pyyaml

### Recreating the Environment

If you need to recreate the environment on another machine:

```bash
# Create environment from YAML file
conda env create -f env.yaml

# Or alternatively
conda env create -f environment.yml

# Activate the environment
conda activate myenv
```

### Fixed Issues

- ✅ Fixed tkinter progress bar thread safety issues
- ✅ Added tkinterdnd2 for drag & drop functionality
- ✅ All dependencies properly installed and tested
- ✅ Modern GUI launches without errors
- ✅ Environment YAML files updated with all current packages

### Running the Application

The Modern GUI application now runs successfully with:
- Proper splash screen with animated progress bar
- Drag & drop functionality for images
- All YOLO detection and text recognition features
- Thread-safe UI updates

Last updated: August 13, 2025
