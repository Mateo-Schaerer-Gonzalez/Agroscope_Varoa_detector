# Varroa Detector - Modern GUI Application

A modern, user-friendly GUI application for analyzing bee mite images using YOLO detection powered by AI.

## Features

🐝 **Modern Interface**: Clean, intuitive design with visual feedback  
📁 **Easy File Selection**: Simple folder browsing for dataset selection  
⚙️ **Flexible Configuration**: Configurable analysis parameters  
📊 **Progress Tracking**: Real-time progress updates with progress bar  
📈 **Automated Reports**: Generates comprehensive analysis reports  
📁 **Easy Results Access**: One-click access to results folder  

## Quick Start

### Option 1: Using the Batch File (Recommended for Windows)
1. Double-click `launch_gui.bat` to start the application

### Option 2: Using Python
1. Run the launcher:
   ```bash
   python launch_gui.py
   ```

### Option 3: Direct Launch
1. Run the GUI directly:
   ```bash
   python varroa_gui.py
   ```

## How to Use

### 1. Select Dataset Folder
- Click the "Browse" button to select your dataset folder
- The folder should contain the images you want to analyze

### 2. Configure Analysis Settings
- **Analysis Name**: Enter a descriptive name for your analysis
- **Plates per Recording**: Choose between 1 or 2 plates
- **Analysis Type**: 
  - "New Analysis": For first-time analysis
  - "Reanalysis": For re-processing existing data

### 3. Start Analysis
- Click "🚀 Start Analysis" to begin processing
- Monitor the progress bar for real-time updates
- The analysis runs in the background, so the UI remains responsive

### 4. View Results
- Once complete, click "📁 Open Results Folder" to access your results
- Results include:
  - Detection visualizations
  - Survival graphs
  - PDF reports
  - Excel summaries
  - Raw data files

## Results Structure

The application generates results in the `outputs/` folder:
```
outputs/
├── results/           # Main analysis results
│   ├── recording1/    # Individual recording results
│   ├── recording2/    # Individual recording results
│   └── ...
├── reanalysis1/       # First reanalysis results
├── reanalysis2/       # Second reanalysis results
└── ...
```

Each recording folder contains:
- `frame0_detection.png` - Detection visualization
- `survival_graph.png` - Survival analysis chart  
- `recording_report.pdf` - Comprehensive PDF report
- `mite_data.xlsx` - Detailed mite data
- Raw analysis files

## System Requirements

- **Operating System**: Windows 10/11, macOS, or Linux
- **Python**: 3.8 or higher
- **Memory**: 4GB RAM minimum, 8GB recommended
- **Storage**: 1GB free space for results

## Dependencies

The application uses standard Python libraries:
- `tkinter` - GUI framework (built-in with Python)
- `threading` - Background processing
- `pathlib` - File path handling

AI/ML dependencies (automatically managed):
- `ultralytics` - YOLO object detection
- `opencv-python` - Image processing
- `numpy` - Numerical computations
- `matplotlib` - Plotting and visualization
- `pandas` - Data analysis
- `openpyxl` - Excel file generation

## Troubleshooting

### Application Won't Start
- Ensure Python is properly installed
- Check that all dependencies are installed
- Try running from command line to see error messages

### Analysis Fails
- Verify the selected folder contains valid image files
- Check that the folder path doesn't contain special characters
- Ensure sufficient disk space for results

### Results Not Found
- Check the `outputs/` folder in the project directory
- Look for `results/` or `reanalysis*/` subfolders
- Verify the analysis completed successfully

## Advanced Usage

### Batch Processing
For processing multiple datasets:
1. Run analysis for each dataset separately
2. Use descriptive names to distinguish results
3. Results are automatically organized in separate folders

### Customizing Analysis Parameters
The GUI provides the most common settings. For advanced configuration:
1. Modify parameters in `main.py`
2. Create custom analysis scripts using the `predict()` function

## Support

For issues or questions:
1. Check the console output for error messages
2. Verify all dependencies are installed correctly
3. Ensure dataset folder structure is correct

## File Structure

Key application files:
- `varroa_gui.py` - Main GUI application
- `launch_gui.py` - Application launcher  
- `launch_gui.bat` - Windows batch launcher
- `main.py` - Core analysis engine
- `classes/` - Analysis modules
- `utils/` - Utility functions

## Version History

- **v1.0** - Initial GUI release with modern interface
- Core features: folder selection, progress tracking, results access
- Built-in error handling and user feedback
