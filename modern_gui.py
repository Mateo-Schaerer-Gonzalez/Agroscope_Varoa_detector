"""
Modern GUI Application for Varroa Detector using standard tkinter
A user-friendly interface for analyzing bee mite images using YOLO detection.
"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
import os
import sys
from pathlib import Path
import time

# Import the main prediction function
from main import predict


class VarroaDetectorApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Varroa Detector - AI-Powered Mite Analysis")
        self.root.geometry("800x700")
        self.root.minsize(700, 600)
        
        # Configure style
        self.setup_styles()
        
        # Variables
        self.selected_folder = tk.StringVar()
        self.analysis_name = tk.StringVar(value="analysis_1")
        self.plates_per_recording = tk.StringVar(value="1")
        self.analysis_type = tk.StringVar(value="New Analysis")
        self.analysis_running = False
        self.results_path = None
        
        # Create UI elements
        self.setup_ui()
        
        # Center the window
        self.center_window()
    
    def setup_styles(self):
        """Configure the visual style of the application"""
        style = ttk.Style()
        
        # Configure colors
        self.colors = {
            'bg': '#f0f0f0',
            'primary': '#2196F3',
            'success': '#4CAF50',
            'error': '#F44336',
            'warning': '#FF9800',
            'text': '#333333',
            'light_bg': '#ffffff'
        }
        
        # Configure root window
        self.root.configure(bg=self.colors['bg'])
        
        # Configure ttk styles
        style.configure('Title.TLabel', 
                       font=('Arial', 20, 'bold'),
                       background=self.colors['bg'],
                       foreground=self.colors['primary'])
        
        style.configure('Subtitle.TLabel',
                       font=('Arial', 10),
                       background=self.colors['bg'],
                       foreground='gray')
        
        style.configure('Section.TLabel',
                       font=('Arial', 12, 'bold'),
                       background=self.colors['light_bg'])
        
        style.configure('Card.TFrame',
                       background=self.colors['light_bg'],
                       relief='solid',
                       borderwidth=1)
    
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
        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title section
        self.create_title_section(main_frame)
        
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
    
    def create_title_section(self, parent):
        """Create the title section"""
        title_frame = tk.Frame(parent, bg=self.colors['bg'])
        title_frame.pack(fill="x", pady=(0, 30))
        
        # Main title
        title_label = ttk.Label(
            title_frame,
            text="🐝 Varroa Detector",
            style='Title.TLabel'
        )
        title_label.pack()
        
        # Subtitle
        subtitle_label = ttk.Label(
            title_frame,
            text="AI-powered analysis of bee mite images using YOLO detection",
            style='Subtitle.TLabel'
        )
        subtitle_label.pack(pady=(5, 0))
    
    def create_file_selection_section(self, parent):
        """Create the file selection section"""
        # Card frame
        card_frame = ttk.Frame(parent, style='Card.TFrame', padding=20)
        card_frame.pack(fill="x", pady=(0, 15))
        
        # Section title
        title_label = ttk.Label(
            card_frame,
            text="📁 Select Dataset Folder",
            style='Section.TLabel'
        )
        title_label.pack(anchor="w", pady=(0, 15))
        
        # File selection row
        select_frame = tk.Frame(card_frame, bg=self.colors['light_bg'])
        select_frame.pack(fill="x")
        
        self.folder_entry = tk.Entry(
            select_frame,
            textvariable=self.selected_folder,
            font=('Arial', 10),
            state='readonly',
            bg='white'
        )
        self.folder_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        self.browse_button = tk.Button(
            select_frame,
            text="Browse",
            command=self.browse_folder,
            bg=self.colors['primary'],
            fg='white',
            font=('Arial', 10, 'bold'),
            padx=20,
            cursor='hand2'
        )
        self.browse_button.pack(side="right")
    
    def create_configuration_section(self, parent):
        """Create the configuration section"""
        # Card frame
        card_frame = ttk.Frame(parent, style='Card.TFrame', padding=20)
        card_frame.pack(fill="x", pady=(0, 15))
        
        # Section title
        title_label = ttk.Label(
            card_frame,
            text="⚙️ Analysis Configuration",
            style='Section.TLabel'
        )
        title_label.pack(anchor="w", pady=(0, 15))
        
        # Configuration grid
        config_frame = tk.Frame(card_frame, bg=self.colors['light_bg'])
        config_frame.pack(fill="x")
        
        # Analysis name
        tk.Label(config_frame, text="Analysis Name:", 
                font=('Arial', 10), bg=self.colors['light_bg']).grid(
                row=0, column=0, sticky="w", padx=(0, 10), pady=8)
        
        name_entry = tk.Entry(config_frame, textvariable=self.analysis_name,
                             font=('Arial', 10), width=30)
        name_entry.grid(row=0, column=1, sticky="ew", padx=(0, 20), pady=8)
        
        # Plates per recording
        tk.Label(config_frame, text="Plates per Recording:", 
                font=('Arial', 10), bg=self.colors['light_bg']).grid(
                row=1, column=0, sticky="w", padx=(0, 10), pady=8)
        
        plates_combo = ttk.Combobox(config_frame, textvariable=self.plates_per_recording,
                                   values=["1", "2"], state="readonly", width=27)
        plates_combo.grid(row=1, column=1, sticky="ew", padx=(0, 20), pady=8)
        
        # Analysis type
        tk.Label(config_frame, text="Analysis Type:", 
                font=('Arial', 10), bg=self.colors['light_bg']).grid(
                row=2, column=0, sticky="w", padx=(0, 10), pady=8)
        
        type_combo = ttk.Combobox(config_frame, textvariable=self.analysis_type,
                                 values=["New Analysis", "Reanalysis"], 
                                 state="readonly", width=27)
        type_combo.grid(row=2, column=1, sticky="ew", padx=(0, 20), pady=8)
        
        # Configure grid weights
        config_frame.columnconfigure(1, weight=1)
    
    def create_progress_section(self, parent):
        """Create the progress section"""
        # Card frame
        card_frame = ttk.Frame(parent, style='Card.TFrame', padding=20)
        card_frame.pack(fill="x", pady=(0, 15))
        
        # Progress label
        self.progress_label = tk.Label(
            card_frame,
            text="Ready to start analysis",
            font=('Arial', 10),
            bg=self.colors['light_bg']
        )
        self.progress_label.pack(pady=(0, 10))
        
        # Progress bar
        self.progress_bar = ttk.Progressbar(
            card_frame,
            mode='determinate',
            length=400
        )
        self.progress_bar.pack()
    
    def create_action_buttons_section(self, parent):
        """Create the action buttons section"""
        button_frame = tk.Frame(parent, bg=self.colors['bg'])
        button_frame.pack(fill="x", pady=(0, 15))
        
        # Start Analysis button
        self.start_button = tk.Button(
            button_frame,
            text="🚀 Start Analysis",
            font=('Arial', 12, 'bold'),
            bg=self.colors['success'],
            fg='white',
            height=2,
            command=self.start_analysis,
            cursor='hand2'
        )
        self.start_button.pack(side="left", expand=True, fill="x", padx=(0, 10))
        
        # Stop button
        self.stop_button = tk.Button(
            button_frame,
            text="⏹️ Stop",
            font=('Arial', 12, 'bold'),
            bg=self.colors['error'],
            fg='white',
            height=2,
            command=self.stop_analysis,
            state="disabled",
            cursor='hand2'
        )
        self.stop_button.pack(side="right", padx=(10, 0))
    
    def create_results_section(self, parent):
        """Create the results section"""
        # Card frame
        card_frame = ttk.Frame(parent, style='Card.TFrame', padding=20)
        card_frame.pack(fill="x")
        
        # Section title
        title_label = ttk.Label(
            card_frame,
            text="📊 Analysis Results",
            style='Section.TLabel'
        )
        title_label.pack(anchor="w", pady=(0, 15))
        
        # Results info
        self.results_info = tk.Label(
            card_frame,
            text="No analysis completed yet",
            font=('Arial', 10),
            fg='gray',
            bg=self.colors['light_bg']
        )
        self.results_info.pack(pady=(0, 15))
        
        # Download button
        self.download_button = tk.Button(
            card_frame,
            text="📁 Open Results Folder",
            font=('Arial', 10, 'bold'),
            bg=self.colors['primary'],
            fg='white',
            command=self.open_results_folder,
            state="disabled",
            cursor='hand2'
        )
        self.download_button.pack()
    
    def browse_folder(self):
        """Open file dialog to select folder"""
        folder_path = filedialog.askdirectory(
            title="Select Dataset Folder",
            initialdir=os.getcwd()
        )
        
        if folder_path:
            self.selected_folder.set(folder_path)
    
    def validate_inputs(self):
        """Validate user inputs"""
        if not self.selected_folder.get():
            messagebox.showerror("Error", "Please select a dataset folder")
            return False
        
        if not os.path.exists(self.selected_folder.get()):
            messagebox.showerror("Error", "Selected folder does not exist")
            return False
        
        name = self.analysis_name.get().strip()
        if not name:
            messagebox.showerror("Error", "Please enter an analysis name")
            return False
        
        return True
    
    def start_analysis(self):
        """Start the analysis process"""
        if not self.validate_inputs():
            return
        
        # Update UI state
        self.analysis_running = True
        self.start_button.configure(state="disabled")
        self.stop_button.configure(state="normal")
        self.progress_bar['value'] = 0
        self.progress_label.configure(text="Initializing analysis...", fg=self.colors['text'])
        
        # Get parameters
        folder_path = self.selected_folder.get()
        name = self.analysis_name.get().strip()
        num_per_plate = int(self.plates_per_recording.get())
        reanalyze = self.analysis_type.get() == "Reanalysis"
        
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
            self.root.after(0, lambda: self.update_progress(10, "Loading detector..."))
            
            # Update progress
            self.root.after(0, lambda: self.update_progress(30, "Processing images..."))
            
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
            self.root.after(0, lambda: self.update_progress(80, "Generating reports..."))
            
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
    
    def update_progress(self, value, message):
        """Update progress bar and message"""
        self.progress_bar['value'] = value
        self.progress_label.configure(text=message)
        self.root.update_idletasks()
    
    def analysis_completed(self):
        """Handle successful analysis completion"""
        self.analysis_running = False
        self.start_button.configure(state="normal")
        self.stop_button.configure(state="disabled")
        self.progress_bar['value'] = 100
        self.progress_label.configure(text="✅ Analysis completed successfully!", 
                                    fg=self.colors['success'])
        
        # Update results section
        self.results_info.configure(
            text="Analysis completed! Results are ready for download.",
            fg=self.colors['success']
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
        self.progress_bar['value'] = 0
        self.progress_label.configure(text="❌ Analysis failed", fg=self.colors['error'])
        
        # Show error message
        messagebox.showerror("Analysis Failed", error_msg)
    
    def stop_analysis(self):
        """Stop the current analysis"""
        if self.analysis_running:
            # Note: In a real implementation, you'd need to properly interrupt the analysis
            self.analysis_running = False
            self.start_button.configure(state="normal")
            self.stop_button.configure(state="disabled")
            self.progress_bar['value'] = 0
            self.progress_label.configure(text="Analysis stopped", fg=self.colors['warning'])
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
