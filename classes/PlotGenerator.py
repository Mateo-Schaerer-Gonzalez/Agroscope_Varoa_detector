"""Plot generation utilities for the Varroa detector project."""

import matplotlib
matplotlib.use('Agg')  # Must be set before importing pyplot

import matplotlib.pyplot as plt
import pandas as pd
import math
from classes.mite import Mite


class PlotGenerator:
    """Handles the generation of various plot types."""
    
    def __init__(self, img_size=(15, 10)):
        self.img_size = img_size
    
    def create_survival_graph(self, summary_data, mite_data, recording_number):
        """Create survival graph for a specific recording."""
        # Guard clauses
        if summary_data.empty or mite_data.empty:
            raise ValueError("No data available for plotting")
        
        # Filter both datasets by the given recording number
        summary_data = summary_data[summary_data['recording'] == recording_number]
        mite_data = mite_data[mite_data['recording'] == recording_number]
        
        if summary_data.empty or mite_data.empty:
            raise ValueError(f"No data found for recording {recording_number}")
        
        # Create a figure with 2 subplots side by side
        fig, axes = plt.subplots(1, 2, figsize=(12, 6))
        
        # Subplot 1: Histogram of max pixel difference
        axes[0].hist(mite_data['max diff'], bins=20, color="steelblue", edgecolor="black")
        axes[0].set_title("Distribution of Mite Max Pixel Difference")
        axes[0].set_xlabel("Max Pixel Difference")
        axes[0].set_ylabel("Frequency")
        axes[0].grid(True)
        axes[0].axvline(Mite.threshold, color='red', linestyle='--', linewidth=2)
        
        # Subplot 2: Bar chart of survival rates
        axes[1].bar(summary_data['zone ID'], summary_data['Survival %'], 
                   color="mediumseagreen", edgecolor="black")
        axes[1].set_title("Survival Rate by Zone")
        axes[1].set_xlabel("Zone ID")
        axes[1].set_ylabel("Survival %")
        axes[1].set_ylim(0, 100)
        axes[1].grid(True)
        
        plt.tight_layout()
        return fig
    
    def create_survival_time_graph(self, df, time_between_recording):
        """Create survival over time graph."""
        if df.empty:
            raise ValueError("No data available for time series plotting")
        
        plt.figure(figsize=(10, 6))
        
        for zone in df['zone ID'].unique():
            zone_data = df[df['zone ID'] == zone]
            plt.plot(
                zone_data['recording'] * time_between_recording,
                zone_data['Survival %'],
                marker='o',
                label=f'{zone}'
            )
        
        plt.xlabel('Time [min]')
        plt.ylabel('Survival %')
        plt.title('Survival Per Zone Over Time')
        plt.legend(title='Zone ID')
        plt.grid(True)
        plt.tight_layout()
        
        return plt.gcf()
    
    def create_distribution_graph(self, df, column, title, xlabel, save_path):
        """Create distribution histogram grouped by ground truth."""
        if df.empty:
            raise ValueError("No data available for distribution plotting")
        
        plt.figure(figsize=self.img_size)
        
        for alive_status, group in df.groupby('Ground_truth'):
            plt.hist(group[column], bins=30, alpha=0.6, label=alive_status)
        
        plt.xlabel(xlabel)
        plt.ylabel('Frequency')
        plt.title(title)
        plt.legend()
        plt.savefig(save_path)
        plt.close()
    
    def create_mite_variability_plot(self, zone_df, zone, time_between_recording, 
                                   threshold, y_min, y_max):
        """Create variability plot for mites in a specific zone."""
        mites = zone_df['mite ID'].unique()
        num_mites = len(mites)
        
        if num_mites == 0:
            return None
        
        # Arrange in two columns
        ncols = 2
        nrows = math.ceil(num_mites / ncols)
        
        fig, axes = plt.subplots(nrows=nrows, ncols=ncols, 
                               figsize=(14, 4 * nrows), sharex=True, sharey=True)
        
        # Handle single subplot case
        if num_mites == 1:
            axes = [axes] if not isinstance(axes, list) else axes
        else:
            axes = axes.flatten() if nrows > 1 else [axes] if ncols == 1 else axes.flatten()
        
        fig.suptitle(f"Zone: {zone}", fontsize=18)
        
        for i, mite_id in enumerate(mites):
            ax = axes[i]
            mite_df = zone_df[zone_df['mite ID'] == mite_id]
            
            # Background shading
            ax.axhspan(y_min, threshold, color='red', alpha=0.2)
            ax.axhspan(threshold, y_max, color='green', alpha=0.2)
            
            # Plot data
            ax.plot(mite_df['recording'] * time_between_recording, 
                   mite_df['max diff'], marker='o', label='Max Diff')
            ax.plot(mite_df['recording'] * time_between_recording, 
                   mite_df['local diff'], marker='x', label='Local Diff')
            
            ax.set_title(f"Mite: {mite_id}")
            ax.set_ylabel("Diff")
            ax.set_xlabel("Time [min]")
            ax.set_ylim(y_min, y_max)
            ax.grid(True)
            ax.legend()
        
        # Hide unused subplots
        for j in range(len(mites), len(axes)):
            fig.delaxes(axes[j])
        
        plt.tight_layout(rect=[0, 0.03, 1, 0.95])
        return fig
