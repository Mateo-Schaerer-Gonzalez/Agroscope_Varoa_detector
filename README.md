# Agroscope Varroa Detector

This repository provides a complete pipeline for Varroa mite detection and live/dead classification, designed to support automated monitoring of honeybee colonies with a modern graphical user interface.

## Detection Model Used

Detection Model:
Mite detection is performed using the model introduced in:
"An AI-Based Open-Source Software for Varroa Mite Fall Analysis in Honeybee Colonies"
Giovanni Formato et al., 2023
https://www.mdpi.com/2077-0472/15/9/969#:~:text=This%20study%20was%20designed%20to%20develop%20and%20test,images%20of%20sticky%20boards%20collected%20in%20honeybee%20colonies.

## Installation and Usage

### Prerequisites
- Python 3.8 or higher
- Windows/macOS/Linux

### Installation

```bash
git clone https://github.com/Mateo-Schaerer-Gonzalez/Agroscope_Varoa_detector.git
cd Agroscope_Varoa_detector
pip install -r requirements.txt
```

### Running the Application

#### Option 1: GUI Application (Recommended)
For a user-friendly graphical interface:

**Windows:**
```bash
start_app.bat
```

**macOS/Linux:**
```bash
python run_app.py
```

#### Option 2: Command Line Interface
For direct script execution:
```bash
python main.py
```

## Features

### Modern GUI Application
- **Intuitive Interface**: Modern dark theme with customizable options
- **Drag & Drop**: Easy folder selection for image processing
- **Progress Tracking**: Real-time progress updates during analysis
- **Results Download**: One-click access to analysis results
- **Error Handling**: Clear error messages and validation

### Analysis Capabilities
- Automated Varroa mite detection using YOLOv11
- Live/dead classification
- Survival time analysis
- Excel and PDF report generation
- Visualization of detection results
- Support for reanalysis of existing data

### Supported Input Formats
- JPG/JPEG
- PNG
- BMP
- TIFF/TIF

## How to Use the GUI

1. **Select Folder**: Click "Browse" to select a folder containing your microscopy images
2. **Analysis Name**: Enter a descriptive name for your analysis session
3. **Configure Options**:
   - Choose number of mites per plate (1 or 2)
   - Optionally enable reanalysis mode
4. **Start Analysis**: Click "Start Analysis" to begin processing
5. **Monitor Progress**: Watch the progress bar and status updates
6. **Download Results**: Once complete, click "Download Results" to access output files

## Output Files

The application generates comprehensive results including:
- Detection visualization images
- Survival time graphs and statistics
- Excel spreadsheets with detailed mite data
- PDF reports with summary information
- Raw data files for further analysis

## Project Structure

```
├── app/                    # GUI application files
│   ├── main_window.py     # Main application window
│   ├── launch.py          # Application launcher
│   └── icons/             # Application icons
├── classes/               # Core detection and analysis classes
├── utils/                 # Utility functions and tools
├── Datasets/              # Sample datasets for testing
├── outputs/               # Analysis results and reports
├── run_app.py             # Simple application launcher
├── start_app.bat          # Windows batch launcher
└── requirements.txt       # Python dependencies
```

## Development

For developers wanting to extend or modify the application:

### Core Components
- `classes/detector.py`: Main detection engine using YOLOv11
- `classes/MiteManager.py`: Mite tracking and status management
- `classes/PlotterModular.py`: Visualization and report generation
- `app/main_window.py`: GUI implementation using CustomTkinter

### Adding New Features
1. Fork the repository
2. Create a feature branch
3. Implement your changes
4. Test thoroughly with sample data
5. Submit a pull request

## Troubleshooting

### Common Issues
- **Import errors**: Ensure all dependencies are installed via `pip install -r requirements.txt`
- **Model loading errors**: Verify that `yolo11n.pt` is present in the project directory
- **Permission errors**: Run with appropriate permissions, especially on Windows
- **Memory issues**: For large image sets, consider processing smaller batches

### Getting Help
- Check the built-in help by clicking "ℹ How to use" in the application
- Review error messages in the status bar
- Consult the console output for detailed debugging information

## Citation

If you use this software in your research, please cite:
"An AI-Based Open-Source Software for Varroa Mite Fall Analysis in Honeybee Colonies"
Giovanni Formato et al., 2023

## License

This project is open source and available under the MIT License.



