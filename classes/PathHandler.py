"""Path handling utilities for the Varroa detector project."""

import os


class PathHandler:
    """Handles path generation and management for output files."""
    
    def __init__(self, output_folder, discobox_run):
        self.discobox_run = discobox_run
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Set the output folder
        if discobox_run:
            self.output_path = os.path.abspath(os.path.join(self.base_dir, "..", "..", output_folder))
        else:
            self.output_path = os.path.abspath(os.path.join(self.base_dir, "..", output_folder))
        
        self.general_summary_path = os.path.abspath(os.path.join(self.output_path, os.pardir))
        
        # Initialize all paths
        self._initialize_paths()
    
    def _initialize_paths(self):
        """Initialize all required paths."""
        self.pdf_path = os.path.join(self.output_path, "recording.pdf")
        self.csv_path = os.path.join(self.output_path, "summary.csv")
        self.frame_path = os.path.join(self.general_summary_path, "frame_0.jpg")
        self.survival_path = os.path.join(self.output_path, "survival.png")
        self.time_survival_path = os.path.join(self.general_summary_path, "survival.png")
        self.distribution_max_diff = os.path.join(self.general_summary_path, 'max_diff.png')
        self.distribution_max_local_diff = os.path.join(self.general_summary_path, 'local_diff.png')
        self.distribution_data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'variabilites.csv')
        self.by_mite_path = os.path.join(self.general_summary_path, 'zones')
        self.excel_by_zones = os.path.join(self.by_mite_path, "mites.xlsx")
        self.excel_by_recording = os.path.join(self.general_summary_path, "recordings_summary.xlsx")
        self.time_file_path = os.path.join(self.general_summary_path, os.pardir, "time_between_recording.txt")

        # Find the settings file in the general summary path
        self.settings_file_path = os.path.join(self.general_summary_path, ".settings.txt")

        # Create necessary directories
        self._create_directories()
    
    def _create_directories(self):
        """Create necessary directories."""
        os.makedirs(self.output_path, exist_ok=True)
        os.makedirs(self.by_mite_path, exist_ok=True)
    
    def get_time_between_recordings(self, time_between_recordings):
        """Get or set time between recordings."""
        if time_between_recordings != 1:
            time_value = time_between_recordings / 60
            self._write_time_to_file(time_value)
            return time_value
        else:
            return self._read_time_from_file()
    
    def _write_time_to_file(self, time_value):
        """Write time value to file."""
        try:
            with open(self.time_file_path, "w") as f:
                f.write(str(time_value))
        except Exception as e:
            print(f"Failed to write time to file: {e}")
    
    def _read_time_from_file(self):
        """Read time value from file."""
        try:
            print("Looking for time in:", self.time_file_path)
            with open(self.time_file_path, 'r') as f:
                content = f.read().strip()
                return float(content)
        except FileNotFoundError:
            print("Time file not found, setting time to 1 minute")
            return 1.0
        except Exception as e:
            print(f"Error reading time file: {e}")
            return 1.0
