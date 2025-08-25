import os
import random
import shutil
from glob import glob

# -------------------- CONFIG --------------------
# Replace with your absolute dataset path
DATASET_DIR = r"C:\Users\mateo\OneDrive\Escritorio\zivildienst\Agroscope_Varoa_detector\yolo_data"

IMG_DIR = os.path.join(DATASET_DIR, "images")
LBL_DIR = os.path.join(DATASET_DIR, "labels")
TRAIN_RATIO = 0.8                  # 80% train, 20% val

# Temporary dirs for splitting
TMP_IMG_DIR = os.path.join(DATASET_DIR, "images_split")
TMP_LBL_DIR = os.path.join(DATASET_DIR, "labels_split")

# Supported image extensions
EXTS = ["jpg","jpeg","png","bmp","tif","tiff","webp"]

# -------------------- COLLECT IMAGES --------------------
images = []
for ext in EXTS:
    # lower and upper case
    images.extend(glob(f"{IMG_DIR}/*.{ext}"))
    images.extend(glob(f"{IMG_DIR}/*.{ext.upper()}"))

if not images:
    raise RuntimeError(f"No images found in {IMG_DIR}. Check DATASET_DIR and extensions.")

# Debug: show first 5 images
print(f"Looking in: {IMG_DIR}")
print(f"Found {len(images)} images")
print("First 5 images:", images[:5])

# -------------------- SHUFFLE & SPLIT --------------------
random.shuffle(images)
n = len(images)
train_idx = int(n * TRAIN_RATIO)

datasets = {
    "train": images[:train_idx],
    "val": images[train_idx:]
}

# -------------------- CREATE TEMP SPLIT DIRS --------------------
for split in datasets.keys():
    os.makedirs(os.path.join(TMP_IMG_DIR, split), exist_ok=True)
    os.makedirs(os.path.join(TMP_LBL_DIR, split), exist_ok=True)

# -------------------- COPY FILES --------------------
for split, files in datasets.items():
    for img_path in files:
        fname = os.path.basename(img_path)
        lbl_path = os.path.join(LBL_DIR, os.path.splitext(fname)[0] + ".txt")

        shutil.copy(img_path, os.path.join(TMP_IMG_DIR, split, fname))
        if os.path.exists(lbl_path):
            shutil.copy(lbl_path, os.path.join(TMP_LBL_DIR, split, os.path.basename(lbl_path)))

# -------------------- OVERWRITE ORIGINAL DIRS --------------------
if os.path.exists(IMG_DIR):
    shutil.rmtree(IMG_DIR)
if os.path.exists(LBL_DIR):
    shutil.rmtree(LBL_DIR)

os.rename(TMP_IMG_DIR, IMG_DIR)
os.rename(TMP_LBL_DIR, LBL_DIR)

# -------------------- DONE --------------------
print(f"✅ Dataset split complete. Train: {len(datasets['train'])}, Val: {len(datasets['val'])}")
print(f"Train images path: {os.path.join(IMG_DIR, 'train')}")
print(f"Val images path: {os.path.join(IMG_DIR, 'val')}")
