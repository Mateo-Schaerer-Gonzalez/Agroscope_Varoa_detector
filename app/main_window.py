import tkinter as tk
import customtkinter as ctk
from tkinter import filedialog, messagebox
import os
import sys
import threading
from typing import Optional

# Ensure root of the project is in Python path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from main import predict


class ProgressWindow:
    """Separate window to show progress during analysis"""
    
    def __init__(self, parent):
        self.window = ctk.CTkToplevel(parent)
        self.window.title("Processing...")
        self.window.geometry("400x200")
        self.window.resizable(False, False)
        
        # Center the window
        self.window.transient(parent)
        self.window.grab_set()
        
        # Progress elements
        self.status_label = ctk.CTkLabel(
            self.window, 
            text="Initializing analysis...", 
            font=ctk.CTkFont(size=14)
        )
        self.status_label.pack(pady=20)
        
        self.progress_bar = ctk.CTkProgressBar(self.window, width=300)
        self.progress_bar.pack(pady=10)
        self.progress_bar.set(0)
        
        self.detail_label = ctk.CTkLabel(
            self.window, 
            text="", 
            font=ctk.CTkFont(size=12)
        )
        self.detail_label.pack(pady=10)
        
    def update_status(self, status: str, progress: float = None, detail: str = ""):
        """Update the progress window"""
        self.status_label.configure(text=status)
        if progress is not None:
            self.progress_bar.set(progress)
        if detail:
            self.detail_label.configure(text=detail)
        self.window.update()
    
    def close(self):
        """Close the progress window"""
        self.window.destroy()


