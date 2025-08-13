"""
Modern GUI Application for Varroa Detector with enhanced UI design
Features: Modern styling, drag-and-drop, ZIP downloads
"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk, font
import threading
import os
import sys
from pathlib import Path
import time
import zipfile
import shutil
from datetime import datetime
import tempfile


class ModernVarroaDetectorApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Varroa Detector - AI-Powered Mite Analysis")
        self.root.geometry("1000x800")
        self.root.minsize(900, 700)
        
        # Configure modern styling
        self.setup_modern_styles()
        
        # Variables
        self.selected_folder = tk.StringVar()
        self.analysis_name = tk.StringVar(value="analysis_1")
        self.plates_per_recording = tk.StringVar(value="1")
        self.time_between_recordings = tk.StringVar(value="1")
        self.analysis_running = False
        self.results_path = None
        
        # Create UI elements
        self.setup_ui()
        
        # Center the window
        self.center_window()
        
        # Setup drag and drop
        self.setup_drag_drop()
    
    def setup_modern_styles(self):
        """Configure modern visual styling"""
        # Modern color scheme
        self.colors = {
            'bg_primary': '#1e1e2e',      # Dark background
            'bg_secondary': '#313244',     # Secondary dark
            'bg_tertiary': '#45475a',      # Tertiary dark
            'accent': '#89b4fa',           # Blue accent
            'accent_hover': '#74c7ec',     # Light blue
            'success': '#a6e3a1',          # Green
            'warning': '#fab387',          # Orange
            'error': '#f38ba8',            # Red
            'text_primary': '#cdd6f4',     # Light text
            'text_secondary': '#a6adc8',   # Secondary text
            'text_muted': '#6c7086',       # Muted text
            'surface': '#383a59',          # Surface color
            'gradient_start': '#89b4fa',
            'gradient_end': '#cba6f7'
        }
        
        # Configure root
        self.root.configure(bg=self.colors['bg_primary'])
        
        # Modern fonts
        self.fonts = {
            'title': ('Segoe UI', 28, 'bold'),
            'heading': ('Segoe UI', 16, 'bold'),
            'subheading': ('Segoe UI', 12, 'bold'),
            'body': ('Segoe UI', 10),
            'small': ('Segoe UI', 9)
        }
        
        # Configure ttk styles for modern look
        style = ttk.Style()
        
        # Configure modern button style
        style.configure('Modern.TButton',
                       background=self.colors['accent'],
                       foreground='white',
                       borderwidth=0,
                       focuscolor='none',
                       padding=(20, 10))
        
        style.map('Modern.TButton',
                 background=[('active', self.colors['accent_hover']),
                           ('pressed', self.colors['accent'])])
        
        # Configure modern frame style
        style.configure('Card.TFrame',
                       background=self.colors['bg_secondary'],
                       borderwidth=1,
                       relief='solid')
        
        # Configure modern progressbar
        style.configure('Modern.Horizontal.TProgressbar',
                       background=self.colors['accent'],
                       troughcolor=self.colors['bg_tertiary'],
                       borderwidth=0,
                       lightcolor=self.colors['accent'],
                       darkcolor=self.colors['accent'])
    
    def center_window(self):
        """Center the window on the screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def setup_ui(self):
        """Create and arrange all UI elements with modern design"""
        
        # Create main container with scrolling capability
        main_canvas = tk.Canvas(self.root, bg=self.colors['bg_primary'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=main_canvas.yview)
        scrollable_frame = tk.Frame(main_canvas, bg=self.colors['bg_primary'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: main_canvas.configure(scrollregion=main_canvas.bbox("all"))
        )
        
        main_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        main_canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack canvas and scrollbar
        main_canvas.pack(side="left", fill="both", expand=True, padx=20, pady=20)
        scrollbar.pack(side="right", fill="y")
        
        # Title section
        self.create_title_section(scrollable_frame)
        
        # Drag and drop section
        self.create_drag_drop_section(scrollable_frame)
        
        # Configuration section
        self.create_configuration_section(scrollable_frame)
        
        # Progress section
        self.create_progress_section(scrollable_frame)
        
        # Action buttons section
        self.create_action_buttons_section(scrollable_frame)
        
        # Results section
        self.create_results_section(scrollable_frame)
        
        # Bind mousewheel to canvas
        def _on_mousewheel(event):
            main_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        main_canvas.bind_all("<MouseWheel>", _on_mousewheel)
    
    def create_title_section(self, parent):
        """Create modern title section with gradient effect"""
        title_frame = tk.Frame(parent, bg=self.colors['bg_primary'], height=120)
        title_frame.pack(fill="x", pady=(0, 40))
        title_frame.pack_propagate(False)
        
        # Main title with modern styling
        title_label = tk.Label(
            title_frame,
            text="🐝 Varroa Detector",
            font=self.fonts['title'],
            bg=self.colors['bg_primary'],
            fg=self.colors['gradient_end']
        )
        title_label.pack(pady=(20, 5))
        
        # Subtitle with better styling
        subtitle_label = tk.Label(
            title_frame,
            text="AI-powered analysis of bee mite images using advanced YOLO detection",
            font=self.fonts['body'],
            bg=self.colors['bg_primary'],
            fg=self.colors['text_secondary']
        )
        subtitle_label.pack(pady=(0, 10))
        
        # Status indicator
        self.status_label = tk.Label(
            title_frame,
            text="● Ready",
            font=self.fonts['small'],
            bg=self.colors['bg_primary'],
            fg=self.colors['success']
        )
        self.status_label.pack()
    
    def create_drag_drop_section(self, parent):
        """Create modern drag and drop area"""
        # Card container
        card_frame = tk.Frame(parent, bg=self.colors['bg_secondary'], relief='solid', borderwidth=1)
        card_frame.pack(fill="x", pady=(0, 20), padx=10)
        
        # Section header
        header_frame = tk.Frame(card_frame, bg=self.colors['bg_secondary'])
        header_frame.pack(fill="x", padx=20, pady=(20, 10))
        
        title_label = tk.Label(
            header_frame,
            text="📁 Dataset Input",
            font=self.fonts['heading'],
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_primary']
        )
        title_label.pack(anchor="w")
        
        # Drag and drop area
        self.drop_frame = tk.Frame(
            card_frame,
            bg=self.colors['bg_tertiary'],
            relief='ridge',
            borderwidth=2,
            height=120
        )
        self.drop_frame.pack(fill="x", padx=20, pady=(0, 10))
        self.drop_frame.pack_propagate(False)
        
        # Drop area content
        drop_content = tk.Frame(self.drop_frame, bg=self.colors['bg_tertiary'])
        drop_content.place(relx=0.5, rely=0.5, anchor="center")
        
        self.drop_icon = tk.Label(
            drop_content,
            text="📂",
            font=('Segoe UI', 24),
            bg=self.colors['bg_tertiary'],
            fg=self.colors['text_muted']
        )
        self.drop_icon.pack()
        
        self.drop_text = tk.Label(
            drop_content,
            text="Drag & drop folder here or click to browse",
            font=self.fonts['body'],
            bg=self.colors['bg_tertiary'],
            fg=self.colors['text_muted']
        )
        self.drop_text.pack(pady=(5, 0))
        
        # Selected folder display
        self.folder_display = tk.Label(
            card_frame,
            textvariable=self.selected_folder,
            font=self.fonts['small'],
            bg=self.colors['bg_secondary'],
            fg=self.colors['accent'],
            wraplength=800,
            justify="left"
        )
        self.folder_display.pack(fill="x", padx=20, pady=(0, 20))
        
        # Bind click event to browse
        self.drop_frame.bind("<Button-1>", lambda e: self.browse_folder())
        for widget in [drop_content, self.drop_icon, self.drop_text]:
            widget.bind("<Button-1>", lambda e: self.browse_folder())
    
    def setup_drag_drop(self):
        """Setup drag and drop functionality (fallback to click if not available)"""
        try:
            # Try to import drag and drop functionality
            from tkinterdnd2 import DND_FILES, TkinterDnD
            
            # Convert root to support drag and drop
            self.root = TkinterDnD.Tk()
            self.root.title("Varroa Detector - AI-Powered Mite Analysis")
            self.root.geometry("1000x800")
            self.root.configure(bg=self.colors['bg_primary'])
            
            # Enable drag and drop on the drop frame
            self.drop_frame.drop_target_register(DND_FILES)
            self.drop_frame.dnd_bind('<<Drop>>', self.on_drop)
            
        except ImportError:
            # Fallback to click-only functionality
            print("Drag and drop not available, using click-to-browse only")
    
    def on_drop(self, event):
        """Handle drag and drop events"""
        files = event.data.split()
        if files:
            folder_path = files[0].strip('{}')
            if os.path.isdir(folder_path):
                self.selected_folder.set(folder_path)
                self.animate_drop_success()
            else:
                messagebox.showwarning("Invalid Drop", "Please drop a folder, not a file.")
    
    def animate_drop_success(self):
        """Animate successful drop"""
        original_bg = self.drop_frame.cget('bg')
        self.drop_frame.configure(bg=self.colors['success'])
        self.drop_text.configure(text="✅ Folder loaded successfully!", fg=self.colors['text_primary'])
        
        # Reset after animation
        self.root.after(1500, lambda: [
            self.drop_frame.configure(bg=original_bg),
            self.drop_text.configure(text="Drag & drop folder here or click to browse", 
                                   fg=self.colors['text_muted'])
        ])
    
    def create_configuration_section(self, parent):
        """Create modern configuration section"""
        card_frame = tk.Frame(parent, bg=self.colors['bg_secondary'], relief='solid', borderwidth=1)
        card_frame.pack(fill="x", pady=(0, 20), padx=10)
        
        # Header
        header_frame = tk.Frame(card_frame, bg=self.colors['bg_secondary'])
        header_frame.pack(fill="x", padx=20, pady=(20, 15))
        
        title_label = tk.Label(
            header_frame,
            text="⚙️ Analysis Configuration",
            font=self.fonts['heading'],
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_primary']
        )
        title_label.pack(anchor="w")
        
        # Subtitle for reanalysis mode
        subtitle_label = tk.Label(
            header_frame,
            text="🔄 Running in Reanalysis Mode",
            font=self.fonts['small'],
            bg=self.colors['bg_secondary'],
            fg=self.colors['accent']
        )
        subtitle_label.pack(anchor="w", pady=(5, 0))
        
        # Configuration grid
        config_frame = tk.Frame(card_frame, bg=self.colors['bg_secondary'])
        config_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        # Grid setup with modern entries
        configs = [
            ("Analysis Name:", self.analysis_name, "entry"),
            ("Plates per Recording:", self.plates_per_recording, "combo", ["1", "2"]),
            ("Time Between Recordings (min):", self.time_between_recordings, "entry")
        ]
        
        for i, config in enumerate(configs):
            label_text, variable, widget_type = config[:3]
            
            # Label
            label = tk.Label(
                config_frame,
                text=label_text,
                font=self.fonts['body'],
                bg=self.colors['bg_secondary'],
                fg=self.colors['text_secondary'],
                anchor="w"
            )
            label.grid(row=i, column=0, sticky="w", pady=8, padx=(0, 20))
            
            # Widget
            if widget_type == "entry":
                widget = tk.Entry(
                    config_frame,
                    textvariable=variable,
                    font=self.fonts['body'],
                    bg=self.colors['surface'],
                    fg=self.colors['text_primary'],
                    relief='solid',
                    borderwidth=1,
                    width=30,
                    insertbackground=self.colors['text_primary']
                )
                widget.grid(row=i, column=1, sticky="ew", pady=8, ipady=6)
            
            elif widget_type == "combo":
                values = config[3]
                widget = ttk.Combobox(
                    config_frame,
                    textvariable=variable,
                    values=values,
                    state="readonly",
                    width=28,
                    font=self.fonts['body']
                )
                widget.grid(row=i, column=1, sticky="ew", pady=8, ipady=6)
        
        # Configure grid weights
        config_frame.columnconfigure(1, weight=1)
    
    def create_progress_section(self, parent):
        """Create modern progress section"""
        card_frame = tk.Frame(parent, bg=self.colors['bg_secondary'], relief='solid', borderwidth=1)
        card_frame.pack(fill="x", pady=(0, 20), padx=10)
        
        # Header
        header_frame = tk.Frame(card_frame, bg=self.colors['bg_secondary'])
        header_frame.pack(fill="x", padx=20, pady=(20, 15))
        
        title_label = tk.Label(
            header_frame,
            text="📊 Analysis Progress",
            font=self.fonts['heading'],
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_primary']
        )
        title_label.pack(anchor="w")
        
        # Progress content
        progress_content = tk.Frame(card_frame, bg=self.colors['bg_secondary'])
        progress_content.pack(fill="x", padx=20, pady=(0, 20))
        
        # Status label
        self.progress_label = tk.Label(
            progress_content,
            text="Ready to start analysis",
            font=self.fonts['body'],
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_secondary']
        )
        self.progress_label.pack(pady=(0, 15))
        
        # Modern progress bar
        self.progress_bar = ttk.Progressbar(
            progress_content,
            mode='determinate',
            length=600,
            style='Modern.Horizontal.TProgressbar'
        )
        self.progress_bar.pack()
        
        # Percentage label
        self.progress_percent = tk.Label(
            progress_content,
            text="0%",
            font=self.fonts['small'],
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_muted']
        )
        self.progress_percent.pack(pady=(5, 0))
    
    def create_action_buttons_section(self, parent):
        """Create modern action buttons"""
        button_frame = tk.Frame(parent, bg=self.colors['bg_primary'])
        button_frame.pack(fill="x", pady=(0, 20), padx=10)
        
        # Start button
        self.start_button = tk.Button(
            button_frame,
            text="🚀 Start Analysis",
            font=self.fonts['subheading'],
            bg=self.colors['success'],
            fg='white',
            relief='flat',
            padx=40,
            pady=15,
            command=self.start_analysis,
            cursor='hand2'
        )
        self.start_button.pack(side="left", expand=True, fill="x", padx=(0, 10))
        
        # Stop button
        self.stop_button = tk.Button(
            button_frame,
            text="⏹️ Stop",
            font=self.fonts['subheading'],
            bg=self.colors['error'],
            fg='white',
            relief='flat',
            padx=40,
            pady=15,
            command=self.stop_analysis,
            state="disabled",
            cursor='hand2'
        )
        self.stop_button.pack(side="right", padx=(10, 0))
        
        # Button hover effects
        self.add_hover_effect(self.start_button, self.colors['success'], '#8cc85d')
        self.add_hover_effect(self.stop_button, self.colors['error'], '#e64553')
    
    def add_hover_effect(self, button, normal_color, hover_color):
        """Add hover effect to button"""
        def on_enter(e):
            if button['state'] != 'disabled':
                button.configure(bg=hover_color)
        
        def on_leave(e):
            if button['state'] != 'disabled':
                button.configure(bg=normal_color)
        
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)
    
    def create_results_section(self, parent):
        """Create modern results section"""
        card_frame = tk.Frame(parent, bg=self.colors['bg_secondary'], relief='solid', borderwidth=1)
        card_frame.pack(fill="x", pady=(0, 20), padx=10)
        
        # Header
        header_frame = tk.Frame(card_frame, bg=self.colors['bg_secondary'])
        header_frame.pack(fill="x", padx=20, pady=(20, 15))
        
        title_label = tk.Label(
            header_frame,
            text="📦 Results",
            font=self.fonts['heading'],
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_primary']
        )
        title_label.pack(anchor="w")
        
        # Results content
        results_content = tk.Frame(card_frame, bg=self.colors['bg_secondary'])
        results_content.pack(fill="x", padx=20, pady=(0, 20))
        
        # Results info
        self.results_info = tk.Label(
            results_content,
            text="No analysis completed yet",
            font=self.fonts['body'],
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_muted']
        )
        self.results_info.pack(pady=(0, 15))
        
        # Buttons frame
        buttons_frame = tk.Frame(results_content, bg=self.colors['bg_secondary'])
        buttons_frame.pack(fill="x")
        
        # Download ZIP button (centered)
        self.download_button = tk.Button(
            buttons_frame,
            text="📥 Download ZIP",
            font=self.fonts['body'],
            bg=self.colors['warning'],
            fg='white',
            relief='flat',
            padx=20,
            pady=10,
            command=self.download_results_zip,
            state="disabled",
            cursor='hand2'
        )
        self.download_button.pack(expand=True, fill="x")
        
        # Add hover effects
        self.add_hover_effect(self.download_button, self.colors['warning'], '#fab387')
    
    def browse_folder(self):
        """Open file dialog to select folder"""
        folder_path = filedialog.askdirectory(
            title="Select Dataset Folder",
            initialdir=os.getcwd()
        )
        
        if folder_path:
            self.selected_folder.set(folder_path)
            self.animate_drop_success()
    
    def validate_inputs(self):
        """Validate user inputs"""
        if not self.selected_folder.get():
            messagebox.showerror("Error", "Please select a dataset folder")
            return False
        
        if not os.path.exists(self.selected_folder.get()):
            messagebox.showerror("Error", "Selected dataset folder does not exist")
            return False
        
        name = self.analysis_name.get().strip()
        if not name:
            messagebox.showerror("Error", "Please enter an analysis name")
            return False
        
        # Validate numeric inputs
        try:
            time_between = float(self.time_between_recordings.get())
            if time_between < 0:
                messagebox.showerror("Error", "Time between recordings cannot be negative")
                return False
        except ValueError:
            messagebox.showerror("Error", "Time between recordings must be a valid number")
            return False
        
        return True
    
    def start_analysis(self):
        """Start the analysis process"""
        if not self.validate_inputs():
            return
        
        # Update UI state
        self.analysis_running = True
        self.start_button.configure(state="disabled", bg=self.colors['bg_tertiary'])
        self.stop_button.configure(state="normal", bg=self.colors['error'])
        self.progress_bar['value'] = 0
        self.progress_percent.configure(text="0%")
        self.progress_label.configure(text="Initializing analysis...", fg=self.colors['text_primary'])
        self.status_label.configure(text="● Running", fg=self.colors['warning'])
        
        # Get parameters
        folder_path = self.selected_folder.get()
        name = self.analysis_name.get().strip()
        num_per_plate = int(self.plates_per_recording.get())
        reanalyze = True  # Always run in reanalysis mode
        num_recordings = 2  # Default value for reanalysis
        time_between_rec = float(self.time_between_recordings.get())
        
        # Start analysis in separate thread
        analysis_thread = threading.Thread(
            target=self.run_analysis,
            args=(folder_path, name, num_per_plate, reanalyze, num_recordings, time_between_rec),
            daemon=True
        )
        analysis_thread.start()
    
    def run_analysis(self, folder_path, name, num_per_plate, reanalyze, num_recordings, time_between_rec):
        """Run the analysis in a separate thread"""
        try:
            # Update progress
            self.root.after(0, lambda: self.update_progress(10, "Loading AI detector..."))
            
            # Lazy import to avoid issues at startup
            try:
                from main import predict
            except ImportError as e:
                raise RuntimeError(f"Could not import analysis module: {e}")
            
            # Update progress
            self.root.after(0, lambda: self.update_progress(30, "Processing images with AI..."))
            
            # Run the actual prediction with all parameters
            predict(
                folder_path=folder_path,
                name=name,
                num_per_plate=num_per_plate,
                reanalyze=reanalyze,
                discobox_run=False,
                num_recordings=num_recordings,
                count=2,
                time_between_rec=time_between_rec
            )
            
            # Update progress
            self.root.after(0, lambda: self.update_progress(80, "Generating comprehensive reports..."))
            
            # Simulate final processing
            time.sleep(1)
            
            # Find results folder in default outputs location
            original_cwd = os.getcwd()
            results_folder = os.path.join(original_cwd, "outputs", "results")
            if os.path.exists(results_folder):
                self.results_path = results_folder
            else:
                outputs_dir = os.path.join(original_cwd, "outputs")
                if os.path.exists(outputs_dir):
                    reanalysis_dirs = [d for d in os.listdir(outputs_dir) if d.startswith("reanalysis")]
                    if reanalysis_dirs:
                        latest = max(reanalysis_dirs, key=lambda x: int(x.replace("reanalysis", "") or "0"))
                        self.results_path = os.path.join(outputs_dir, latest)
                    else:
                        self.results_path = outputs_dir
            
            # Update UI on completion
            self.root.after(0, self.analysis_completed)
            
        except Exception as e:
            error_msg = f"Analysis failed: {str(e)}"
            self.root.after(0, lambda: self.analysis_failed(error_msg))
    
    def update_progress(self, value, message):
        """Update progress bar and message"""
        self.progress_bar['value'] = value
        self.progress_percent.configure(text=f"{int(value)}%")
        self.progress_label.configure(text=message)
        self.root.update_idletasks()
    
    def analysis_completed(self):
        """Handle successful analysis completion"""
        self.analysis_running = False
        self.start_button.configure(state="normal", bg=self.colors['success'])
        self.stop_button.configure(state="disabled", bg=self.colors['bg_tertiary'])
        self.progress_bar['value'] = 100
        self.progress_percent.configure(text="100%")
        self.progress_label.configure(text="✅ Analysis completed successfully!", 
                                    fg=self.colors['success'])
        self.status_label.configure(text="● Complete", fg=self.colors['success'])
        
        # Update results section
        self.results_info.configure(
            text="🎉 Analysis completed! Results are ready for download.",
            fg=self.colors['success']
        )
        self.download_button.configure(state="normal", bg=self.colors['warning'])
        
        # Show completion message
        messagebox.showinfo(
            "Success",
            "🎉 Analysis completed successfully!\n\nYou can now download your results as a ZIP file."
        )
    
    def analysis_failed(self, error_msg):
        """Handle analysis failure"""
        self.analysis_running = False
        self.start_button.configure(state="normal", bg=self.colors['success'])
        self.stop_button.configure(state="disabled", bg=self.colors['bg_tertiary'])
        self.progress_bar['value'] = 0
        self.progress_percent.configure(text="0%")
        self.progress_label.configure(text="❌ Analysis failed", fg=self.colors['error'])
        self.status_label.configure(text="● Error", fg=self.colors['error'])
        
        # Show error message
        messagebox.showerror("Analysis Failed", f"❌ {error_msg}")
    
    def stop_analysis(self):
        """Stop the current analysis"""
        if self.analysis_running:
            self.analysis_running = False
            self.start_button.configure(state="normal", bg=self.colors['success'])
            self.stop_button.configure(state="disabled", bg=self.colors['bg_tertiary'])
            self.progress_bar['value'] = 0
            self.progress_percent.configure(text="0%")
            self.progress_label.configure(text="Analysis stopped", fg=self.colors['warning'])
            self.status_label.configure(text="● Stopped", fg=self.colors['warning'])
            messagebox.showinfo("Stopped", "Analysis has been stopped")
    
    def download_results_zip(self):
        """Create and download results as ZIP file, then clean up outputs folder"""
        if not self.results_path or not os.path.exists(self.results_path):
            messagebox.showwarning("No Results", "No results folder found to download")
            return
        
        try:
            # Ask user where to save the ZIP
            analysis_name = self.analysis_name.get().strip() or "analysis"
            default_filename = f"{analysis_name}.zip"
            
            zip_path = filedialog.asksaveasfilename(
                title="Save Results ZIP",
                defaultextension=".zip",
                filetypes=[("ZIP files", "*.zip"), ("All files", "*.*")],
                initialdir=os.path.expanduser("~/Downloads"),
                initialfile=default_filename
            )
            
            if not zip_path:
                return
            
            # Create progress dialog
            progress_window = tk.Toplevel(self.root)
            progress_window.title("Creating ZIP...")
            progress_window.geometry("400x120")
            progress_window.configure(bg=self.colors['bg_secondary'])
            progress_window.transient(self.root)
            progress_window.grab_set()
            
            # Center the progress window
            progress_window.update_idletasks()
            x = (progress_window.winfo_screenwidth() // 2) - 200
            y = (progress_window.winfo_screenheight() // 2) - 60
            progress_window.geometry(f"400x120+{x}+{y}")
            
            progress_label = tk.Label(
                progress_window,
                text="Creating ZIP file...",
                font=self.fonts['body'],
                bg=self.colors['bg_secondary'],
                fg=self.colors['text_primary']
            )
            progress_label.pack(pady=20)
            
            zip_progress = ttk.Progressbar(
                progress_window,
                mode='indeterminate',
                length=300,
                style='Modern.Horizontal.TProgressbar'
            )
            zip_progress.pack(pady=(0, 20))
            zip_progress.start()
            
            # Create ZIP in separate thread
            def create_zip():
                try:
                    # Determine the specific reanalysis folder to zip
                    outputs_dir = os.path.join(os.getcwd(), "outputs")
                    folder_to_zip = None
                    
                    if os.path.exists(outputs_dir):
                        # Find the latest reanalysis folder
                        reanalysis_dirs = [d for d in os.listdir(outputs_dir) if d.startswith("reanalysis")]
                        if reanalysis_dirs:
                            # Get the latest reanalysis folder
                            latest = max(reanalysis_dirs, key=lambda x: int(x.replace("reanalysis", "") or "0"))
                            folder_to_zip = os.path.join(outputs_dir, latest)
                        else:
                            # If no reanalysis folder, check if results folder exists
                            results_folder = os.path.join(outputs_dir, "results")
                            if os.path.exists(results_folder):
                                folder_to_zip = results_folder
                            else:
                                folder_to_zip = outputs_dir
                    
                    if not folder_to_zip or not os.path.exists(folder_to_zip):
                        raise Exception("No results folder found to zip")
                    
                    # Update progress text
                    self.root.after(0, lambda: progress_label.configure(text="Compressing files..."))
                    
                    # Create the ZIP file with only the contents of the reanalysis folder
                    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                        for root, dirs, files in os.walk(folder_to_zip):
                            for file in files:
                                file_path = os.path.join(root, file)
                                # Create archive path relative to the folder being zipped
                                # This puts files directly in the ZIP root, not in a subfolder
                                arc_path = os.path.relpath(file_path, folder_to_zip)
                                zipf.write(file_path, arc_path)
                    
                    # Update progress text
                    self.root.after(0, lambda: progress_label.configure(text="Cleaning up..."))
                    
                    # Remove only the specific reanalysis folder after successful ZIP creation
                    if os.path.exists(folder_to_zip):
                        shutil.rmtree(folder_to_zip)
                        # Reset results path since folder is gone
                        self.results_path = None
                    
                    # Get folder name for success message
                    folder_name = os.path.basename(folder_to_zip)
                    
                    # Close progress window and show success
                    self.root.after(0, lambda: [
                        progress_window.destroy(),
                        self.download_button.configure(state="disabled", bg=self.colors['bg_tertiary']),
                        self.results_info.configure(text="📁 Results have been downloaded and cleaned up", fg=self.colors['text_muted']),
                        messagebox.showinfo(
                            "ZIP Created",
                            f"✅ Results from '{folder_name}' successfully saved to:\n{zip_path}\n\nFile size: {self.get_file_size(zip_path)}\n\n🗑️ Analysis folder cleaned up."
                        )
                    ])
                    
                except Exception as e:
                    self.root.after(0, lambda: [
                        progress_window.destroy(),
                        messagebox.showerror("ZIP Error", f"Failed to create ZIP file:\n{e}")
                    ])
            
            # Start ZIP creation
            threading.Thread(target=create_zip, daemon=True).start()
            
        except Exception as e:
            messagebox.showerror("Download Error", f"Failed to download results:\n{e}")
    
    def get_file_size(self, file_path):
        """Get human readable file size"""
        size = os.path.getsize(file_path)
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024:
                return f"{size:.1f} {unit}"
            size /= 1024
        return f"{size:.1f} TB"
    
    def run(self):
        """Start the application"""
        self.root.mainloop()


def main():
    """Main entry point"""
    try:
        app = ModernVarroaDetectorApp()
        app.run()
    except Exception as e:
        print(f"Error starting application: {e}")
        messagebox.showerror("Startup Error", f"Failed to start application: {e}")


if __name__ == "__main__":
    main()
