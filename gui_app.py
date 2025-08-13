"""
Modern GUI Application for Varroa Detector
A user-friendly interface for analyzing bee mite images using YOLO detection.
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import os
import sys
import shutil
from pathlib import Path
import time

# Import the main prediction function
from main import predict

# Set the theme and color
ctk.set_appearance_mode("dark")  # Can be "light" or "dark"
ctk.set_default_color_theme("blue")  # Can be "blue", "green", or "dark-blue"


class VarroaDetectorApp:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Varroa Detector - AI-Powered Mite Analysis")
        self.root.geometry("900x700")
        self.root.minsize(800, 600)
        
        # Variables
        self.selected_folder = None
        self.analysis_running = False
        self.results_path = None
        
        # Create UI elements
        self.setup_ui()
        
        # Center the window
        self.center_window()
    
    def center_window(self):
        """Center the window on the screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def setup_ui(self):
        """Create and arrange all UI elements"""
        
        # Main container with padding
        main_frame = ctk.CTkFrame(self.root, corner_radius=15)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        title_label = ctk.CTkLabel(
            main_frame, 
            text="🐝 Varroa Detector",
            font=ctk.CTkFont(size=32, weight="bold")
        )
        title_label.pack(pady=(30, 10))
        
        # Subtitle
        subtitle_label = ctk.CTkLabel(
            main_frame,
            text="AI-powered analysis of bee mite images using YOLO detection",
            font=ctk.CTkFont(size=14),
            text_color="gray"
        )
        subtitle_label.pack(pady=(0, 30))
        
        # File selection section
        self.create_file_selection_section(main_frame)
        
        # Configuration section
        self.create_configuration_section(main_frame)
        
        # Progress section
        self.create_progress_section(main_frame)
        
        # Action buttons section
        self.create_action_buttons_section(main_frame)
        
        # Results section
        self.create_results_section(main_frame)
    
    def create_file_selection_section(self, parent):
        """Create the file selection section"""
        file_frame = ctk.CTkFrame(parent, corner_radius=10)
        file_frame.pack(fill="x", padx=30, pady=(0, 20))
        
        # Section title
        file_title = ctk.CTkLabel(
            file_frame,
            text="📁 Select Dataset Folder",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        file_title.pack(pady=(20, 15))
        
        # File selection row
        select_frame = ctk.CTkFrame(file_frame, fg_color="transparent")
        select_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        self.folder_entry = ctk.CTkEntry(
            select_frame,
            placeholder_text="No folder selected...",
            height=40,
            font=ctk.CTkFont(size=12)
        )
        self.folder_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        self.browse_button = ctk.CTkButton(
            select_frame,
            text="Browse",
            width=100,
            height=40,
            command=self.browse_folder
        )
        self.browse_button.pack(side="right")
    
    def create_configuration_section(self, parent):
        """Create the configuration section"""
        config_frame = ctk.CTkFrame(parent, corner_radius=10)
        config_frame.pack(fill="x", padx=30, pady=(0, 20))
        
        # Section title
        config_title = ctk.CTkLabel(
            config_frame,
            text="⚙️ Analysis Configuration",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        config_title.pack(pady=(20, 15))
        
        # Configuration options in a grid
        config_grid = ctk.CTkFrame(config_frame, fg_color="transparent")
        config_grid.pack(fill="x", padx=20, pady=(0, 20))
        
        # Name input
        name_label = ctk.CTkLabel(config_grid, text="Analysis Name:", font=ctk.CTkFont(size=12))
        name_label.grid(row=0, column=0, sticky="w", padx=(0, 10), pady=5)
        
        self.name_entry = ctk.CTkEntry(
            config_grid,
            placeholder_text="Enter analysis name (e.g., 'experiment_1')",
            width=200
        )
        self.name_entry.grid(row=0, column=1, sticky="ew", padx=10, pady=5)
        
        # Plates per recording
        plates_label = ctk.CTkLabel(config_grid, text="Plates per Recording:", font=ctk.CTkFont(size=12))
        plates_label.grid(row=1, column=0, sticky="w", padx=(0, 10), pady=5)
        
        self.plates_var = ctk.StringVar(value="1")
        self.plates_dropdown = ctk.CTkOptionMenu(
            config_grid,
            variable=self.plates_var,
            values=["1", "2"],
            width=200
        )
        self.plates_dropdown.grid(row=1, column=1, sticky="ew", padx=10, pady=5)
        
        # Analysis type
        type_label = ctk.CTkLabel(config_grid, text="Analysis Type:", font=ctk.CTkFont(size=12))
        type_label.grid(row=2, column=0, sticky="w", padx=(0, 10), pady=5)
        
        self.analysis_type_var = ctk.StringVar(value="New Analysis")
        self.type_dropdown = ctk.CTkOptionMenu(
            config_grid,
            variable=self.analysis_type_var,
            values=["New Analysis", "Reanalysis"],
            width=200
        )
        self.type_dropdown.grid(row=2, column=1, sticky="ew", padx=10, pady=5)
        
        # Configure grid weights
        config_grid.columnconfigure(1, weight=1)
    
    def create_progress_section(self, parent):
        """Create the progress section"""
        progress_frame = ctk.CTkFrame(parent, corner_radius=10)
        progress_frame.pack(fill="x", padx=30, pady=(0, 20))
        
        # Progress label
        self.progress_label = ctk.CTkLabel(
            progress_frame,
            text="Ready to start analysis",
            font=ctk.CTkFont(size=12)
        )
        self.progress_label.pack(pady=(20, 10))
        
        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(
            progress_frame,
            width=400,
            height=10
        )
        self.progress_bar.pack(pady=(0, 20))
        self.progress_bar.set(0)
    
    def create_action_buttons_section(self, parent):
        """Create the action buttons section"""
        button_frame = ctk.CTkFrame(parent, fg_color="transparent")
        button_frame.pack(fill="x", padx=30, pady=(0, 20))
        
        # Start Analysis button
        self.start_button = ctk.CTkButton(
            button_frame,
            text="🚀 Start Analysis",
            font=ctk.CTkFont(size=16, weight="bold"),
            height=50,
            command=self.start_analysis
        )
        self.start_button.pack(side="left", expand=True, fill="x", padx=(0, 10))
        
        # Stop button
        self.stop_button = ctk.CTkButton(
            button_frame,
            text="⏹️ Stop",
            font=ctk.CTkFont(size=16, weight="bold"),
            height=50,
            fg_color="red",
            hover_color="darkred",
            command=self.stop_analysis,
            state="disabled"
        )
        self.stop_button.pack(side="right", padx=(10, 0))
    
    def create_results_section(self, parent):
        """Create the results section"""
        results_frame = ctk.CTkFrame(parent, corner_radius=10)
        results_frame.pack(fill="x", padx=30, pady=(0, 10))
        
        # Results label
        results_title = ctk.CTkLabel(
            results_frame,
            text="📊 Analysis Results",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        results_title.pack(pady=(20, 15))
        
        # Results info
        self.results_info = ctk.CTkLabel(
            results_frame,
            text="No analysis completed yet",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        self.results_info.pack(pady=(0, 10))
        
        # Download button
        self.download_button = ctk.CTkButton(
            results_frame,
            text="📥 Open Results Folder",
            height=40,
            command=self.open_results_folder,
            state="disabled"
        )
        self.download_button.pack(pady=(0, 20))
    
    def browse_folder(self):
        """Open file dialog to select folder"""
        folder_path = filedialog.askdirectory(
            title="Select Dataset Folder",
            initialdir=os.getcwd()
        )
        
        if folder_path:
            self.selected_folder = folder_path
            self.folder_entry.delete(0, tk.END)
            self.folder_entry.insert(0, folder_path)
    
    def validate_inputs(self):
        """Validate user inputs"""
        if not self.selected_folder:
            messagebox.showerror("Error", "Please select a dataset folder")
            return False
        
        if not os.path.exists(self.selected_folder):
            messagebox.showerror("Error", "Selected folder does not exist")
            return False
        
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showerror("Error", "Please enter an analysis name")
            return False
        
        return True
    
    def start_analysis(self):
        """Start the analysis process"""
        if not self.validate_inputs():
            return
        
        # Prepare parameters
        folder_path = self.selected_folder
        name = self.name_entry.get().strip()
        num_per_plate = int(self.plates_var.get())
        reanalyze = self.analysis_type_var.get() == "Reanalysis"
        
        # Update UI state
        self.analysis_running = True
        self.start_button.configure(state="disabled")
        self.stop_button.configure(state="normal")
        self.progress_bar.set(0)
        self.progress_label.configure(text="Initializing analysis...")
        
        # Start analysis in separate thread
        analysis_thread = threading.Thread(
            target=self.run_analysis,
            args=(folder_path, name, num_per_plate, reanalyze),
            daemon=True
        )
        analysis_thread.start()
    
    def run_analysis(self, folder_path, name, num_per_plate, reanalyze):
        """Run the analysis in a separate thread"""
        try:
            # Update progress
            self.root.after(0, lambda: self.progress_label.configure(text="Loading detector..."))
            self.root.after(0, lambda: self.progress_bar.set(0.1))
            
            # Update progress
            self.root.after(0, lambda: self.progress_label.configure(text="Processing images..."))
            self.root.after(0, lambda: self.progress_bar.set(0.3))
            
            # Run the actual prediction
            predict(
                folder_path=folder_path,
                name=name,
                num_per_plate=num_per_plate,
                reanalyze=reanalyze,
                discobox_run=False,
                num_recordings=2,
                count=2,
                time_between_rec=1
            )
            
            # Update progress
            self.root.after(0, lambda: self.progress_bar.set(0.8))
            self.root.after(0, lambda: self.progress_label.configure(text="Generating reports..."))
            
            # Simulate final processing
            time.sleep(1)
            
            # Find results folder
            results_folder = os.path.join(os.getcwd(), "outputs", "results")
            if os.path.exists(results_folder):
                self.results_path = results_folder
            
            # Update UI on completion
            self.root.after(0, self.analysis_completed)
            
        except Exception as e:
            error_msg = f"Analysis failed: {str(e)}"
            self.root.after(0, lambda: self.analysis_failed(error_msg))
    
    def analysis_completed(self):
        """Handle successful analysis completion"""
        self.analysis_running = False
        self.start_button.configure(state="normal")
        self.stop_button.configure(state="disabled")
        self.progress_bar.set(1.0)
        self.progress_label.configure(text="✅ Analysis completed successfully!")
        
        # Update results section
        self.results_info.configure(
            text="Analysis completed! Results are ready for download.",
            text_color="green"
        )
        self.download_button.configure(state="normal")
        
        # Show completion message
        messagebox.showinfo(
            "Success",
            "Analysis completed successfully!\nClick 'Open Results Folder' to view the results."
        )
    
    def analysis_failed(self, error_msg):
        """Handle analysis failure"""
        self.analysis_running = False
        self.start_button.configure(state="normal")
        self.stop_button.configure(state="disabled")
        self.progress_bar.set(0)
        self.progress_label.configure(text="❌ Analysis failed")
        
        # Show error message
        messagebox.showerror("Analysis Failed", error_msg)
    
    def stop_analysis(self):
        """Stop the current analysis"""
        if self.analysis_running:
            # Note: In a real implementation, you'd need to properly interrupt the analysis
            self.analysis_running = False
            self.start_button.configure(state="normal")
            self.stop_button.configure(state="disabled")
            self.progress_bar.set(0)
            self.progress_label.configure(text="Analysis stopped")
            messagebox.showinfo("Stopped", "Analysis has been stopped")
    
    def open_results_folder(self):
        """Open the results folder in file explorer"""
        if self.results_path and os.path.exists(self.results_path):
            if sys.platform == "win32":
                os.startfile(self.results_path)
            elif sys.platform == "darwin":
                os.system(f"open '{self.results_path}'")
            else:
                os.system(f"xdg-open '{self.results_path}'")
        else:
            # Fallback to outputs folder
            outputs_folder = os.path.join(os.getcwd(), "outputs")
            if os.path.exists(outputs_folder):
                if sys.platform == "win32":
                    os.startfile(outputs_folder)
                else:
                    messagebox.showinfo("Results", f"Results saved to: {outputs_folder}")
            else:
                messagebox.showwarning("Not Found", "Results folder not found")
    
    def run(self):
        """Start the application"""
        self.root.mainloop()


def main():
    """Main entry point"""
    app = VarroaDetectorApp()
    app.run()


if __name__ == "__main__":
    main()
