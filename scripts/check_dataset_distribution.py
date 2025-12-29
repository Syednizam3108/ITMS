"""
Check Dataset Class Distribution
Analyzes the current dataset to see actual class distribution
"""

from pathlib import Path
from collections import Counter
from tqdm import tqdm

LABELS_DIR = Path("dataset/labels/train")

print("=" * 80)
print("📊 DATASET CLASS DISTRIBUTION ANALYSIS")
print("=" * 80)

# Class names from data.yaml
CLASS_NAMES = {
    0: 'helmet',
    1: 'no_helmet',
    2: 'mobile_phone',
    3: 'triple_riding',
    4: 'license_plate',
    5: 'motorcycle'
}

# Count instances
class_counts = Counter()
image_with_class = {i: set() for i in range(6)}
total_images = 0

label_files = list(LABELS_DIR.glob("*.txt"))
print(f"\nAnalyzing {len(label_files)} label files...")

for label_file in tqdm(label_files, desc="Scanning"):
    total_images += 1
    with open(label_file, 'r') as f:
        lines = f.readlines()
    
    for line in lines:
        parts = line.strip().split()
        if len(parts) >= 5:
            class_id = int(parts[0])
            class_counts[class_id] += 1
            image_with_class[class_id].add(label_file.stem)

print("\n" + "=" * 80)
print("CLASS DISTRIBUTION")
print("=" * 80)
print(f"{'Class ID':<10} {'Class Name':<20} {'Instances':<12} {'Images':<12} {'Percentage'}")
print("-" * 80)

total_instances = sum(class_counts.values())

for class_id in sorted(CLASS_NAMES.keys()):
    class_name = CLASS_NAMES[class_id]
    instances = class_counts[class_id]
    images = len(image_with_class[class_id])
    percentage = (instances / total_instances * 100) if total_instances > 0 else 0
    
    print(f"{class_id:<10} {class_name:<20} {instances:<12} {images:<12} {percentage:.2f}%")

print("-" * 80)
print(f"{'TOTAL':<10} {'':<20} {total_instances:<12} {total_images:<12} 100.00%")
print("=" * 80)

# Analysis
print("\n📋 ANALYSIS")
print("=" * 80)

# Find underrepresented classes (< 5% of total)
threshold = total_instances * 0.05
underrep = [(class_id, CLASS_NAMES[class_id], class_counts[class_id]) 
            for class_id in CLASS_NAMES.keys() if class_counts[class_id] < threshold]

if underrep:
    print("\n⚠️  Underrepresented Classes (< 5% of total):")
    for class_id, name, count in underrep:
        print(f"  - {name}: {count} instances ({count/total_instances*100:.2f}%)")
        print(f"    Recommendation: Augment to at least {int(threshold)} instances")
else:
    print("\n✅ All classes are reasonably balanced")

# Mobile phone specific analysis
mobile_count = class_counts[2]
mobile_images = len(image_with_class[2])
print(f"\n📱 Mobile Phone Detection:")
print(f"  - Instances: {mobile_count}")
print(f"  - Images with mobile phone: {mobile_images}")
print(f"  - Average per image: {mobile_count/mobile_images:.2f}")
print(f"  - Percentage of dataset: {mobile_count/total_instances*100:.2f}%")

if mobile_count < 200:
    print(f"\n  ⚠️  Consider augmenting mobile_phone class to 300+ instances")
    print(f"  Need to generate: {300 - mobile_count} more samples")
else:
    print(f"\n  ✅ Mobile phone class has sufficient data")

print("\n" + "=" * 80)
