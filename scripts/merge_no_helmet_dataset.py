"""
Merge no_helmet dataset with existing dataset
Maps downloaded classes to helmet/no_helmet
"""
import os
import shutil
from pathlib import Path

# Paths
SOURCE_DATASET = r"all_datasets_raw\no_helmet_roboflow"
TARGET_DATASET = r"dataset"

# Class mapping from downloaded dataset to our dataset
# Downloaded: ['1-2-helmet', '3-4-helmet', 'Bald', 'Cap', 'Face and Hair', 'Full-face-helmet']
# Our classes: 0:helmet, 1:no_helmet, 2:mobile_phone, 3:triple_riding, 4:license_plate, 5:motorcycle

CLASS_MAPPING = {
    0: 0,  # 1-2-helmet -> helmet
    1: 0,  # 3-4-helmet -> helmet
    2: 1,  # Bald -> no_helmet
    3: 1,  # Cap -> no_helmet
    4: 1,  # Face and Hair -> no_helmet
    5: 0,  # Full-face-helmet -> helmet
}

print("=" * 80)
print("🔄 MERGING NO-HELMET DATASET")
print("=" * 80)
print(f"\nSource: {SOURCE_DATASET}")
print(f"Target: {TARGET_DATASET}\n")

print("Class Mapping:")
print("  Downloaded -> Our Dataset")
print("  0 (1-2-helmet) -> 0 (helmet)")
print("  1 (3-4-helmet) -> 0 (helmet)")
print("  2 (Bald) -> 1 (no_helmet)")
print("  3 (Cap) -> 1 (no_helmet)")
print("  4 (Face and Hair) -> 1 (no_helmet)")
print("  5 (Full-face-helmet) -> 0 (helmet)")
print()

# Statistics
stats = {
    'helmet_added': 0,
    'no_helmet_added': 0,
    'images_copied': 0,
    'labels_created': 0,
    'skipped': 0
}

def remap_label_file(source_label_path, target_label_path):
    """Read source label, remap classes, write to target"""
    remapped_lines = []
    
    with open(source_label_path, 'r') as f:
        for line in f:
            parts = line.strip().split()
            if not parts:
                continue
            
            old_class_id = int(parts[0])
            new_class_id = CLASS_MAPPING[old_class_id]
            
            # Update statistics
            if new_class_id == 0:
                stats['helmet_added'] += 1
            elif new_class_id == 1:
                stats['no_helmet_added'] += 1
            
            # Create new line with remapped class
            new_line = f"{new_class_id} {' '.join(parts[1:])}\n"
            remapped_lines.append(new_line)
    
    # Write remapped labels
    with open(target_label_path, 'w') as f:
        f.writelines(remapped_lines)
    
    stats['labels_created'] += 1

def merge_split(split_name):
    """Merge train/valid/test split"""
    print(f"\n{'=' * 80}")
    print(f"Processing {split_name.upper()} split...")
    print(f"{'=' * 80}")
    
    source_images_dir = os.path.join(SOURCE_DATASET, split_name, 'images')
    source_labels_dir = os.path.join(SOURCE_DATASET, split_name, 'labels')
    
    # Map to our dataset structure (train/val instead of train/valid)
    target_split = 'train' if split_name == 'train' else 'val'
    target_images_dir = os.path.join(TARGET_DATASET, 'images', target_split)
    target_labels_dir = os.path.join(TARGET_DATASET, 'labels', target_split)
    
    if not os.path.exists(source_images_dir):
        print(f"⚠️  Skipping {split_name} - directory not found")
        return
    
    # Create target directories
    os.makedirs(target_images_dir, exist_ok=True)
    os.makedirs(target_labels_dir, exist_ok=True)
    
    # Get image files
    image_files = [f for f in os.listdir(source_images_dir) 
                   if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    
    print(f"Found {len(image_files)} images")
    
    for i, image_file in enumerate(image_files, 1):
        if i % 100 == 0:
            print(f"  Processing {i}/{len(image_files)}...")
        
        # Source paths
        source_image_path = os.path.join(source_images_dir, image_file)
        source_label_path = os.path.join(source_labels_dir, 
                                         os.path.splitext(image_file)[0] + '.txt')
        
        # Target paths - add prefix to avoid filename conflicts
        target_image_name = f"no_helmet_roboflow_{image_file}"
        target_label_name = f"no_helmet_roboflow_{os.path.splitext(image_file)[0]}.txt"
        
        target_image_path = os.path.join(target_images_dir, target_image_name)
        target_label_path = os.path.join(target_labels_dir, target_label_name)
        
        # Check if label exists
        if not os.path.exists(source_label_path):
            stats['skipped'] += 1
            continue
        
        # Copy image
        shutil.copy2(source_image_path, target_image_path)
        stats['images_copied'] += 1
        
        # Remap and copy label
        remap_label_file(source_label_path, target_label_path)
    
    print(f"✅ Completed {split_name}: {stats['images_copied']} images merged")

# Process each split
try:
    # Process train split
    merge_split('train')
    
    # Process valid split (maps to our val)
    merge_split('valid')
    
    # Process test split (also maps to val)
    merge_split('test')
    
    print("\n" + "=" * 80)
    print("✅ MERGE COMPLETE")
    print("=" * 80)
    print(f"\nStatistics:")
    print(f"  Images copied: {stats['images_copied']}")
    print(f"  Labels created: {stats['labels_created']}")
    print(f"  Helmet instances added: {stats['helmet_added']}")
    print(f"  No-helmet instances added: {stats['no_helmet_added']}")
    print(f"  Skipped (no labels): {stats['skipped']}")
    
    print("\n" + "=" * 80)
    print("🔍 NEXT STEPS")
    print("=" * 80)
    print("\n1. Verify merge:")
    print("   python check_dataset_distribution.py")
    print("\n2. Check for class balance:")
    print("   Should now see no_helmet instances!")
    print("\n3. If satisfied, retrain:")
    print("   python retrain_with_augmented_data.py")
    print("\n" + "=" * 80)
    
except Exception as e:
    print(f"\n❌ Error during merge: {e}")
    import traceback
    traceback.print_exc()
