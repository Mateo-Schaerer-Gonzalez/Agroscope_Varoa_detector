import os
import cv2
import numpy as np


COUNTER_FILE = ".count"


def get_frames(folder_path, discobox_run=True, reanalyze=True):
    frames_by_folder = {}

    # Resolve full folder path
    if discobox_run:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        folder_path = os.path.abspath(os.path.join(base_dir, "..", "..", folder_path))
    else:
        folder_path = os.path.abspath(folder_path)

    # Check if folder_path contains subfolders
    subfolders = sorted([
        os.path.join(folder_path, d)
        for d in os.listdir(folder_path)
        if os.path.isdir(os.path.join(folder_path, d))
    ])

    if not subfolders:
        subfolders = [folder_path]

    for subfolder in subfolders:
        frames = []
        for root, dirs, files in os.walk(subfolder, followlinks=True):
            for fname in files:
                if not fname.lower().endswith(".bmp"):
                    continue
                img_path = os.path.join(root, fname)
                img = cv2.imread(img_path)
                if img is None:
                    print(f"Skipped (not image or unreadable): {img_path}")
                    continue
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                frames.append(img)

        if frames:
            frames_by_folder[subfolder] = np.stack(frames)
            

    if not frames_by_folder:
        raise ValueError("No images found in folder or none could be loaded.")

    if not reanalyze:
        # Only return the last folder's stack
        last_folder = sorted(frames_by_folder.keys())[-1]
        return frames_by_folder[last_folder]

    # Else return all as list
    return list(frames_by_folder.values())




def draw_rects_from_polygon_labels(image_path, label_path, output_path):
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"Image not found: {image_path}")
    h, w = image.shape[:2]

    def extract_rect_from_polygon_line(line, image_width, image_height):
        parts = list(map(float, line.strip().split()))
        class_id = int(parts[0])
        coords = parts[1:]

        if len(coords) != 8:
            raise ValueError(f"Expected 8 coordinates, got {len(coords)}")

        x_coords = [coords[i] * image_width for i in range(0, 8, 2)]
        y_coords = [coords[i] * image_height for i in range(1, 8, 2)]

        x_min, x_max = int(min(x_coords)), int(max(x_coords))
        y_min, y_max = int(min(y_coords)), int(max(y_coords))

        return class_id, (x_min, y_min, x_max, y_max)

    with open(label_path, 'r') as f:
        lines = f.readlines()

    for line in lines:
        class_id, (x1, y1, x2, y2) = extract_rect_from_polygon_line(line, w, h)
        color = (0, 255, 0) if class_id == 0 else (0, 0, 255)
        cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)
        cv2.putText(image, f"Class {class_id}", (x1, max(y1 - 10, 0)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)

    cv2.imwrite(output_path, image)


def convert_yolo_to_coords(input_file, output_file, image_path):
    """Convert YOLO polygon format bounding boxes to pixel coordinates (x1, y1, x2, y2).
    
    Args:
        input_file (str): Path to the input file with YOLO format bounding boxes.
        output_file (str): Path to save the output file with pixel coordinates.
        image_path (str): Path to the image to get dimensions for conversion.
    
    Output format:
        class_id x1 y1 x2 y2  (pixel coordinates)
    """
    # Load image using cv2
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(f"Image not found or unable to open: {image_path}")
    
    img_height, img_width = img.shape[:2]
    print(f"Image size: {img_width}x{img_height}")

    with open(input_file, 'r') as f_in, open(output_file, 'w') as f_out:
        for line in f_in:
            parts = line.strip().split()
            if len(parts) != 9:
                print(f"Skipping invalid line (expected 9 elements): {line.strip()}")
                continue

            class_id = parts[0]
            coords = list(map(float, parts[1:]))

            xs = coords[0::2]
            ys = coords[1::2]

            min_x, max_x = min(xs), max(xs)
            min_y, max_y = min(ys), max(ys)

            # Convert normalized coordinates to pixel coordinates
            x1_px = min_x * img_width
            y1_px = min_y * img_height
            x2_px = max_x * img_width
            y2_px = max_y * img_height

            f_out.write(f"{class_id} {x1_px:.2f} {y1_px:.2f} {x2_px:.2f} {y2_px:.2f}\n")

    print(f"Conversion complete! Output saved to {output_file}")


def read_counter():
    if os.path.exists(COUNTER_FILE):
        with open(COUNTER_FILE, "r") as f:
            try:
                return int(f.read().strip())
            except ValueError:
                return 0
    return 0

def write_counter(count):
    with open(COUNTER_FILE, "w") as f:
        f.write(str(count))

def reset_counter():
    if os.path.exists(COUNTER_FILE):
        os.remove(COUNTER_FILE)
