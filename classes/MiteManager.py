import cv2
from classes.mite import Mite
from classes.Rect import TextZone, MiteZone
from classes.TextReader import TextReader
from PIL import Image
import pandas as pd
import pickle
import os

class MiteManager:
    """Manages mites detection, zone assignment, and data processing."""

    def __init__(self, mites_detection, frames, coordinate_file, name):
        # Guard clauses
        if not mites_detection:
            raise ValueError("Mites detection results must be provided")
        if frames is None or len(frames) == 0:
            raise ValueError("Frames must be provided and not empty")
        if not coordinate_file:
            raise ValueError("Coordinate file must be provided")
        if not name:
            raise ValueError("Name must be provided")
        
        print("Initializing stage...")
        
        self._initialize_paths()
        
        if os.path.exists(self.save_path):
            self.load_miteManager(frames)
        else:
            self._initialize_new_manager(mites_detection, frames, coordinate_file, name)

    def _initialize_paths(self):
        """Initialize file paths."""
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.save_path = os.path.join(base_dir, "mite_manager.plk")

    def _initialize_new_manager(self, mites_detection, frames, coordinate_file, name):
        """Initialize a new MiteManager instance."""
        self.zones = []
        self.name = name
        self.frames = frames
        self.zone_map = {
            0: "text_zone",
            1: "mite_zone"
        }

        self.get_zones(coordinate_file)
        self.getMites(mites_detection)
        self.img_size = (15, 10)
        self.frame0 = None
        self.data = pd.DataFrame()
        self.mite_data = pd.DataFrame()
        self.reloaded = False
        

    def save(self):
        with open(self.save_path, 'wb') as f:
            pickle.dump(self, f)


    def load_miteManager(self,frames):
        with open(self.save_path, 'rb') as f:
            loaded = pickle.load(f)
            self.__dict__.update(loaded.__dict__)
            self.reloaded = True
            self.update_mites(frames)


    def load_coordinate_file(self, coordinate_file):
        """Load and validate coordinate file path."""
        if not coordinate_file:
            raise ValueError("Coordinate file path cannot be empty")
        
        if not os.path.isabs(coordinate_file):
            coordinate_file = os.path.abspath(
                os.path.join(
                    os.path.dirname(__file__),
                    "..",
                    coordinate_file
                )
            )
        
        if not os.path.exists(coordinate_file):
            raise FileNotFoundError(f"Coordinate file not found: {coordinate_file}")
        
        self.coordinate_file = coordinate_file

    def get_zones(self, coordinate_file):
        """Parse zones from coordinate file."""
        self.load_coordinate_file(coordinate_file)
        
        with open(self.coordinate_file, 'r') as f:
            for line_num, line in enumerate(f, 1):
                try:
                    self._process_zone_line(line, line_num)
                except ValueError as e:
                    print(f"Warning: Line {line_num} - {e}")
                    continue

    def _process_zone_line(self, line, line_num):
        """Process a single line from the coordinate file."""
        parts = line.strip().split()
        
        if len(parts) != 5:
            raise ValueError(f"Invalid line format (expected 5 parts, got {len(parts)}): {line.strip()}")

        try:
            class_id = int(parts[0])
            x1, y1, x2, y2 = map(float, parts[1:])
        except ValueError as e:
            raise ValueError(f"Invalid number format: {e}")

        if class_id not in self.zone_map:
            raise ValueError(f"Unknown class ID {class_id}")

        zone_id = self.zone_map[class_id]

        if zone_id == "mite_zone":
            self.zones.append(MiteZone(int(x1), int(y1), int(x2), int(y2)))
        elif zone_id == "text_zone":
            text_zone = TextZone(int(x1), int(y1), int(x2), int(y2))
            self._assign_text_zone_to_mite_zone(text_zone)

    def _assign_text_zone_to_mite_zone(self, text_zone):
        """Find and assign text zone to its parent mite zone."""
        for mite_zone in self.zones:
            if text_zone in mite_zone:
                text_zone.parent_rect = mite_zone
                mite_zone.add_text_zone(text_zone)
                return
        
        print(f"Warning: Text zone {text_zone} could not be assigned to any mite zone")


    def getMites(self, result):
        """Extract mites from detection results and assign them to zones."""
        # Guard clauses
        if not result or not hasattr(result, 'boxes'):
            print("Warning: No detection results or boxes found")
            return
        
        if not result.boxes.xyxy.numel():
            print("Warning: No bounding boxes in detection results")
            return

        boxes = result.boxes.xyxy.cpu().numpy().astype(int)
        assigned_count = 0
        
        print(f"Processing {len(boxes)} detected mites...")
        
        for i, box in enumerate(boxes):
            try:
                mite = Mite(box, self.frames)
                if self._assign_mite_to_zone(mite):
                    assigned_count += 1
            except Exception as e:
                print(f"Warning: Failed to process mite {i}: {e}")
                continue
        
        print(f"Got mites: {len(boxes)}")
        print(f"Assigned mites: {assigned_count}")
        
        self._read_zone_labels()

    def _assign_mite_to_zone(self, mite):
        """Assign a mite to an appropriate zone."""
        for zone in self.zones:
            if self._is_mite_in_valid_zone(mite, zone):
                return zone.assign_mites(mite)
        return False

    def _is_mite_in_valid_zone(self, mite, zone):
        """Check if mite is in zone but not overlapping text zones."""
        if mite.bbox not in zone:
            return False
        
        # Check that mite doesn't overlap with text zones
        for text_zone in zone.text_zones:
            if mite.bbox in text_zone:
                return False
        
        return True

    def _read_zone_labels(self):
        """Read labels from text zones using OCR."""
        text_reader = TextReader()
        print("Text reader loaded...")
        
        for zone in self.zones:
            if not zone.mites:  # Skip zones without mites
                continue
                
            for text_zone in zone.text_zones:
                try:
                    self._process_text_zone(text_zone, text_reader)
                except Exception as e:
                    print(f"Warning: Failed to read text from zone {text_zone}: {e}")

    def _process_text_zone(self, text_zone, text_reader):
        """Process a single text zone to extract label."""
        img = text_zone.get_ROI(self.frames)[0]
        img_PIL = Image.fromarray(img).convert("RGB")
        text_zone.text = text_reader.read(img_PIL)
        print(f"Read text: '{text_zone.text}' from zone {text_zone}")
        
        # Update the zone id for the parent zone
        if hasattr(text_zone, 'parent_rect') and text_zone.parent_rect:
            text_zone.parent_rect.zone_id = text_zone.text

    def reset(self):
        """Delete save file and reset object to default state."""
        if os.path.exists(self.save_path):
            os.remove(self.save_path)
            print(f"Deleted save file: {self.save_path}")

    def update_mites(self, frames):
        """Update mites with new frame data."""
        if frames is None or len(frames) == 0:
            raise ValueError("Frames must be provided and not empty")
        
        for zone in self.zones:
            for mite in zone.mites:
                mite.update_ROI(frames)

    def update_mite_status(self, ground_truth):
        """Update the status of all mites."""
        save = ground_truth in ['alive', 'dead']

        for zone in self.zones:
            print(f"Zone {zone.zone_id} has {len(zone.mites)} mites.")
            
            for mite in zone.mites:
                mite.update_status()
                mite.update_status_severin()
        
                if save:
                    mite.save_with_ground_truth(ground_truth)
        

    def save_data(self, recording_count):
        # Step 1: Prepare the data
        summary_data = []
        mite_data = []

        for zone in self.zones:
            if zone.zone_id == "EMPTY":
                continue

            total = len(zone.mites)
            alive = sum(1 for mite in zone.mites if mite.alive)
            dead = total - alive
            survival_pct = (alive / total * 100) if total > 0 else 0.0

          
            summary_data.append({
                "Zone ID": zone.zone_id,
                "Total Mites": total,
                "Alive Mites": alive,
                "Dead Mites": dead,
                "Survival %": round(survival_pct, 2),
                "recording": recording_count
            })

            # collect individual mite data
            for mite in zone.mites:
                mite_data.append(mite.to_dict(recording_count))


        if summary_data:
            df_summary = pd.DataFrame(summary_data)
            self.data = pd.concat([df_summary, self.data], ignore_index=True)
             #merge identicall labels
            self.data = (
                self.data
                .groupby(['Zone ID', 'recording'], as_index=False)
                .agg({
                    'Total Mites': 'sum',
                    'Alive Mites': 'sum',
                    'Dead Mites': 'sum',
                })
            )

            #recalculate survival rate after merge
            self.data['Survival %'] = ((self.data['Alive Mites'] / self.data['Total Mites']) * 100).round(2)


            # Sort by recording and Zone
            self.data = self.data.sort_values(by=['Zone ID', 'recording'])
           

        else:
            print("found no mites..")
        if mite_data:


            df_mites = pd.DataFrame(mite_data)

        
            self.mite_data = pd.concat([df_mites, self.mite_data], ignore_index=True)
            self.mite_data = self.mite_data.sort_values(by=['mite ID', 'recording'])
        else:
            print("NO Mite data found")


       

        
                
        return self.data, self.mite_data



       


       