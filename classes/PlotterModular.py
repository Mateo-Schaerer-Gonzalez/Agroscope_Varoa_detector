"""Modular Plotter class for the Varroa detector project."""

import os
import cv2
import math
import pandas as pd
import matplotlib.pyplot as plt
from classes.mite import Mite
from classes.PlotGenerator import PlotGenerator
from classes.ExcelGenerator import ExcelGenerator
from classes.PDFGenerator import PDFGenerator
from classes.PathHandler import PathHandler


class PlotterModular:
    """
    Modular plotter that delegates responsibilities to specialized classes.
    This replaces the monolithic Plotter class with better separation of concerns.
    """
    
    def __init__(self, stage, output_folder, discobox_run):
        # Guard clauses
        if not stage:
            raise ValueError("Stage must be provided")
        if not output_folder:
            raise ValueError("Output folder must be provided")
        
        self.stage = stage
        
        # Initialize specialized handlers
        self.path_handler = PathHandler(output_folder, discobox_run)
        self.plot_generator = PlotGenerator(stage.img_size, self.stage.settings)
        self.excel_generator = ExcelGenerator(self.stage.settings)
        self.pdf_generator = PDFGenerator(self.stage.settings)

    
    
    def save_frame0_detection(self, image, thickness=2):
        """Save the first frame with detection overlays."""
        # Guard clause
        if image is None:
            raise ValueError("Image must be provided")
        
        # Draw zones on the image
        for zone in self.stage.zones:
            zone.draw(image, thickness=thickness)
        
        cv2.imwrite(self.path_handler.frame_path, image)
        print(f"Image saved to: {self.path_handler.frame_path}")
    
    def make_survival_graph(self, recording_number):
        """Create and save survival graph for a recording."""
        # Guard clauses
        if recording_number <= 0:
            raise ValueError("Recording number must be greater than 0")
        
        if self.stage.data.empty or self.stage.mite_data.empty:
            self.stage.reset()
            raise ValueError("No mites found in the dataset")
        
        try:
            fig = self.plot_generator.create_survival_graph(
                self.stage.data, self.stage.mite_data, recording_number)
            fig.savefig(self.path_handler.survival_path)
            plt.close(fig)
            print(f"Survival graph saved to: {self.path_handler.survival_path}")
            
        except Exception as e:
            print(f"Error creating survival graph: {e}")
            raise
    
    def make_survival_time_graph(self):
        """Create and save survival over time graph."""
        if self.stage.data.empty:
            self.stage.reset()
            raise ValueError("No mites found in the dataset")
        
        try:
            fig = self.plot_generator.create_survival_time_graph(
                self.stage.data
            )
            fig.savefig(self.path_handler.time_survival_path)
            plt.close(fig)
            print(f"Time survival graph saved to: {self.path_handler.time_survival_path}")
            
        except Exception as e:
            print(f"Error creating time survival graph: {e}")
            raise
    
    def distribution_graph(self):
        """Create distribution graphs for max and local differences."""
        try:
            df = pd.read_csv(self.path_handler.distribution_data_path)
            
            if df.empty:
                raise ValueError("No distribution data found")
            
            # Max difference distribution
            self.plot_generator.create_distribution_graph(
                df, 'max_diff', 'Histogram of Max Difference', 'Max Difference',
                self.path_handler.distribution_max_diff
            )
            
            # Local difference distribution
            self.plot_generator.create_distribution_graph(
                df, 'local_diff', 'Histogram of Local Difference', 'Local Difference',
                self.path_handler.distribution_max_local_diff
            )
            
        except Exception as e:
            print(f"Error creating distribution graphs: {e}")
            raise
    
    def plot_variability_by_mite(self):
        """Create variability plots for each mite by zone."""
        # Guard clause
        if self.stage.mite_data.empty:
            raise ValueError("No mite data available for plotting")
        
        try:
            # Ensure data is sorted properly
            df = self.stage.mite_data.sort_values(by=['zone ID', 'mite ID', 'recording'])
            
            # Create zones folder if not already exists
            zones_folder = os.path.join(self.path_handler.by_mite_path, "zones")
            os.makedirs(zones_folder, exist_ok=True)
            
            # Set threshold and consistent y-limits
            threshold = Mite.threshold
            y_min = df[['max diff', 'local diff']].min().min() - 0.1
            y_max = df[['max diff', 'local diff']].max().max() + 0.1
            
            # Process each zone
            self._create_zone_plots(df, threshold, y_min, y_max, zones_folder)
            
        except Exception as e:
            print(f"Error plotting variability by mite: {e}")
            raise
    
    def _create_zone_plots(self, df, threshold, y_min, y_max, zones_folder):
        """Create plots for each zone."""
        zones = df['zone ID'].unique()
        
        for zone in zones:
            zone_df = df[df['zone ID'] == zone]
            
            if zone_df.empty:
                continue
            
            try:
                fig = self.plot_generator.create_mite_variability_plot(
                    zone_df, zone,
                    threshold, y_min, y_max
                )
                
                if fig:
                    save_path = os.path.join(zones_folder, f'{zone}.png')
                    fig.savefig(save_path)
                    plt.close(fig)
                    print(f"Plotting zone: {zone}")
                
            except Exception as e:
                print(f"Error plotting zone {zone}: {e}")
                continue
    
    def create_recording_pdf(self, recording_count):
        """Create PDF with recording data and graphs."""
        # Guard clause
        if recording_count <= 0:
            raise ValueError("Recording count must be greater than 0")
        
        try:
            # Create the survival graph for this recording
            self.make_survival_graph(recording_count)
            
            # For now, just include the survival graph
            # Could be extended to include more figures
            figures = []
            
            # Load the saved survival graph
            if os.path.exists(self.path_handler.survival_path):
                # Since we can't directly pass matplotlib figures,
                # we'll recreate the figure for PDF
                fig = self.plot_generator.create_survival_graph(
                    self.stage.data, self.stage.mite_data, recording_count
                )
                figures.append(fig)
            
            if figures:
                self.pdf_generator.create_recording_pdf(figures, self.path_handler.pdf_path)
                
                # Clean up figures
                for fig in figures:
                    plt.close(fig)
            
        except Exception as e:
            print(f"Error creating recording PDF: {e}")
            raise
    
    def excel_summary_recordings(self):
        """Create Excel summary with recordings data."""
        try:
            recordings_base_path = os.path.dirname(self.path_handler.excel_by_recording)
            self.excel_generator.create_recordings_summary(
                self.stage.data,
                self.path_handler.time_survival_path,
                self.path_handler.excel_by_recording,
                recordings_base_path)

        except ValueError as e:
            print(f"Excel generation error: {e}")
            self.stage.reset()
            raise
        except Exception as e:
            print(f"Unexpected error in Excel generation: {e}")
            raise
    
    def excel_summary_mites(self):
        """Create Excel summary with mite status data."""
        try:
            zones = self.stage.mite_data['zone ID'].unique()
            self.excel_generator.create_mites_summary(
                self.stage.mite_data,
                zones,
                self.path_handler.by_mite_path,
                self.path_handler.excel_by_zones,
                self.path_handler.frame_path,
                self.stage.zones
            )
            
        except ValueError as e:
            print(f"Mites Excel generation error: {e}")
            self.stage.reset()
            raise
        except Exception as e:
            print(f"Unexpected error in mites Excel generation: {e}")
            raise


# For backwards compatibility, create an alias
class Plotter(PlotterModular):
    """Backwards compatibility alias for the modular plotter."""
    pass
