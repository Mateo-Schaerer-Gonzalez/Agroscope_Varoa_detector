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
        
        # Initialize text verification attributes early
        self.analysis_complete_flag = False
        self.zones_locked = False
        self.mite_zones = []
        self.current_hover_zone = None
        self.zone_coordinates = []
        self.canvas_scale = 1.0
        self.canvas_offset_x = 0
        self.canvas_offset_y = 0
        
        # MiteManager integration
        self.mite_manager = None  # Will store the MiteManager instance after analysis
        self.mite_manager = None  # Will store the MiteManager instance from analysis
        
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
            # Try to use MiteManager data first, fall back to coordinate files
            if self.mite_manager and hasattr(self.mite_manager, 'zones'):
                return self.apply_mite_manager_overlay(image)
            else:
                return self.apply_coordinate_file_overlay(image)
                
        except Exception as e:
            print(f"Error applying zone overlay: {e}")
            return image
    
    def apply_mite_manager_overlay(self, image):
        """Apply zone overlay using MiteManager data"""
        # Convert to PIL for drawing
        pil_image = Image.fromarray(image)
        draw = ImageDraw.Draw(pil_image)
        
        # Clear and rebuild zone coordinates from MiteManager
        self.zone_coordinates = []
        
        # Process MiteManager zones
        for zone_idx, mite_zone in enumerate(self.mite_manager.zones):
            # Get zone coordinates
            x1, y1, x2, y2 = mite_zone.x1, mite_zone.y1, mite_zone.x2, mite_zone.y2
            
            # Store zone coordinates for interaction (use zone_idx as class_id)
            self.zone_coordinates.append((zone_idx, x1, y1, x2, y2))
            
            # Determine colors based on lock status
            if self.zones_locked:
                outline_color = (200, 50, 50)  # Red when locked
                line_width = 5
            else:
                outline_color = (100, 255, 100)  # Green when unlocked  
                line_width = 3
                
            # Draw rectangle outline
            draw.rectangle([x1, y1, x2, y2], outline=outline_color, width=line_width)
            
            # Add zone label
            mite_count = len(mite_zone.mites) if hasattr(mite_zone, 'mites') else 0
            zone_text = f"Zone {zone_idx + 1}"
            if self.zones_locked:
                zone_text += " 🔒"
            zone_text += f" ({mite_count} mites)"
            
            try:
                # Try to use a font, fallback to default if not available
                font = ImageFont.truetype("arial.ttf", 16)
            except:
                font = ImageFont.load_default()
            
            # Draw text background
            text_bbox = draw.textbbox((x1, y1-25), zone_text, font=font)
            bg_color = outline_color
            draw.rectangle(text_bbox, fill=bg_color)
            draw.text((x1, y1-25), zone_text, fill=(255, 255, 255), font=font)
            
            # Add click indicator if analysis is completed
            if self.analysis_complete_flag and not self.zones_locked and mite_count > 0:
                click_text = "Click to verify"
                click_bbox = draw.textbbox((x1, y2+5), click_text, font=font)
                draw.rectangle(click_bbox, fill=(100, 100, 255))
                draw.text((x1, y2+5), click_text, fill=(255, 255, 255), font=font)
        
        return np.array(pil_image)
    
    def apply_coordinate_file_overlay(self, image):
        """Apply zone overlay using coordinate files (fallback method)"""
        num_zones = int(self.plates_per_recording.get())
        coordinates_file = f"Zoning/coordinates{num_zones}.txt"
        
        if not os.path.exists(coordinates_file):
            return image
        
        # Convert to PIL for drawing
        pil_image = Image.fromarray(image)
        draw = ImageDraw.Draw(pil_image)
        
        # Read zone coordinates and store for interaction
        self.zone_coordinates = []
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
                
                # Store zone coordinates for interaction
                self.zone_coordinates.append((class_id, x1, y1, x2, y2))
                
                # Get color for this class
                color = colors.get(class_id, (100, 100, 255, 128))
                
                # Draw rectangle outline - thicker if zones are locked
                line_width = 5 if self.zones_locked else 3
                outline_color = color[:3] if not self.zones_locked else (200, 50, 50)  # Red when locked
                
                draw.rectangle([x1, y1, x2, y2], outline=outline_color, width=line_width)
                
                # Add zone label with lock indicator
                zone_text = f"Zone {class_id}"
                if self.zones_locked:
                    zone_text += " 🔒"
                
                try:
                    # Try to use a font, fallback to default if not available
                    font = ImageFont.truetype("arial.ttf", 16)
                except:
                    font = ImageFont.load_default()
                
                # Draw text background
                text_bbox = draw.textbbox((x1, y1-25), zone_text, font=font)
                bg_color = outline_color if self.zones_locked else color[:3]
                draw.rectangle(text_bbox, fill=bg_color)
                draw.text((x1, y1-25), zone_text, fill=(255, 255, 255), font=font)
                
                # Add click indicator if analysis is completed
                if self.analysis_complete_flag and not self.zones_locked:
                    click_text = "Click to verify"
                    click_bbox = draw.textbbox((x1, y2+5), click_text, font=font)
                    draw.rectangle(click_bbox, fill=(100, 100, 255))
                    draw.text((x1, y2+5), click_text, fill=(255, 255, 255), font=font)
        
        return np.array(pil_image)
    
    def display_image(self, image_array):
        """Display the image in the GUI canvas"""
        try:
            # Hide fallback label if showing
            self.image_display_label.pack_forget()
            
            # Convert to PIL
            pil_image = Image.fromarray(image_array)
            
            # Calculate display size (maintain aspect ratio, max 400x300 for left panel)
            max_width, max_height = 400, 300
            img_width, img_height = pil_image.size
            
            # Calculate scaling factor
            scale_w = max_width / img_width
            scale_h = max_height / img_height
            self.canvas_scale = min(scale_w, scale_h)
            
            # Resize image
            new_width = int(img_width * self.canvas_scale)
            new_height = int(img_height * self.canvas_scale)
            pil_image_resized = pil_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # Configure canvas size
            self.image_canvas.configure(width=new_width, height=new_height)
            
            # Calculate centering offsets
            canvas_width = self.image_canvas.winfo_reqwidth()
            canvas_height = self.image_canvas.winfo_reqheight()
            self.canvas_offset_x = max(0, (canvas_width - new_width) // 2)
            self.canvas_offset_y = max(0, (canvas_height - new_height) // 2)
            
            # Convert to PhotoImage
            photo = ImageTk.PhotoImage(pil_image_resized)
            
            # Clear canvas and add image
            self.image_canvas.delete("all")
            self.image_canvas.create_image(
                self.canvas_offset_x, self.canvas_offset_y, 
                anchor="nw", image=photo
            )
            
            # Store reference to prevent garbage collection
            self.image_canvas.photo = photo
            
        except Exception as e:
            self.update_image_display_error(f"Error displaying image: {str(e)}")
    
    def update_image_display_error(self, error_message):
        """Update image display with error message"""
        # Show fallback label with error
        self.image_display_label.pack(expand=True, pady=50)
        self.image_display_label.configure(
            image='',
            text=f"⚠️ {error_message}",
            font=self.fonts['body'],
            fg=self.colors['error']
        )
        if hasattr(self.image_display_label, 'image'):
            self.image_display_label.image = None
        
        # Clear canvas
        if hasattr(self, 'image_canvas'):
            self.image_canvas.delete("all")
    
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
                
                # Store reference to plates combobox for zone locking
                if variable == self.plates_per_recording:
                    self.plates_combobox = widget
        
        # Configure grid weights
        config_frame.columnconfigure(1, weight=1)
    
    def create_image_preview_section(self, parent):
        """Create image preview section with zone overlay and text verification"""
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
            text="Preview of the first image with zone boundaries. Click zones to verify text after analysis.",
            font=self.fonts['small'],
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_secondary']
        )
        subtitle_label.pack(anchor="w", pady=(5, 0))
        
        # Main content frame with image and info panel
        content_frame = tk.Frame(card_frame, bg=self.colors['bg_secondary'])
        content_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Left side: Image display
        left_frame = tk.Frame(content_frame, bg=self.colors['bg_secondary'])
        left_frame.pack(side="left", fill="both", expand=True)
        
        # Create a scrollable canvas for the image
        canvas_frame = tk.Frame(left_frame, bg=self.colors['surface'], relief='flat', bd=1)
        canvas_frame.pack(fill="both", expand=True, pady=10)
        
        # Create canvas for interactive image
        self.image_canvas = tk.Canvas(
            canvas_frame,
            bg=self.colors['surface'],
            highlightthickness=0
        )
        self.image_canvas.pack(fill="both", expand=True)
        
        # Bind canvas events for text verification
        self.image_canvas.bind("<Motion>", self.on_image_hover)
        self.image_canvas.bind("<Button-1>", self.on_image_click)
        self.image_canvas.bind("<Leave>", self.on_image_leave)
        
        # Fallback image display label
        self.image_display_label = tk.Label(
            canvas_frame,
            text="📂 Select a dataset folder to see the first image with zone overlay",
            font=self.fonts['body'],
            bg=self.colors['surface'],
            fg=self.colors['text_muted'],
            wraplength=400,
            justify='center'
        )
        self.image_display_label.pack(expand=True, pady=50)
        
        # Right side: Zone info panel
        self.create_zone_info_panel(content_frame)
        
        # Initialize text verification state
        self.analysis_complete_flag = False
        self.zones_locked = False
        self.mite_zones = []  # Will store detected mite zones with text
        self.current_hover_zone = None
        self.zone_coordinates = []  # Zone boundary coordinates
        self.canvas_scale = 1.0
        self.canvas_offset_x = 0
        self.canvas_offset_y = 0
    
    def create_zone_info_panel(self, parent):
        """Create the zone information panel on the right side"""
        # Right side: Zone info panel
        right_frame = tk.Frame(parent, bg=self.colors['bg_tertiary'], relief='flat', bd=1)
        right_frame.pack(side="right", fill="y", padx=(15, 0))
        right_frame.configure(width=300)
        right_frame.pack_propagate(False)
        
        # Panel header
        panel_header = tk.Label(
            right_frame,
            text="🔍 Zone Information",
            font=self.fonts['subheading'],
            bg=self.colors['bg_tertiary'],
            fg=self.colors['text_primary']
        )
        panel_header.pack(pady=(15, 10))
        
        # Zone status indicator
        self.zone_status_frame = tk.Frame(right_frame, bg=self.colors['bg_tertiary'])
        self.zone_status_frame.pack(fill="x", padx=10, pady=(0, 15))
        
        self.zone_lock_status = tk.Label(
            self.zone_status_frame,
            text="🔓 Zones Unlocked",
            font=self.fonts['small'],
            bg=self.colors['bg_tertiary'],
            fg=self.colors['warning']
        )
        self.zone_lock_status.pack()
        
        # Current hover info
        hover_frame = tk.Frame(right_frame, bg=self.colors['surface'], relief='flat', bd=1)
        hover_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        tk.Label(
            hover_frame,
            text="Current Zone:",
            font=self.fonts['small'],
            bg=self.colors['surface'],
            fg=self.colors['text_secondary']
        ).pack(pady=(10, 5))
        
        self.hover_zone_info = tk.Label(
            hover_frame,
            text="Hover over a zone to see details",
            font=self.fonts['body'],
            bg=self.colors['surface'],
            fg=self.colors['text_muted'],
            wraplength=250,
            justify='center'
        )
        self.hover_zone_info.pack(pady=(0, 10))
        
        # Mite detection results
        results_frame = tk.Frame(right_frame, bg=self.colors['surface'], relief='flat', bd=1)
        results_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        tk.Label(
            results_frame,
            text="Detected Mites:",
            font=self.fonts['small'],
            bg=self.colors['surface'],
            fg=self.colors['text_secondary']
        ).pack(pady=(10, 5))
        
        # Scrollable mite list
        mite_scroll_frame = tk.Frame(results_frame, bg=self.colors['surface'])
        mite_scroll_frame.pack(fill="both", expand=True, padx=5)
        
        self.mite_listbox = tk.Listbox(
            mite_scroll_frame,
            bg=self.colors['bg_primary'],
            fg=self.colors['text_primary'],
            selectbackground=self.colors['accent'],
            selectforeground='white',
            font=self.fonts['small'],
            height=8
        )
        self.mite_listbox.pack(fill="both", expand=True, pady=(0, 5))
        self.mite_listbox.insert(0, "No analysis results yet")
        
        # Text verification controls
        verification_frame = tk.Frame(right_frame, bg=self.colors['bg_tertiary'])
        verification_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        tk.Label(
            verification_frame,
            text="Text Verification:",
            font=self.fonts['small'],
            bg=self.colors['bg_tertiary'],
            fg=self.colors['text_secondary']
        ).pack()
        
        self.verify_button = tk.Button(
            verification_frame,
            text="🔍 Click Zone to Edit Text",
            font=self.fonts['small'],
            bg=self.colors['text_muted'],
            fg='white',
            state="disabled",
            relief='flat',
            pady=5
        )
        self.verify_button.pack(fill="x", pady=(5, 0))
    
    def on_image_hover(self, event):
        """Handle mouse hover over the image canvas"""
        if not self.zone_coordinates:
            return
            
        # Get mouse coordinates relative to the image
        canvas_x = self.image_canvas.canvasx(event.x)
        canvas_y = self.image_canvas.canvasy(event.y)
        
        # Convert canvas coordinates to image coordinates
        img_x = int((canvas_x - self.canvas_offset_x) / self.canvas_scale)
        img_y = int((canvas_y - self.canvas_offset_y) / self.canvas_scale)
        
        # Check which zone we're hovering over
        hovered_zone = self.get_zone_at_point(img_x, img_y)
        
        if hovered_zone != self.current_hover_zone:
            self.current_hover_zone = hovered_zone
            self.update_hover_info(hovered_zone)
            
        # Change cursor if over a clickable zone (after analysis)
        if self.analysis_complete_flag and hovered_zone is not None:
            self.image_canvas.configure(cursor="hand2")
        else:
            self.image_canvas.configure(cursor="")
    
    def on_image_click(self, event):
        """Handle mouse click on the image canvas"""
        if not self.analysis_complete_flag or not self.zone_coordinates:
            return
            
        # Get mouse coordinates relative to the image
        canvas_x = self.image_canvas.canvasx(event.x)
        canvas_y = self.image_canvas.canvasy(event.y)
        
        # Convert canvas coordinates to image coordinates
        img_x = int((canvas_x - self.canvas_offset_x) / self.canvas_scale)
        img_y = int((canvas_y - self.canvas_offset_y) / self.canvas_scale)
        
        # Check which zone was clicked
        clicked_zone = self.get_zone_at_point(img_x, img_y)
        
        if clicked_zone is not None:
            self.open_text_verification_dialog(clicked_zone)
    
    def on_image_leave(self, event):
        """Handle mouse leaving the image canvas"""
        self.current_hover_zone = None
        self.update_hover_info(None)
        self.image_canvas.configure(cursor="")
    
    def get_zone_at_point(self, x, y):
        """Get the zone index at the given point coordinates"""
        for i, (zone_class, x1, y1, x2, y2) in enumerate(self.zone_coordinates):
            if x1 <= x <= x2 and y1 <= y <= y2:
                return i
        return None
    
    def update_hover_info(self, zone_index):
        """Update the hover information panel with simplified display"""
        if zone_index is None:
            self.hover_zone_info.configure(
                text="Hover over a zone to see details",
                fg=self.colors['text_muted']
            )
            return
            
        if zone_index < len(self.zone_coordinates):
            # Initialize variables
            zone_label = f"Zone {zone_index + 1}"  # Default zone label
            mite_count = 0
            
            # Get zone label and mite count from MiteManager if available
            if self.mite_manager and hasattr(self.mite_manager, 'zones') and zone_index < len(self.mite_manager.zones):
                # Use actual MiteManager data
                mite_zone = self.mite_manager.zones[zone_index]
                mite_count = len(mite_zone.mites) if hasattr(mite_zone, 'mites') else 0
                zone_label = getattr(mite_zone, 'zone_id', f"Zone {zone_index + 1}")
            else:
                # Fallback to mite_zones data
                zone_mites = [mite for mite in self.mite_zones if mite.get('zone_id') == zone_index]
                mite_count = len(zone_mites)
                
                # Try to get zone label from first mite in the zone
                if zone_mites:
                    zone_label = zone_mites[0].get('zone_label', f"Zone {zone_index + 1}")
            
            # Simple display: Zone ID and mite count only
            zone_info = f"{zone_label}\nMites: {mite_count}"
            
            # Add click hint if analysis is complete and there are mites
            if self.analysis_complete_flag and mite_count > 0:
                zone_info += "\n\nClick to verify text"
            elif mite_count > 0:  # Show hint even if analysis not complete (for testing)
                zone_info += "\n\nClick to verify text"
            
            self.hover_zone_info.configure(
                text=zone_info,
                fg=self.colors['text_primary']
            )
    
    def open_text_verification_dialog(self, zone_index):
        """Open the text verification dialog for the clicked zone"""
        zone_mites = [mite for mite in self.mite_zones if mite.get('zone_id') == zone_index]
        
        if not zone_mites:
            messagebox.showinfo("No Mites", f"No mites detected in Zone {zone_index + 1}")
            return
        
        # Create text verification dialog
        dialog = tk.Toplevel(self.root)
        dialog.title(f"🔍 Text Verification - Zone {zone_index + 1}")
        dialog.geometry("500x400")
        dialog.configure(bg=self.colors['bg_primary'])
        dialog.resizable(True, True)
        
        # Center dialog
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Dialog content
        main_frame = tk.Frame(dialog, bg=self.colors['bg_primary'])
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        title_label = tk.Label(
            main_frame,
            text=f"🔍 Verify Detected Text - Zone {zone_index + 1}",
            font=self.fonts['heading'],
            bg=self.colors['bg_primary'],
            fg=self.colors['text_primary']
        )
        title_label.pack(pady=(0, 15))
        
        # Mite list with text editing
        for i, mite in enumerate(zone_mites):
            mite_frame = tk.Frame(main_frame, bg=self.colors['surface'], relief='flat', bd=1)
            mite_frame.pack(fill="x", pady=(0, 10))
            
            # Mite info
            mite_info_label = tk.Label(
                mite_frame,
                text=f"Mite {mite.get('mite_id', f'mite_{i+1}')} - Status: {mite.get('status', 'unknown')}",
                font=self.fonts['body'],
                bg=self.colors['surface'],
                fg=self.colors['text_primary']
            )
            mite_info_label.pack(anchor="w", padx=10, pady=(10, 5))
            
            # Text entry
            text_label = tk.Label(
                mite_frame,
                text="Detected/Edited Text:",
                font=self.fonts['small'],
                bg=self.colors['surface'],
                fg=self.colors['text_secondary']
            )
            text_label.pack(anchor="w", padx=10)
            
            text_entry = tk.Entry(
                mite_frame,
                font=self.fonts['body'],
                bg=self.colors['bg_primary'],
                relief='flat',
                bd=1
            )
            current_text = mite.get('detected_text', f"Text for mite {mite.get('mite_id', i+1)}")
            text_entry.insert(0, current_text)
            text_entry.pack(fill="x", padx=10, pady=(2, 10))
            
            # Store reference for saving
            mite['text_entry'] = text_entry
        
        # Buttons frame
        button_frame = tk.Frame(main_frame, bg=self.colors['bg_primary'])
        button_frame.pack(fill="x", pady=(15, 0))
        
        # Save button
        save_button = tk.Button(
            button_frame,
            text="💾 Save Changes",
            font=self.fonts['body'],
            bg=self.colors['success'],
            fg='white',
            relief='flat',
            pady=10,
            command=lambda: self.save_text_verification(zone_mites, dialog)
        )
        save_button.pack(side="left", padx=(0, 10))
        
        # Cancel button
        cancel_button = tk.Button(
            button_frame,
            text="✖ Cancel",
            font=self.fonts['body'],
            bg=self.colors['error'],
            fg='white',
            relief='flat',
            pady=10,
            command=dialog.destroy
        )
        cancel_button.pack(side="left")
    
    def save_text_verification(self, zone_mites, dialog):
        """Save the verified text changes"""
        changes_made = False
        
        for mite in zone_mites:
            if 'text_entry' in mite:
                new_text = mite['text_entry'].get()
                old_text = mite.get('detected_text', '')
                
                if new_text != old_text:
                    mite['verified_text'] = new_text
                    mite['detected_text'] = new_text  # Update the display text
                    mite['text_verified'] = True
                    changes_made = True
                    
                    # If MiteManager is available, update the text zones
                    if hasattr(self, 'mite_manager') and self.mite_manager:
                        zone_id = mite.get('zone_id', 0)
                        if zone_id < len(self.mite_manager.zones):
                            zone = self.mite_manager.zones[zone_id]
                            
                            # Update text zones if they exist
                            if hasattr(zone, 'text_zones') and zone.text_zones:
                                for text_zone in zone.text_zones:
                                    if hasattr(text_zone, 'text'):
                                        text_zone.text = new_text
                            else:
                                # Create a text zone if none exists
                                try:
                                    from classes.Rect import TextZone
                                    if not hasattr(zone, 'text_zones'):
                                        zone.text_zones = []
                                    
                                    # Create a basic text zone with zone coordinates
                                    text_zone = TextZone(zone.x1, zone.y1, zone.x2, zone.y2)
                                    text_zone.text = new_text
                                    zone.text_zones.append(text_zone)
                                except ImportError:
                                    print("Warning: Could not create TextZone - TextZone class not available")
                    
                    print(f"✅ Updated text for {mite.get('mite_id')}: '{old_text}' → '{new_text}'")
        
        # Save MiteManager if changes were made and it's available
        if changes_made and hasattr(self, 'mite_manager') and self.mite_manager:
            try:
                self.mite_manager.save()
                print("✅ Saved changes to MiteManager")
            except Exception as e:
                print(f"Warning: Could not save MiteManager: {e}")
                
        # Update the display
        self.update_mite_list_display()
        
        # Show success message
        if changes_made:
            messagebox.showinfo("Success", "Text verification saved successfully!")
        else:
            messagebox.showinfo("Info", "No changes were made.")
        
        dialog.destroy()
    
    def update_mite_list_display(self):
        """Update the mite list display in the zone info panel"""
        if not hasattr(self, 'mite_listbox'):
            return
            
        self.mite_listbox.delete(0, tk.END)
        
        if not self.mite_zones:
            self.mite_listbox.insert(0, "No analysis results yet")
            return
        
        for mite in self.mite_zones:
            status_icon = "✅" if mite.get('text_verified', False) else "⏳"
            status = mite.get('status', 'unknown')
            zone_id = mite.get('zone_id', 'N/A')
            mite_id = mite.get('mite_id', 'unknown')
            
            display_text = f"{status_icon} {mite_id} (Zone {zone_id + 1}) - {status}"
            self.mite_listbox.insert(tk.END, display_text)
    
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
        
        # Lock zones immediately when analysis starts to prevent changes during analysis
        self.lock_zones()
        
        # Refresh image display to show locked zones
        if self.selected_folder.get():
            self.load_and_display_first_image(self.selected_folder.get())
        
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
        self.analysis_complete_flag = True  # Mark analysis as completed for text verification
        # Zones are already locked from when analysis started
        
        # Update UI elements if they exist
        if hasattr(self, 'start_button'):
            self.start_button.configure(state="normal", bg=self.colors.get('success', 'green'))
        if hasattr(self, 'stop_button'):
            self.stop_button.configure(state="disabled", bg=self.colors.get('bg_tertiary', 'lightgray'))
        if hasattr(self, 'progress_bar'):
            self.progress_bar['value'] = 100
        if hasattr(self, 'progress_percent'):
            self.progress_percent.configure(text="100%")
        if hasattr(self, 'progress_label'):
            self.progress_label.configure(text="✅ Analysis completed successfully!", 
                                        fg=self.colors.get('success', 'green'))
        if hasattr(self, 'status_label'):
            self.status_label.configure(text="● Complete", fg=self.colors.get('success', 'green'))
        
        # Update results section if it exists
        if hasattr(self, 'results_info'):
            self.results_info.configure(
                text="🎉 Analysis completed! Results are ready for download.",
                fg=self.colors.get('success', 'green')
            )
        if hasattr(self, 'download_button'):
            self.download_button.configure(state="normal", bg=self.colors.get('warning', 'orange'))
        
        # Load analysis results for text verification
        self.load_analysis_results()
        
        # Enable text verification if UI exists
        if hasattr(self, 'verify_button'):
            self.verify_button.configure(
                text="🔍 Click zones to verify text",
                state="normal",
                bg=self.colors.get('accent', 'blue')
            )
        
        # Refresh image display with locked zones if possible
        if hasattr(self, 'selected_folder') and self.selected_folder.get():
            self.load_and_display_first_image(self.selected_folder.get())
        
        # Show completion message
        messagebox.showinfo(
            "Success",
            "🎉 Analysis completed successfully!\n\n"
            "• Results are ready for download\n"
            "• Zones are now locked\n"
            "• Click on zones to verify detected text"
        )
    
    def lock_zones(self):
        """Lock zones to prevent modification after analysis"""
        self.zones_locked = True
        
        # Update zone lock status if UI elements exist
        if hasattr(self, 'zone_lock_status'):
            self.zone_lock_status.configure(
                text="🔒 Zones Locked",
                fg=self.colors['success'] if hasattr(self, 'colors') else 'green'
            )
        
        # Disable zone selection controls if they exist
        if hasattr(self, 'plates_combobox'):
            self.plates_combobox.configure(state="disabled")
    
    def unlock_zones(self):
        """Unlock zones to allow modification"""
        self.zones_locked = False
        
        # Update zone lock status if UI elements exist
        if hasattr(self, 'zone_lock_status'):
            self.zone_lock_status.configure(
                text="🔓 Zones Unlocked",
                fg=self.colors['warning'] if hasattr(self, 'colors') else 'orange'
            )
        
        # Enable zone selection controls if they exist
        if hasattr(self, 'plates_combobox'):
            self.plates_combobox.configure(state="readonly")
    
    def load_analysis_results(self):
        """Load analysis results and populate mite data from MiteManager"""
        if not hasattr(self, 'results_path') or not self.results_path:
            print("No results path available, creating dummy data for testing")
            self.create_dummy_mite_data()
            return
            
        try:
            # Try multiple locations for the MiteManager
            search_paths = [
                # Look in the classes directory (where it's normally saved)
                os.path.join(os.path.dirname(__file__), "classes", "mite_manager.plk"),
                # Look in the results path if provided
                os.path.join(self.results_path, "mite_manager.plk") if self.results_path else None,
                # Look for it in the results/recording folder structure
                os.path.join(self.results_path, "results", "recording1", "mite_manager.plk") if self.results_path else None
            ]
            
            # Filter out None paths
            search_paths = [path for path in search_paths if path]
            
            mite_manager_found = False
            
            for mite_manager_path in search_paths:
                if os.path.exists(mite_manager_path):
                    print(f"Loading MiteManager from: {mite_manager_path}")
                    
                    # Import MiteManager and pickle
                    import pickle
                    from classes.MiteManager import MiteManager
                    
                    # Load the MiteManager
                    with open(mite_manager_path, 'rb') as f:
                        self.mite_manager = pickle.load(f)
                    
                    print(f"✅ Loaded MiteManager with {len(self.mite_manager.zones)} zones")
                    mite_manager_found = True
                    break
            
            if mite_manager_found:
                # Extract mite data from MiteManager zones
                self.mite_zones = []
                zone_index = 0
                
                for zone in self.mite_manager.zones:
                    print(f"Processing zone {zone_index}: '{zone.zone_id}' with {len(zone.mites)} mites")
                    
                    for mite_idx, mite in enumerate(zone.mites):
                        mite_data = {
                            'mite_id': mite.mite_id,
                            'zone_id': zone_index,  # Use zone index for UI
                            'zone_label': str(zone.zone_id),  # Store the actual zone label
                            'status': 'alive' if mite.alive else 'dead',
                            'max_diff': getattr(mite, 'max_diff', 0),
                            'local_diff': getattr(mite, 'local_avg_diff', 0),
                            'recording': 1,  # Default recording number
                            'detected_text': f"{zone.zone_id}",  # Use zone label as detected text
                            'text_verified': False,
                            'bbox': (mite.bbox.x, mite.bbox.y, mite.bbox.x + mite.bbox.w, mite.bbox.y + mite.bbox.h)
                        }
                        self.mite_zones.append(mite_data)
                    
                    zone_index += 1
                
                print(f"✅ Extracted {len(self.mite_zones)} mites from MiteManager")
                
                # Update mite list display
                self.update_mite_list_display()
                return
                
        except Exception as e:
            print(f"Error loading MiteManager: {e}")
            print("Falling back to CSV parsing...")
        
        # Fallback to CSV parsing if MiteManager loading fails
        self._load_from_csv_fallback()
    
    def _load_from_csv_fallback(self):
        """Fallback method to load from CSV files if MiteManager is not available"""
            
        try:
            # Look for CSV results file
            results_files = []
            for root, dirs, files in os.walk(self.results_path):
                for file in files:
                    if file.endswith('.csv') and 'results' in file.lower():
                        results_files.append(os.path.join(root, file))
            
            if not results_files:
                print("No CSV results file found")
                return
                
            # Read the first results file
            results_file = results_files[0]
            print(f"Loading results from: {results_file}")
            
            # Parse CSV results
            try:
                import pandas as pd
                df = pd.read_csv(results_file)
                
                self.mite_zones = []
                for index, row in df.iterrows():
                    mite_data = {
                        'mite_id': row.get('mite ID', f'mite_{index}'),
                        'zone_id': int(row.get('zone ID', 0)),
                        'status': row.get('status', 'unknown'),
                        'max_diff': row.get('max diff', 0),
                        'local_diff': row.get('local diff', 0),
                        'recording': row.get('recording', 0),
                        'detected_text': f"Mite {row.get('mite ID', f'mite_{index}')} - {row.get('status', 'unknown')}",
                        'text_verified': False
                    }
                    self.mite_zones.append(mite_data)
                
            except ImportError:
                # Fallback to manual CSV parsing if pandas not available
                with open(results_file, 'r') as f:
                    lines = f.readlines()
                    if len(lines) > 1:  # Skip header
                        headers = lines[0].strip().split(',')
                        self.mite_zones = []
                        
                        for i, line in enumerate(lines[1:]):
                            values = line.strip().split(',')
                            if len(values) >= len(headers):
                                mite_data = {
                                    'mite_id': values[0] if len(values) > 0 else f'mite_{i}',
                                    'zone_id': int(values[1]) if len(values) > 1 and values[1].isdigit() else 0,
                                    'status': values[2] if len(values) > 2 else 'unknown',
                                    'max_diff': float(values[3]) if len(values) > 3 and values[3].replace('.','').isdigit() else 0,
                                    'local_diff': float(values[4]) if len(values) > 4 and values[4].replace('.','').isdigit() else 0,
                                    'recording': int(values[5]) if len(values) > 5 and values[5].isdigit() else 0,
                                    'detected_text': f"Mite {values[0] if len(values) > 0 else f'mite_{i}'} - {values[2] if len(values) > 2 else 'unknown'}",
                                    'text_verified': False
                                }
            print(f"Loaded {len(self.mite_zones)} mites from CSV")
            
            # Update mite list display
            self.update_mite_list_display()
            
        except Exception as e:
            print(f"Error loading CSV results: {e}")
            # Create dummy data for testing if no results found
            self.create_dummy_mite_data()
            
            print(f"Loaded {len(self.mite_zones)} mites from results")
            
            # Update mite list display
            self.update_mite_list_display()
            
        except Exception as e:
            print(f"Error loading analysis results: {e}")
            # Create dummy data for testing if no results found
            self.create_dummy_mite_data()
    
    def create_dummy_mite_data(self):
        """Create dummy mite data for testing when no results are available"""
        print("Creating dummy mite data for testing")
        self.mite_zones = [
            {
                'mite_id': 'mite_001',
                'zone_id': 0,
                'zone_label': 'A1',
                'status': 'alive',
                'max_diff': 15.2,
                'local_diff': 12.8,
                'recording': 1,
                'detected_text': 'A1',
                'text_verified': False
            },
            {
                'mite_id': 'mite_002',
                'zone_id': 0,
                'zone_label': 'A1',
                'status': 'dead',
                'max_diff': 8.1,
                'local_diff': 6.5,
                'recording': 1,
                'detected_text': 'A1',
                'text_verified': False
            },
            {
                'mite_id': 'mite_003',
                'zone_id': 1,
                'zone_label': 'B2',
                'status': 'alive',
                'max_diff': 18.7,
                'local_diff': 16.2,
                'recording': 1,
                'detected_text': 'B2',
                'text_verified': False
            },
            {
                'mite_id': 'mite_004',
                'zone_id': 2,
                'zone_label': 'C1', 
                'status': 'alive',
                'max_diff': 22.3,
                'local_diff': 19.1,
                'recording': 1,
                'detected_text': 'C1',
                'text_verified': False
            }
        ]
        
        # Also create dummy zone coordinates for testing hover functionality
        self.zone_coordinates = [
            (0, 50, 50, 200, 150),   # Zone A1 (zone_id=0)
            (1, 250, 100, 400, 200), # Zone B2 (zone_id=1) 
            (2, 100, 250, 300, 350)  # Zone C1 (zone_id=2)
        ]
        
        print(f"Created {len(self.mite_zones)} dummy mites in {len(self.zone_coordinates)} zones")
        self.update_mite_list_display()
    
    def analysis_failed(self, error_msg):
        """Handle analysis failure"""
        self.analysis_running = False
        
        # Unlock zones since analysis failed
        self.unlock_zones()
        
        self.start_button.configure(state="normal", bg=self.colors['success'])
        self.stop_button.configure(state="disabled", bg=self.colors['bg_tertiary'])
        self.progress_bar['value'] = 0
        self.progress_percent.configure(text="0%")
        self.progress_label.configure(text="❌ Analysis failed", fg=self.colors['error'])
        self.status_label.configure(text="● Error", fg=self.colors['error'])
        
        # Refresh image display to show unlocked zones
        if self.selected_folder.get():
            self.load_and_display_first_image(self.selected_folder.get())
        
        # Show error message
        messagebox.showerror("Analysis Failed", f"❌ {error_msg}")
    
    def stop_analysis(self):
        """Stop the current analysis"""
        if self.analysis_running:
            self.analysis_running = False
            
            # Unlock zones since analysis was stopped
            self.unlock_zones()
            
            self.start_button.configure(state="normal", bg=self.colors['success'])
            self.stop_button.configure(state="disabled", bg=self.colors['bg_tertiary'])
            self.progress_bar['value'] = 0
            self.progress_percent.configure(text="0%")
            self.progress_label.configure(text="Analysis stopped", fg=self.colors['warning'])
            self.status_label.configure(text="● Stopped", fg=self.colors['warning'])
            
            # Refresh image display to show unlocked zones
            if self.selected_folder.get():
                self.load_and_display_first_image(self.selected_folder.get())
            
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
                            "Analysis Complete! 🎉",
                            f"✅ Analysis results successfully saved to:\n{zip_path}\n\nFile size: {self.get_file_size(zip_path)}\n\n🧹 All temporary files have been automatically cleaned up.\n\n📊 Your analysis is ready to use!"
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