class VarroaDetectorApp:
    """Main application window for Varroa Detector"""
    
    def __init__(self):
        # Configure theme
        ctk.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
        ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"
        
        # Main window setup
        self.root = ctk.CTk()
        self.root.title("Varroa Detector - Agroscope")
        self.root.geometry("900x700")
        self.root.minsize(700, 600)
        
        # Set icon if available
        icon_path = os.path.join(os.path.dirname(__file__), "icons", "app_icon.ico")
        if os.path.exists(icon_path):
            self.root.iconbitmap(icon_path)
        
        # Variables
        self.selected_folder: Optional[str] = None
        self.analysis_name: str = ""
        self.results_ready: bool = False
        self.output_folder: str = ""
        
        self.setup_ui()
        
    def setup_ui(self):
        """Set up the user interface"""
        
        # Title
        title_label = ctk.CTkLabel(
            self.root, 
            text="Varroa Mite Detection System", 
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title_label.pack(pady=(30, 10))
        
        subtitle_label = ctk.CTkLabel(
            self.root, 
            text="Automated detection and analysis of Varroa mites", 
            font=ctk.CTkFont(size=16)
        )
        subtitle_label.pack(pady=(0, 30))
        
        # Main content frame
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill="both", expand=True, padx=40, pady=20)
        
        # Input section
        input_section = ctk.CTkFrame(main_frame)
        input_section.pack(fill="x", padx=20, pady=20)
        
        # Folder selection
        folder_label = ctk.CTkLabel(
            input_section, 
            text="Select Image Folder", 
            font=ctk.CTkFont(size=16, weight="bold")
        )
        folder_label.pack(pady=(20, 10))
        
        folder_frame = ctk.CTkFrame(input_section)
        folder_frame.pack(fill="x", padx=20, pady=(0, 10))
        
        self.folder_path_label = ctk.CTkLabel(
            folder_frame, 
            text="No folder selected", 
            font=ctk.CTkFont(size=12)
        )
        self.folder_path_label.pack(side="left", padx=10, pady=10, fill="x", expand=True)
        
        self.browse_button = ctk.CTkButton(
            folder_frame,
            text="Browse",
            width=100,
            command=self.browse_folder
        )
        self.browse_button.pack(side="right", padx=10, pady=10)
        
        # Analysis name input
        name_label = ctk.CTkLabel(
            input_section, 
            text="Analysis Name", 
            font=ctk.CTkFont(size=16, weight="bold")
        )
        name_label.pack(pady=(20, 10))
        
        self.name_entry = ctk.CTkEntry(
            input_section, 
            placeholder_text="Enter analysis name (e.g., 'experiment_1')",
            height=40,
            font=ctk.CTkFont(size=12)
        )
        self.name_entry.pack(fill="x", padx=20, pady=(0, 10))
        
        # Analysis options
        options_label = ctk.CTkLabel(
            input_section, 
            text="Analysis Options", 
            font=ctk.CTkFont(size=16, weight="bold")
        )
        options_label.pack(pady=(20, 10))
        
        options_frame = ctk.CTkFrame(input_section)
        options_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        # Plate configuration
        plate_frame = ctk.CTkFrame(options_frame)
        plate_frame.pack(fill="x", padx=10, pady=10)
        
        plate_label = ctk.CTkLabel(plate_frame, text="Mites per plate:")
        plate_label.pack(side="left", padx=10)
        
        self.plate_var = ctk.StringVar(value="1")
        self.plate_combobox = ctk.CTkComboBox(
            plate_frame,
            values=["1", "2"],
            variable=self.plate_var,
            width=100
        )
        self.plate_combobox.pack(side="right", padx=10, pady=5)
        
        # Reanalyze option
        self.reanalyze_var = ctk.BooleanVar()
        self.reanalyze_checkbox = ctk.CTkCheckBox(
            options_frame,
            text="Reanalyze existing data",
            variable=self.reanalyze_var
        )
        self.reanalyze_checkbox.pack(padx=10, pady=5, anchor="w")
        
        # Action buttons
        button_frame = ctk.CTkFrame(main_frame)
        button_frame.pack(fill="x", padx=20, pady=20)
        
        self.analyze_button = ctk.CTkButton(
            button_frame,
            text="Start Analysis",
            height=50,
            font=ctk.CTkFont(size=16, weight="bold"),
            command=self.start_analysis,
            state="disabled"
        )
        self.analyze_button.pack(side="left", padx=10, pady=20, fill="x", expand=True)
        
        self.download_button = ctk.CTkButton(
            button_frame,
            text="Download Results",
            height=50,
            font=ctk.CTkFont(size=16, weight="bold"),
            command=self.download_results,
            state="disabled"
        )
        self.download_button.pack(side="right", padx=10, pady=20, fill="x", expand=True)
        
        # Status section
        status_section = ctk.CTkFrame(main_frame)
        status_section.pack(fill="x", padx=20, pady=(0, 20))
        
        self.status_label = ctk.CTkLabel(
            status_section, 
            text="Ready - Please select a folder to begin", 
            font=ctk.CTkFont(size=14)
        )
        self.status_label.pack(pady=20)
        
        # Info section
        info_frame = ctk.CTkFrame(main_frame)
        info_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        info_button = ctk.CTkButton(
            info_frame,
            text="ℹ How to use",
            width=100,
            height=30,
            command=self.show_info
        )
        info_button.pack(pady=10)
        
        # Bind events
        self.name_entry.bind("<KeyRelease>", self.validate_inputs)
    
    def show_info(self):
        """Show information dialog about how to use the application"""
        info_text = """Varroa Detector - Usage Instructions

1. SELECT FOLDER: Click 'Browse' to select a folder containing your microscopy images
   - Supported formats: JPG, PNG, BMP, TIFF
   - Images should contain Varroa mites for detection

2. ANALYSIS NAME: Enter a descriptive name for your analysis
   - This will be used to organize your results

3. ANALYSIS OPTIONS:
   - Mites per plate: Select 1 or 2 depending on your setup
   - Reanalyze: Check this to reprocess existing analysis data

4. START ANALYSIS: Click 'Start Analysis' to begin processing
   - The AI will detect mites in your images
   - Progress will be shown in a separate window

5. DOWNLOAD RESULTS: Once complete, click to open the results folder
   - Contains detection images, survival graphs, and Excel reports

Developed by Agroscope for automated Varroa mite detection and analysis."""
        
        info_window = ctk.CTkToplevel(self.root)
        info_window.title("How to Use - Varroa Detector")
        info_window.geometry("600x500")
        info_window.resizable(False, False)
        
        # Center the window
        info_window.transient(self.root)
        
        text_widget = ctk.CTkTextbox(info_window, wrap="word")
        text_widget.pack(fill="both", expand=True, padx=20, pady=20)
        text_widget.insert("1.0", info_text)
        text_widget.configure(state="disabled")  # Make it read-only
        
        close_button = ctk.CTkButton(
            info_window,
            text="Close",
            command=info_window.destroy
        )
        close_button.pack(pady=(0, 20))
        
    def browse_folder(self):
        """Open folder selection dialog"""
        folder = filedialog.askdirectory(
            title="Select folder containing images"
        )
        
        if folder:
            self.selected_folder = folder
            # Show shortened path
            if len(folder) > 60:
                display_path = "..." + folder[-57:]
            else:
                display_path = folder
            self.folder_path_label.configure(text=display_path)
            self.validate_inputs()
    
    def validate_inputs(self, event=None):
        """Validate input fields and enable/disable buttons"""
        folder_selected = bool(self.selected_folder)
        name_entered = bool(self.name_entry.get().strip())
        
        if folder_selected and name_entered:
            self.analyze_button.configure(state="normal")
            self.status_label.configure(text="Ready for analysis")
        else:
            self.analyze_button.configure(state="disabled")
            if not folder_selected:
                self.status_label.configure(text="Please select a folder")
            elif not name_entered:
                self.status_label.configure(text="Please enter an analysis name")
    
    def start_analysis(self):
        """Start the analysis process in a separate thread"""
        if not self.selected_folder or not self.name_entry.get().strip():
            messagebox.showerror("Error", "Please select a folder and enter an analysis name")
            return
        
        self.analysis_name = self.name_entry.get().strip()
        
        # Disable UI elements during analysis
        self.analyze_button.configure(state="disabled")
        self.browse_button.configure(state="disabled")
        self.name_entry.configure(state="disabled")
        self.plate_combobox.configure(state="disabled")
        self.reanalyze_checkbox.configure(state="disabled")
        
        # Start analysis in separate thread
        analysis_thread = threading.Thread(target=self.run_analysis)
        analysis_thread.daemon = True
        analysis_thread.start()
    
    def run_analysis(self):
        """Run the analysis with progress tracking"""
        progress_window = ProgressWindow(self.root)
        
        try:
            progress_window.update_status("Preparing analysis...", 0.1)
            
            # Get parameters
            num_per_plate = int(self.plate_var.get())
            reanalyze = self.reanalyze_var.get()
            
            progress_window.update_status("Initializing detector...", 0.2, "Loading AI model...")
            
            # Check if folder exists and has images
            if not os.path.exists(self.selected_folder):
                raise ValueError("Selected folder does not exist")
            
            # Count image files
            image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif'}
            image_files = []
            for root, dirs, files in os.walk(self.selected_folder):
                for file in files:
                    if any(file.lower().endswith(ext) for ext in image_extensions):
                        image_files.append(file)
            
            if not image_files:
                raise ValueError("No image files found in the selected folder")
            
            progress_window.update_status(
                "Processing images...", 0.4, 
                f"Found {len(image_files)} images"
            )
            
            # Run the prediction
            predict(
                folder_path=self.selected_folder,
                name=self.analysis_name,
                num_per_plate=num_per_plate,
                reanalyze=reanalyze,
                discobox_run=False,
                num_recordings=2,
                count=2
            )
            
            progress_window.update_status("Generating reports...", 0.9, "Creating visualizations...")
            
            # Set output folder
            self.output_folder = os.path.join("outputs")
            if reanalyze:
                # Find the latest reanalysis folder
                reanalysis_folders = [f for f in os.listdir(self.output_folder) 
                                    if f.startswith("reanalysis") and os.path.isdir(os.path.join(self.output_folder, f))]
                if reanalysis_folders:
                    # Sort by number and get the latest
                    latest = max(reanalysis_folders, key=lambda x: int(x.replace("reanalysis", "")))
                    self.output_folder = os.path.join(self.output_folder, latest)
            else:
                self.output_folder = os.path.join(self.output_folder, "results")
            
            progress_window.update_status("Analysis complete!", 1.0, f"Results saved to {self.output_folder}")
            self.results_ready = True
            
            # Update UI on main thread
            self.root.after(0, self.analysis_completed)
            
        except Exception as e:
            error_msg = str(e)
            self.root.after(0, lambda: self.analysis_failed(error_msg))
        finally:
            self.root.after(1000, progress_window.close)  # Keep window open a bit longer to show completion
    
    def analysis_completed(self):
        """Called when analysis is completed successfully"""
        self.status_label.configure(text="Analysis completed successfully!")
        self.download_button.configure(state="normal")
        
        # Re-enable UI elements
        self.browse_button.configure(state="normal")
        self.name_entry.configure(state="normal")
        self.plate_combobox.configure(state="normal")
        self.reanalyze_checkbox.configure(state="normal")
        self.analyze_button.configure(state="normal")
        
        messagebox.showinfo(
            "Success", 
            "Analysis completed successfully!\nYou can now download the results."
        )
    
    def analysis_failed(self, error_msg: str):
        """Called when analysis fails"""
        self.status_label.configure(text="Analysis failed. Please check your inputs.")
        
        # Re-enable UI elements
        self.browse_button.configure(state="normal")
        self.name_entry.configure(state="normal")
        self.plate_combobox.configure(state="normal")
        self.reanalyze_checkbox.configure(state="normal")
        self.analyze_button.configure(state="normal")
        
        messagebox.showerror("Analysis Error", f"Analysis failed:\n{error_msg}")
    
    def download_results(self):
        """Open the results folder for the user"""
        if not self.results_ready:
            messagebox.showerror("Error", "No results available to download")
            return
        
        try:
            # Open the outputs folder
            if os.path.exists(self.output_folder):
                if sys.platform == "win32":
                    os.startfile(self.output_folder)
                elif sys.platform == "darwin":  # macOS
                    os.system(f"open '{self.output_folder}'")
                else:  # Linux
                    os.system(f"xdg-open '{self.output_folder}'")
                    
                messagebox.showinfo(
                    "Results", 
                    f"Results folder opened:\n{self.output_folder}"
                )
            else:
                messagebox.showerror("Error", "Results folder not found")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open results folder:\n{str(e)}")
    
    def run(self):
        """Start the application"""
        self.root.mainloop()


if __name__ == "__main__":
    app = VarroaDetectorApp()
    app.run()
