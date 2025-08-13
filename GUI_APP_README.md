# Varroa Detector - Modern GUI Application

A user-friendly GUI application for analyzing bee mite images using YOLO detection technology.

## 🚀 Quick Start

### Method 1: Double-click to start
Simply double-click on `launch_gui.bat` to start the application.

### Method 2: PowerShell
Run the PowerShell script:
```powershell
.\launch_gui.ps1
```

### Method 3: Command line
```bash
conda activate myenv
python launch_gui.py
```

## 📱 Using the Application

1. **Select Dataset Folder**: Click "Browse" to select a folder containing your bee images
2. **Select Output Folder (Optional)**: Choose where to save results, or leave empty to use default location
3. **Configure Analysis**: 
   - Enter an analysis name (e.g., "experiment_1")
   - Select number of plates per recording (1 or 2)
   - Choose analysis type (New Analysis or Reanalysis)
   - Set number of recordings to process
   - Set time between recordings (in minutes)
4. **Start Analysis**: Click "🚀 Start Analysis" to begin processing
5. **Monitor Progress**: Watch the progress bar and status messages
6. **View Results**: Click "📥 Open Results Folder" when analysis is complete

## 🎯 Features

- **Modern Interface**: Clean, intuitive design with progress tracking
- **Flexible Configuration**: Support for different plate configurations and analysis types
- **Custom Output Location**: Choose where to save your results
- **Timing Control**: Configure recording intervals and number of recordings
- **Real-time Progress**: Live updates during analysis processing
- **Easy Results Access**: One-click access to results folder
- **Error Handling**: Clear error messages and validation

## 📁 Results Location

Analysis results are saved to:
- `outputs/results/` - For new analyses
- `outputs/reanalysis{N}/` - For reanalysis runs

Results include:
- Detection visualizations
- Survival analysis graphs
- PDF reports
- Excel summaries
- Raw data files

## ⚙️ Requirements

- Python environment with required packages (ultralytics, opencv, etc.)
- The `myenv` conda environment should be properly configured
- Windows OS (for batch file launcher)

## 🔧 Troubleshooting

### "Import ultralytics could not be resolved"
Make sure you're running in the `myenv` environment where ultralytics is installed.

### "No folder selected" error
Click the "Browse" button to select a valid dataset folder before starting analysis.

### Application won't start
Try running from command line to see detailed error messages:
```bash
conda activate myenv
python launch_gui.py
```

## 📊 Supported Image Formats

The application supports common image formats including:
- JPG/JPEG
- PNG
- TIF/TIFF
- BMP

## 🏗️ Project Structure

```
├── launch_gui.py          # Main GUI application
├── launch_gui.bat         # Windows batch launcher
├── launch_gui.ps1         # PowerShell launcher
├── varroa_gui.py         # Tkinter-based GUI (alternative)
├── main.py               # Core analysis functions
├── classes/              # Detection and analysis classes
├── utils/                # Utility functions
├── app/                  # Application resources
└── outputs/              # Analysis results
```

## 📞 Support

If you encounter issues:
1. Check that `myenv` environment is properly configured
2. Verify that the dataset folder contains valid images
3. Check the terminal/command prompt for detailed error messages
4. Ensure all required packages are installed in the `myenv` environment

---

**Note**: This GUI provides a user-friendly interface for the Varroa detection system. For advanced usage or batch processing, you can still use the command-line interface via `main.py`.
