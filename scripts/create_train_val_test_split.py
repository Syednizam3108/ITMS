"""
Split dataset into train/val/test sets with proper stratification
Maintains class distribution across all splits
"""
import os
import shutil
import random
from pathlib import Path
from collections import defaultdict
from tqdm import tqdm

# Configuration
DATASET_DIR = r"dataset"
TRAIN_RATIO = 0.70
VAL_RATIO = 0.20
TEST_RATIO = 0.10

# Seed for reproducibility
random.seed(42)

print("=" * 80)
print("🔄 CREATING TRAIN/VAL/TEST SPLIT")
print("=" * 80)
print(f"\nSplit ratios:")
print(f"  Train: {TRAIN_RATIO*100:.0f}%")
print(f"  Val:   {VAL_RATIO*100:.0f}%")
print(f"  Test:  {TEST_RATIO*100:.0f}%")
print()

# Create temporary backup
BACKUP_DIR = r"dataset_backup_before_split"
if not os.path.exists(BACKUP_DIR):
    print("📦 Creating backup of current dataset...")
    shutil.copytree(DATASET_DIR, BACKUP_DIR)
    print(f"✅ Backup created: {BACKUP_DIR}\n")
else:
    print(f"⚠️  Backup already exists: {BACKUP_DIR}\n")

# Collect all images and their labels from backup
images_train = os.path.join(BACKUP_DIR, 'images', 'train')
labels_train = os.path.join(BACKUP_DIR, 'labels', 'train')
images_val = os.path.join(BACKUP_DIR, 'images', 'val')
labels_val = os.path.join(BACKUP_DIR, 'labels', 'val')

# Collect all image-label pairs
all_pairs = []

print("📋 Collecting all image-label pairs...")

# From train
if os.path.exists(images_train):
    for img_file in os.listdir(images_train):
        if img_file.lower().endswith(('.jpg', '.jpeg', '.png')):
            label_file = os.path.splitext(img_file)[0] + '.txt'
            img_path = os.path.join(images_train, img_file)
            label_path = os.path.join(labels_train, label_file)
            
            if os.path.exists(label_path):
                all_pairs.append((img_path, label_path, 'train'))

# From val
if os.path.exists(images_val):
    for img_file in os.listdir(images_val):
        if img_file.lower().endswith(('.jpg', '.jpeg', '.png')):
            label_file = os.path.splitext(img_file)[0] + '.txt'
            img_path = os.path.join(images_val, img_file)
            label_path = os.path.join(labels_val, label_file)
            
            if os.path.exists(label_path):
                all_pairs.append((img_path, label_path, 'val'))

print(f"✅ Found {len(all_pairs)} image-label pairs\n")

# Group by primary class (class with most instances in the image)
class_groups = defaultdict(list)

print("🏷️  Grouping by primary class...")
for img_path, label_path, source in tqdm(all_pairs):
    # Read label file to determine primary class
    class_counts = defaultdict(int)
    
    with open(label_path, 'r') as f:
        for line in f:
            parts = line.strip().split()
            if parts:
                class_id = int(parts[0])
                class_counts[class_id] += 1
    
    # Get primary class (most instances)
    if class_counts:
        primary_class = max(class_counts.items(), key=lambda x: x[1])[0]
        class_groups[primary_class].append((img_path, label_path))

print(f"\n✅ Grouped into {len(class_groups)} classes\n")

# Show class distribution
class_names = ['helmet', 'no_helmet', 'mobile_phone', 'triple_riding', 'license_plate', 'motorcycle']
print("Class distribution:")
for class_id, pairs in sorted(class_groups.items()):
    class_name = class_names[class_id] if class_id < len(class_names) else f"class_{class_id}"
    print(f"  Class {class_id} ({class_name}): {len(pairs)} images")
print()

# Stratified split
train_pairs = []
val_pairs = []
test_pairs = []

print("✂️  Performing stratified split...")
for class_id, pairs in class_groups.items():
    # Shuffle pairs for this class
    random.shuffle(pairs)
    
    # Calculate split points
    n = len(pairs)
    train_end = int(n * TRAIN_RATIO)
    val_end = train_end + int(n * VAL_RATIO)
    
    # Split
    train_pairs.extend(pairs[:train_end])
    val_pairs.extend(pairs[train_end:val_end])
    test_pairs.extend(pairs[val_end:])

# Shuffle final splits
random.shuffle(train_pairs)
random.shuffle(val_pairs)
random.shuffle(test_pairs)

print(f"\n✅ Split complete:")
print(f"  Train: {len(train_pairs)} images ({len(train_pairs)/len(all_pairs)*100:.1f}%)")
print(f"  Val:   {len(val_pairs)} images ({len(val_pairs)/len(all_pairs)*100:.1f}%)")
print(f"  Test:  {len(test_pairs)} images ({len(test_pairs)/len(all_pairs)*100:.1f}%)")
print()

# Create new directory structure
print("📁 Creating new directory structure...")

new_dirs = [
    os.path.join(DATASET_DIR, 'images', 'train'),
    os.path.join(DATASET_DIR, 'images', 'val'),
    os.path.join(DATASET_DIR, 'images', 'test'),
    os.path.join(DATASET_DIR, 'labels', 'train'),
    os.path.join(DATASET_DIR, 'labels', 'val'),
    os.path.join(DATASET_DIR, 'labels', 'test'),
]

# Clear existing directories
for dir_path in new_dirs:
    if os.path.exists(dir_path):
        shutil.rmtree(dir_path)
    os.makedirs(dir_path, exist_ok=True)

print("✅ Directories created\n")

# Copy files to new structure
def copy_split(pairs, split_name):
    """Copy images and labels to the split directory"""
    print(f"📦 Copying {split_name} split...")
    
    img_dir = os.path.join(DATASET_DIR, 'images', split_name)
    label_dir = os.path.join(DATASET_DIR, 'labels', split_name)
    
    for img_path, label_path in tqdm(pairs):
        # Copy image
        img_filename = os.path.basename(img_path)
        shutil.copy2(img_path, os.path.join(img_dir, img_filename))
        
        # Copy label
        label_filename = os.path.basename(label_path)
        shutil.copy2(label_path, os.path.join(label_dir, label_filename))
    
    print(f"✅ {split_name} split copied ({len(pairs)} images)\n")

# Copy all splits
copy_split(train_pairs, 'train')
copy_split(val_pairs, 'val')
copy_split(test_pairs, 'test')

# Verify final counts
print("=" * 80)
print("🔍 VERIFICATION")
print("=" * 80)
print()

for split in ['train', 'val', 'test']:
    img_count = len(os.listdir(os.path.join(DATASET_DIR, 'images', split)))
    label_count = len(os.listdir(os.path.join(DATASET_DIR, 'labels', split)))
    print(f"{split.upper():5s} - Images: {img_count:5d} | Labels: {label_count:5d}")

print()
print("=" * 80)
print("✅ SPLIT COMPLETE")
print("=" * 80)
print(f"\nDataset split into train/val/test with stratification")
print(f"Backup saved at: {BACKUP_DIR}")
print()
print("Next steps:")
print("  1. Verify split: python check_dataset_distribution.py")
print("  2. Update data.yaml if needed")
print("  3. Start training: python retrain_with_augmented_data.py")
print("=" * 80)
