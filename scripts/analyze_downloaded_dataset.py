"""
Quick analysis of downloaded no_helmet dataset
"""
import os
from collections import Counter

dataset_path = r"all_datasets_raw\no_helmet_roboflow"

# Classes from data.yaml
classes = ['1-2-helmet', '3-4-helmet', 'Bald', 'Cap', 'Face and Hair', 'Full-face-helmet']

print("=" * 80)
print("📊 ANALYZING DOWNLOADED DATASET")
print("=" * 80)
print(f"\nDataset: {dataset_path}\n")
print(f"Classes: {classes}\n")

# Count instances per class
class_counts = Counter()

for split in ['train', 'valid', 'test']:
    labels_dir = os.path.join(dataset_path, split, 'labels')
    if not os.path.exists(labels_dir):
        continue
    
    label_files = [f for f in os.listdir(labels_dir) if f.endswith('.txt')]
    
    for label_file in label_files:
        label_path = os.path.join(labels_dir, label_file)
        with open(label_path, 'r') as f:
            for line in f:
                parts = line.strip().split()
                if parts:
                    class_id = int(parts[0])
                    class_counts[class_id] += 1

print("=" * 80)
print("CLASS DISTRIBUTION")
print("=" * 80)
for class_id in range(len(classes)):
    count = class_counts.get(class_id, 0)
    print(f"Class {class_id} ({classes[class_id]}): {count} instances")

print("\n" + "=" * 80)
print("ASSESSMENT")
print("=" * 80)

# Check if this is suitable
print("\n⚠️  This dataset has:")
print("  - Helmet types (1-2-helmet, 3-4-helmet, Full-face-helmet)")
print("  - Head states (Bald, Cap, Face and Hair)")
print("\n❌ This is NOT ideal for motorcycle no_helmet detection!")
print("\nWhat we need:")
print("  - Classes: 'helmet' and 'no_helmet' for motorcycle riders")
print("  - This dataset seems to classify helmet TYPES, not helmet vs no-helmet")
print("\n" + "=" * 80)
print("RECOMMENDATION")
print("=" * 80)
print("\n1. We could MAP classes:")
print("   - helmet: 1-2-helmet, 3-4-helmet, Full-face-helmet")
print("   - no_helmet: Bald, Cap, Face and Hair")
print("\n2. Better: Find a different dataset with clear 'helmet'/'no_helmet' classes")
print("\nWhich would you prefer?")
print("  A) Map these classes (may not be accurate)")
print("  B) Try a different dataset from Roboflow")
print("=" * 80)
