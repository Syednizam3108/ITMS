"""
Alternative: Extract No-Helmet Data from Existing Helmet Dataset
Check if your existing Helmet Detection dataset already has no_helmet annotations
"""

from pathlib import Path
from collections import Counter
from tqdm import tqdm
import shutil

print("=" * 80)
print("🔍 CHECKING EXISTING DATASETS FOR NO-HELMET DATA")
print("=" * 80)

# Check all existing datasets
datasets_dir = Path("all_datasets_raw")

if not datasets_dir.exists():
    print("❌ all_datasets_raw directory not found")
    exit(1)

print(f"\nScanning datasets in: {datasets_dir.absolute()}\n")

# Scan each dataset
for dataset_path in datasets_dir.iterdir():
    if not dataset_path.is_dir():
        continue
    
    print(f"\n📁 Checking: {dataset_path.name}")
    print("-" * 80)
    
    # Check for data.yaml
    data_yaml = dataset_path / "data.yaml"
    if data_yaml.exists():
        with open(data_yaml, 'r') as f:
            content = f.read()
        
        print("Classes found in data.yaml:")
        if 'names:' in content:
            # Extract class names
            in_names = False
            for line in content.split('\n'):
                if 'names:' in line:
                    in_names = True
                    continue
                if in_names:
                    if line.strip().startswith('-'):
                        class_name = line.strip('- ').strip()
                        print(f"  - {class_name}")
                        
                        # Check for no_helmet variations
                        if any(x in class_name.lower() for x in ['no_helmet', 'without_helmet', 'no-helmet', 'nohelmet']):
                            print(f"    ✅ FOUND NO-HELMET CLASS: '{class_name}'")
                    elif line.strip() and not line.startswith('#'):
                        # End of names section
                        break
    
    # Check labels for class distribution
    train_labels = dataset_path / "train" / "labels"
    if train_labels.exists():
        class_counts = Counter()
        label_files = list(train_labels.glob("*.txt"))
        
        if label_files:
            print(f"\nAnalyzing {len(label_files)} training labels...")
            for label_file in label_files:
                with open(label_file, 'r') as f:
                    for line in f:
                        parts = line.strip().split()
                        if len(parts) >= 5:
                            class_id = int(parts[0])
                            class_counts[class_id] += 1
            
            if class_counts:
                print("\nClass distribution:")
                for class_id, count in sorted(class_counts.items()):
                    print(f"  Class {class_id}: {count} instances")

print("\n" + "=" * 80)
print("💡 RECOMMENDATIONS")
print("=" * 80)
print("""
If you found a dataset with no_helmet class above:

1. Note the dataset name and class ID
2. You can extract just the no_helmet samples
3. Merge them with your current dataset

If NO no_helmet class was found:
→ You need to download a new dataset (use download_no_helmet_dataset.py)

Common helmet datasets that often include no_helmet:
- Helmet Detection datasets from Roboflow
- Motorcycle Safety datasets
- Traffic Violation datasets
""")

print("\n" + "=" * 80)
print("🚀 NEXT STEPS")
print("=" * 80)
print("""
Option A: If no_helmet found in existing datasets
  → I can create a script to extract and merge that data
  → Let me know which dataset and class ID

Option B: If no_helmet NOT found
  → Run: python download_no_helmet_dataset.py
  → Follow the guide to download from Roboflow
  → Come back for merge script

Option C: Skip no_helmet for now
  → Remove no_helmet from data.yaml
  → Retrain with current classes only
  → Add no_helmet later when data is available
""")

print("=" * 80)
