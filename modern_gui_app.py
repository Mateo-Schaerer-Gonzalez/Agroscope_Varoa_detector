"""
Modern GUI Application for Varroa Detector with enhanced UI design
Features: Modern styling, drag-and-drop, ZIP downloads
"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk, font
import threading
import os
import sys
import subprocess
from pathlib import Path
import time
import zipfile
import shutil
from datetime import datetime
import tempfile
import cv2
import numpy as np
from PIL import Image, ImageTk, ImageDraw, ImageFont

class SplashScreen:
    def __init__(self, duration=3000):
        self.duration = duration
        self.splash = tk.Toplevel()
        self.splash.title("")
        self.splash.geometry("600x400")
        self.splash.configure(bg='#2d7d32')
        self.splash.overrideredirect(True)
        
        # Center splash screen
        self.center_splash()
        
        # Create splash content
        self.create_splash_content()
        
        # Auto close after duration
        self.splash.after(self.duration, self.close_splash)
        
        # Make sure splash is on top
        self.splash.lift()
        self.splash.focus_force()
        
    def center_splash(self):
        self.splash.update_idletasks()
        x = (self.splash.winfo_screenwidth() // 2) - 300
        y = (self.splash.winfo_screenheight() // 2) - 200
        self.splash.geometry(f"600x400+{x}+{y}")
        
    def create_splash_content(self):
        # Main container
        main_frame = tk.Frame(self.splash, bg='#2d7d32')
        main_frame.pack(expand=True, fill='both')
        
        # Title
        title_label = tk.Label(
            main_frame,
            text="🐝 Varroa Detector",
            font=('Segoe UI', 32, 'bold'),
            fg='#ffc107',
            bg='#2d7d32'
        )
        title_label.pack(pady=(60, 20))
        
        # Subtitle
        subtitle_label = tk.Label(
            main_frame,
            text="Advanced AI-Powered Mite Detection",
            font=('Segoe UI', 16),
            fg='white',
            bg='#2d7d32'
        )
        subtitle_label.pack(pady=(0, 40))
        
        # Bee emoji animation area
        self.bee_label = tk.Label(
            main_frame,
            text="🐝",
            font=('Segoe UI', 48),
            fg='#ffc107',
            bg='#2d7d32'
        )
        self.bee_label.pack(pady=20)
        
        # Loading text
        loading_label = tk.Label(
            main_frame,
            text="Loading...",
            font=('Segoe UI', 14),
            fg='white',
            bg='#2d7d32'
        )
        loading_label.pack(pady=(20, 0))
        
        # Progress bar
        progress_frame = tk.Frame(main_frame, bg='#2d7d32')
        progress_frame.pack(pady=20, padx=100, fill='x')
        
        self.progress_bar = tk.Canvas(
            progress_frame, 
            height=6, 
            bg='#1b5e20', 
            highlightthickness=0
        )
        self.progress_bar.pack(fill='x')
        
        # Start animations
        self.animate_progress()
        self.animate_bee()
        
    def animate_progress(self):
        # Animated progress bar
        def update_progress():
            for i in range(101):
                try:
                    if hasattr(self, 'progress_bar') and self.progress_bar.winfo_exists():
                        self.progress_bar.delete("all")
                        width = self.progress_bar.winfo_width()
                        progress_width = (width * i) / 100
                        self.progress_bar.create_rectangle(
                            0, 0, progress_width, 6,
                            fill='#ffc107', outline=''
                        )
                        self.splash.update()
                        time.sleep(0.02)
                    else:
                        break
                except (AttributeError, tk.TclError):
                    break
        
        # Run in thread to avoid blocking
        threading.Thread(target=update_progress, daemon=True).start()
        
    def animate_bee(self):
        # Simple bee animation
        bees = ["🐝", "🐛", "🐝", "🐛"]
        self.bee_index = 0
        
        def update_bee():
            try:
                if hasattr(self, 'bee_label') and self.bee_label.winfo_exists():
                    self.bee_label.configure(text=bees[self.bee_index])
                    self.bee_index = (self.bee_index + 1) % len(bees)
                    self.splash.after(500, update_bee)
            except (AttributeError, tk.TclError):
                pass
        
        update_bee()
        
    def close_splash(self):
        if hasattr(self, 'splash'):
            self.splash.destroy()


class ModernVarroaDetectorApp:
    def __init__(self):
        self.root = tk.Tk()
        
        # Hide main window initially
        self.root.withdraw()
        
        # Show splash screen
        self.splash = SplashScreen(duration=3000)
        
        # Initialize main window after splash
        self.root.after(3200, self.initialize_main_window)
        
    def initialize_main_window(self):
        """Initialize the main application window after splash screen"""
        self.root.title("🐝 Varroa Detector - AI-Powered Mite Analysis")
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
        self.temp_results_dir = None  # Store temp directory path
        self.current_image = None
        self.image_display_label = None
        
        # Track changes to plates_per_recording for zone overlay updates
        self.plates_per_recording.trace('w', self.on_zone_selection_change)
        
        # Create UI elements
        self.setup_ui()
        
        # Center the window
        self.center_window()
        
        # Show main window
        self.root.deiconify()
    
    def setup_modern_styles(self):
        """Configure modern light green visual styling"""
        # Modern light color scheme with green accents
        self.colors = {
            'bg_primary': '#ffffff',       # White background
            'bg_secondary': '#f8fdf8',     # Very light green tint
            'bg_tertiary': '#e8f5e8',      # Light green background
            'accent': '#2d7d32',           # Deep green accent
            'accent_hover': '#388e3c',     # Lighter green hover
            'success': '#4caf50',          # Success green
            'warning': '#ff9800',          # Orange
            'error': '#f44336',            # Red
            'text_primary': '#1b5e20',     # Dark green text
            'text_secondary': '#2e7d32',   # Medium green text
            'text_muted': '#6a7c59',       # Muted green text
            'surface': '#f1f8e9',          # Light green surface
            'gradient_start': '#66bb6a',   # Green gradient start
            'gradient_end': '#81c784',     # Green gradient end
            'bee_yellow': '#ffc107',       # Bee yellow accent
            'honeycomb': '#fff3c4'         # Honeycomb color
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
        
        # Configure modern button style with rounded appearance
        style.configure('Modern.TButton',
                       background=self.colors['accent'],
                       foreground='white',
                       borderwidth=0,
                       focuscolor='none',
                       relief='flat',
                       padding=(25, 15))
        
        style.map('Modern.TButton',
                 background=[('active', self.colors['accent_hover']),
                           ('pressed', self.colors['accent'])])
        
        # Configure modern frame style with softer appearance
        style.configure('Card.TFrame',
                       background=self.colors['bg_secondary'],
                       borderwidth=0,
                       relief='flat')
        
        # Configure modern progressbar with rounded look
        style.configure('Modern.Horizontal.TProgressbar',
                       background=self.colors['accent'],
                       troughcolor=self.colors['bg_tertiary'],
                       borderwidth=0,
                       lightcolor=self.colors['accent'],
                       darkcolor=self.colors['accent'],
                       relief='flat')
    
    def center_window(self):
        """Center the window on the screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def cleanup_previous_results(self):
        """Clean up any previous analysis results at startup when no files are in use"""
        try:
            outputs_dir = os.path.join(os.getcwd(), "outputs")
            if not os.path.exists(outputs_dir):
                return
            
            print("🧹 Cleaning up previous analysis results...")
            
            # More aggressive cleanup approach
            import subprocess
            import time
            
            # Remove all reanalysis directories
            for item in os.listdir(outputs_dir):
                if item.startswith("reanalysis"):
                    reanalysis_path = os.path.join(outputs_dir, item)
                    if os.path.isdir(reanalysis_path):
                        try:
                            # Try multiple approaches for stubborn folders
                            success = self.force_remove_directory(reanalysis_path)
                            if success:
                                print(f"✅ Removed: {item}")
                            else:
                                print(f"⚠️  Could not remove {item} - will try alternative approach")
                                # Alternative: try to remove individual files first
                                self.remove_files_recursively(reanalysis_path)
                        except Exception as e:
                            print(f"⚠️  Could not remove {item}: {e}")
            
            # Also clean up the results folder if it exists
            results_path = os.path.join(outputs_dir, "results")
            if os.path.exists(results_path):
                try:
                    success = self.force_remove_directory(results_path)
                    if success:
                        print("✅ Removed: results folder")
                    else:
                        print("⚠️  Could not remove results folder - trying alternative approach")
                        self.remove_files_recursively(results_path)
                except Exception as e:
                    print(f"⚠️  Could not remove results folder: {e}")
            
            print("🎉 Startup cleanup completed!")
            
        except Exception as e:
            print(f"⚠️  Error during startup cleanup: {e}")
    
    def force_remove_directory(self, directory_path):
        """Force remove a directory using multiple methods"""
        import time
        import subprocess
        
        # Method 1: Try normal removal first
        try:
            # Set all files as writable
            for root, dirs, files in os.walk(directory_path):
                for d in dirs:
                    try:
                        os.chmod(os.path.join(root, d), 0o777)
                    except:
                        pass
                for f in files:
                    try:
                        os.chmod(os.path.join(root, f), 0o777)
                    except:
                        pass
            
            shutil.rmtree(directory_path)
            return True
        except:
            pass
        
        # Method 2: Try Windows rmdir command
        try:
            subprocess.run(['rmdir', '/S', '/Q', directory_path], 
                          shell=True, check=False, 
                          capture_output=True, timeout=10)
            if not os.path.exists(directory_path):
                return True
        except:
            pass
        
        # Method 3: Try PowerShell Remove-Item
        try:
            cmd = f'Remove-Item -Path "{directory_path}" -Recurse -Force -ErrorAction SilentlyContinue'
            subprocess.run(['powershell', '-Command', cmd], 
                          check=False, capture_output=True, timeout=10)
            if not os.path.exists(directory_path):
                return True
        except:
            pass
        
        return False
    
    def remove_files_recursively(self, directory_path):
        """Try to remove individual files when directory removal fails"""
        try:
            for root, dirs, files in os.walk(directory_path, topdown=False):
                # Remove files first
                for file in files:
                    file_path = os.path.join(root, file)
                    try:
                        os.chmod(file_path, 0o777)
                        os.remove(file_path)
                    except:
                        try:
                            # Try force delete with Windows attrib command
                            subprocess.run(['attrib', '-R', '-S', '-H', file_path], 
                                         shell=True, capture_output=True, timeout=5)
                            os.remove(file_path)
                        except:
                            pass
                
                # Then try to remove directories
                for dir in dirs:
                    dir_path = os.path.join(root, dir)
                    try:
                        os.rmdir(dir_path)
                    except:
                        pass
            
            # Finally try to remove the root directory
            try:
                os.rmdir(directory_path)
            except:
                pass
                
        except Exception as e:
            print(f"Error in file removal: {e}")

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
        
        # Image preview section
        self.create_image_preview_section(scrollable_frame)
        
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
        title_frame = tk.Frame(parent, bg=self.colors['bg_primary'], height=140)
        title_frame.pack(fill="x", pady=(0, 30))
        title_frame.pack_propagate(False)
        
        # Main title with modern styling
        title_label = tk.Label(
            title_frame,
            text="🐝 Varroa Detector",
            font=self.fonts['title'],
            bg=self.colors['bg_primary'],
            fg=self.colors['gradient_end']
        )
        title_label.pack(pady=(15, 5))
        
        # Subtitle with better styling
        subtitle_label = tk.Label(
            title_frame,
            text="AI-powered analysis of bee mite images using advanced YOLO detection",
            font=self.fonts['body'],
            bg=self.colors['bg_primary'],
            fg=self.colors['text_secondary']
        )
        subtitle_label.pack(pady=(0, 8))
        
        # Status indicator
        self.status_label = tk.Label(
            title_frame,
            text="● Ready",
            font=self.fonts['small'],
            bg=self.colors['bg_primary'],
            fg=self.colors['success']
        )
        self.status_label.pack(pady=(0, 5))
    
    def create_drag_drop_section(self, parent):
        """Create modern drag and drop area"""
        # Card container with softer styling
        card_frame = tk.Frame(parent, bg=self.colors['bg_secondary'], relief='flat', borderwidth=0)
        card_frame.pack(fill="x", pady=(0, 25), padx=15)
        
        # Section header
        header_frame = tk.Frame(card_frame, bg=self.colors['bg_secondary'])
        header_frame.pack(fill="x", padx=20, pady=(20, 10))
        
        title_label = tk.Label(
            header_frame,
            text="� Dataset Input",
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
                self.load_and_display_first_image(folder_path)
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
    
    def on_zone_selection_change(self, *args):
        """Handle changes to zone selection - update image overlay"""
        if self.selected_folder.get():
            self.load_and_display_first_image(self.selected_folder.get())
    
    def load_and_display_first_image(self, folder_path):
        """Load and display the first image from the dataset with zone overlay"""
        try:
            # Find first image in dataset
            first_image_path = self.find_first_image(folder_path)
            if not first_image_path:
                self.update_image_display_error("No images found in dataset")
                return
            
            # Load image
            image = cv2.imread(first_image_path)
            if image is None:
                self.update_image_display_error("Could not load image")
                return
            
            # Convert to RGB
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            # Apply zone overlay
            image_with_zones = self.apply_zone_overlay(image_rgb)
            
            # Convert to PIL and display
            self.display_image(image_with_zones)
            
        except Exception as e:
            self.update_image_display_error(f"Error loading image: {str(e)}")
    
    def find_first_image(self, folder_path):
        """Find the first .bmp image in the dataset folder"""
        try:
            # Look for subfolders first
            subfolders = sorted([
                os.path.join(folder_path, d)
                for d in os.listdir(folder_path)
                if os.path.isdir(os.path.join(folder_path, d))
            ])
            
            search_paths = subfolders if subfolders else [folder_path]
            
            for search_path in search_paths:
                for root, dirs, files in os.walk(search_path):
                    bmp_files = sorted([f for f in files if f.lower().endswith('.bmp')])
                    if bmp_files:
                        return os.path.join(root, bmp_files[0])
            
            return None
            
        except Exception as e:
            print(f"Error finding first image: {e}")
            return None
    
    def apply_zone_overlay(self, image):
        """Apply zone bounding boxes overlay to the image"""
        try:
            num_zones = int(self.plates_per_recording.get())
            coordinates_file = f"Zoning/coordinates{num_zones}.txt"
            
            if not os.path.exists(coordinates_file):
                return image
            
            # Convert to PIL for drawing
            pil_image = Image.fromarray(image)
            draw = ImageDraw.Draw(pil_image)
            
            # Read zone coordinates
            with open(coordinates_file, 'r') as f:
                lines = f.readlines()
            
            # Define colors for different zone types
            colors = {
                0: (255, 100, 100, 128),  # Red with transparency for class 0
                1: (100, 255, 100, 128)   # Green with transparency for class 1
            }
            
            # Draw each zone
            for line in lines:
                parts = line.strip().split()
                if len(parts) >= 5:
                    class_id = int(parts[0])
                    x1, y1, x2, y2 = map(float, parts[1:5])
                    
                    # Convert coordinates to integers
                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                    
                    # Get color for this class
                    color = colors.get(class_id, (100, 100, 255, 128))
                    
                    # Draw rectangle outline
                    draw.rectangle([x1, y1, x2, y2], outline=color[:3], width=3)
                    
                    # Add zone label
                    zone_text = f"Zone {class_id}"
                    try:
                        # Try to use a font, fallback to default if not available
                        font = ImageFont.truetype("arial.ttf", 16)
                    except:
                        font = ImageFont.load_default()
                    
                    # Draw text background
                    text_bbox = draw.textbbox((x1, y1-25), zone_text, font=font)
                    draw.rectangle(text_bbox, fill=color[:3])
                    draw.text((x1, y1-25), zone_text, fill=(255, 255, 255), font=font)
            
            return np.array(pil_image)
            
        except Exception as e:
            print(f"Error applying zone overlay: {e}")
            return image
    
    def display_image(self, image_array):
        """Display the image in the GUI"""
        try:
            # Convert to PIL
            pil_image = Image.fromarray(image_array)
            
            # Calculate display size (maintain aspect ratio, max 600x400)
            max_width, max_height = 600, 400
            img_width, img_height = pil_image.size
            
            # Calculate scaling factor
            scale_w = max_width / img_width
            scale_h = max_height / img_height
            scale = min(scale_w, scale_h)
            
            # Resize image
            new_width = int(img_width * scale)
            new_height = int(img_height * scale)
            pil_image = pil_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # Convert to PhotoImage
            photo = ImageTk.PhotoImage(pil_image)
            
            # Update display
            self.image_display_label.configure(image=photo, text="")
            self.image_display_label.image = photo  # Keep a reference
            
        except Exception as e:
            self.update_image_display_error(f"Error displaying image: {str(e)}")
    
    def update_image_display_error(self, error_message):
        """Update image display with error message"""
        self.image_display_label.configure(
            image='',
            text=f"⚠️ {error_message}",
            font=self.fonts['body'],
            fg=self.colors['error']
        )
        self.image_display_label.image = None
    
    def create_configuration_section(self, parent):
        """Create modern configuration section"""
        card_frame = tk.Frame(parent, bg=self.colors['bg_secondary'], relief='flat', borderwidth=0)
        card_frame.pack(fill="x", pady=(0, 25), padx=15)
        
        # Header
        header_frame = tk.Frame(card_frame, bg=self.colors['bg_secondary'])
        header_frame.pack(fill="x", padx=20, pady=(20, 15))
        
        title_label = tk.Label(
            header_frame,
            text="🍯 Analysis Configuration",
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
                    relief='flat',
                    borderwidth=0,
                    width=30,
                    insertbackground=self.colors['text_primary']
                )
                widget.grid(row=i, column=1, sticky="ew", pady=10, padx=(15, 0), ipady=10)
            
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
    
    def create_image_preview_section(self, parent):
        """Create image preview section with zone overlay"""
        card_frame = tk.Frame(parent, bg=self.colors['bg_secondary'], relief='flat', borderwidth=0)
        card_frame.pack(fill="x", pady=(0, 25), padx=15)
        
        # Header
        header_frame = tk.Frame(card_frame, bg=self.colors['bg_secondary'])
        header_frame.pack(fill="x", padx=20, pady=(20, 10))
        
        title_label = tk.Label(
            header_frame,
            text="🖼️ Image Preview with Zone Overlay",
            font=self.fonts['heading'],
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_primary']
        )
        title_label.pack(anchor="w")
        
        subtitle_label = tk.Label(
            header_frame,
            text="Preview of the first image with zone boundaries",
            font=self.fonts['small'],
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_secondary']
        )
        subtitle_label.pack(anchor="w", pady=(5, 0))
        
        # Image display frame
        image_frame = tk.Frame(card_frame, bg=self.colors['bg_secondary'])
        image_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Create a scrollable canvas for the image
        canvas_frame = tk.Frame(image_frame, bg=self.colors['surface'], relief='flat', bd=1)
        canvas_frame.pack(fill="both", expand=True, pady=10)
        
        # Image display label
        self.image_display_label = tk.Label(
            canvas_frame,
            text="📂 Select a dataset folder to see the first image with zone overlay",
            font=self.fonts['body'],
            bg=self.colors['surface'],
            fg=self.colors['text_muted'],
            wraplength=600,
            justify='center'
        )
        self.image_display_label.pack(expand=True, pady=50)
    
    def create_progress_section(self, parent):
        """Create modern progress section"""
        card_frame = tk.Frame(parent, bg=self.colors['bg_secondary'], relief='flat', borderwidth=0)
        card_frame.pack(fill="x", pady=(0, 25), padx=15)
        
        # Header
        header_frame = tk.Frame(card_frame, bg=self.colors['bg_secondary'])
        header_frame.pack(fill="x", padx=20, pady=(20, 15))
        
        title_label = tk.Label(
            header_frame,
            text="� Analysis Progress",
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
        button_frame.pack(fill="x", pady=(10, 30), padx=20)
        
        # Start button with more rounded appearance
        self.start_button = tk.Button(
            button_frame,
            text="🚀 Start Analysis",
            font=self.fonts['subheading'],
            bg=self.colors['success'],
            fg='white',
            relief='flat',
            padx=45,
            pady=18,
            command=self.start_analysis,
            cursor='hand2',
            bd=0
        )
        self.start_button.pack(side="left", expand=True, fill="x", padx=(0, 15))
        
        # Stop button with softer styling
        self.stop_button = tk.Button(
            button_frame,
            text="⏹️ Stop",
            font=self.fonts['subheading'],
            bg=self.colors['error'],
            fg='white',
            relief='flat',
            padx=45,
            pady=18,
            command=self.stop_analysis,
            state="disabled",
            cursor='hand2',
            bd=0
        )
        self.stop_button.pack(side="right", padx=(15, 0))
        
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
        card_frame = tk.Frame(parent, bg=self.colors['bg_secondary'], relief='flat', borderwidth=0)
        card_frame.pack(fill="x", pady=(0, 25), padx=15)
        
        # Header
        header_frame = tk.Frame(card_frame, bg=self.colors['bg_secondary'])
        header_frame.pack(fill="x", padx=20, pady=(20, 15))
        
        title_label = tk.Label(
            header_frame,
            text="🍯 Results & Download",
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
            text="� Download Results",
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
            self.load_and_display_first_image(folder_path)
    
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
            self.root.after(0, lambda: self.update_progress(10, "Setting up analysis environment..."))
            
            # Create temporary directory for this analysis
            self.temp_results_dir = tempfile.mkdtemp(prefix="varroa_analysis_", suffix=f"_{name}")
            print(f"📁 Created temporary analysis directory: {self.temp_results_dir}")
            
            # Update progress
            self.root.after(0, lambda: self.update_progress(20, "Loading AI detector..."))
            
            # Lazy import to avoid issues at startup
            try:
                from main import predict
            except ImportError as e:
                raise RuntimeError(f"Could not import analysis module: {e}")
            
            # Update progress
            self.root.after(0, lambda: self.update_progress(40, "Processing images with AI..."))
            
            # Run the actual prediction with temporary output folder
            predict(
                folder_path=folder_path,
                name=name,
                num_per_plate=num_per_plate,
                reanalyze=reanalyze,
                discobox_run=False,
                num_recordings=num_recordings,
                count=2,
                time_between_rec=time_between_rec,
                output_folder=self.temp_results_dir  # Use temp directory
            )
            
            # Update progress
            self.root.after(0, lambda: self.update_progress(80, "Generating comprehensive reports..."))
            
            # Simulate final processing
            time.sleep(1)
            
            # Set results path to the temporary directory
            self.results_path = self.temp_results_dir
            print(f"✅ Analysis completed in: {self.temp_results_dir}")
            
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
        """Create and download results as ZIP file, then clean up temporary folder"""
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
                    # Determine the results folder to zip (use temp directory)
                    folder_to_zip = self.results_path
                    
                    if not folder_to_zip or not os.path.exists(folder_to_zip):
                        raise Exception("No results folder found to zip")
                    
                    # Update progress text
                    self.root.after(0, lambda: progress_label.configure(text="Compressing files..."))
                    
                    # Create the ZIP file with the contents of the temporary results folder
                    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                        for root, dirs, files in os.walk(folder_to_zip):
                            for file in files:
                                file_path = os.path.join(root, file)
                                # Create archive path relative to the folder being zipped
                                # This puts files directly in the ZIP root, not in a subfolder
                                arc_path = os.path.relpath(file_path, folder_to_zip)
                                zipf.write(file_path, arc_path)
                    
                    # Update progress text
                    self.root.after(0, lambda: progress_label.configure(text="Cleaning up temporary files..."))
                    
                    # Clean up the temporary directory
                    if self.temp_results_dir and os.path.exists(self.temp_results_dir):
                        try:
                            shutil.rmtree(self.temp_results_dir)
                            print(f"✅ Cleaned up temporary directory: {self.temp_results_dir}")
                            self.temp_results_dir = None
                            self.results_path = None
                        except Exception as cleanup_error:
                            print(f"⚠️  Warning: Could not clean up temp directory: {cleanup_error}")
                            # Don't fail the whole operation for cleanup issues
                    
                    # Get folder name for success message
                    folder_name = "analysis_results"
                    
                    # Close progress window and show success
                    self.root.after(0, lambda: [
                        progress_window.destroy(),
                        self.download_button.configure(state="disabled", bg=self.colors['bg_tertiary']),
                        self.results_info.configure(text="📁 Results downloaded and temporary files cleaned up", fg=self.colors['text_muted']),
                        messagebox.showinfo(
                            "ZIP Created Successfully",
                            f"✅ Analysis results have been saved to:\n{zip_path}\n\nFile size: {self.get_file_size(zip_path)}\n\n� Analysis folders will be cleaned up on next app startup."
                        )
                    ])
                    
                except Exception as e:
                    error_msg = str(e)
                    self.root.after(0, lambda: [
                        progress_window.destroy(),
                        messagebox.showerror("ZIP Error", f"Failed to create ZIP file:\n{error_msg}")
                    ])
            
            # Start ZIP creation
            threading.Thread(target=create_zip, daemon=True).start()
            
        except Exception as e:
            messagebox.showerror("Download Error", f"Failed to download results:\n{e}")
    
    def safe_remove_folder(self, folder_path):
        """Safely remove a folder with retry logic for Windows permission issues"""
        import time
        max_retries = 5
        delay = 1  # seconds
        
        for attempt in range(max_retries):
            try:
                if os.path.exists(folder_path):
                    # First try to make all files writable
                    for root, dirs, files in os.walk(folder_path):
                        for file in files:
                            file_path = os.path.join(root, file)
                            try:
                                os.chmod(file_path, 0o777)
                            except:
                                pass  # Ignore chmod errors
                    
                    # Try to remove the folder
                    shutil.rmtree(folder_path)
                    print(f"Successfully removed folder: {folder_path}")
                    return
                    
            except PermissionError as e:
                print(f"Attempt {attempt + 1}: Permission error removing {folder_path}: {e}")
                if attempt < max_retries - 1:
                    time.sleep(delay)
                    delay *= 2  # Exponential backoff
                else:
                    print(f"Failed to remove folder after {max_retries} attempts. Manual cleanup may be required.")
                    # Don't raise the exception - just log it and continue
                    
            except Exception as e:
                print(f"Unexpected error removing folder {folder_path}: {e}")
                break

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
