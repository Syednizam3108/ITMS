"""
No-Helmet Detection Dataset Downloader
Guide and resources for collecting no-helmet/without helmet training data
"""

import os
from pathlib import Path

print("=" * 80)
print("🪖 NO-HELMET DATASET COLLECTION GUIDE")
print("=" * 80)
print("\nThis guide helps you find and download datasets for people NOT wearing helmets")
print("(riders without helmets on motorcycles/bikes)\n")

# Create download directory
DOWNLOAD_DIR = Path("no_helmet_datasets")
DOWNLOAD_DIR.mkdir(exist_ok=True)

print(f"Download directory: {DOWNLOAD_DIR.absolute()}\n")

print("=" * 80)
print("📋 RECOMMENDED DATASET SOURCES")
print("=" * 80)
print("""
1. Roboflow Universe - Helmet/No-Helmet Datasets ⭐ BEST OPTION
   
   Search queries to try:
   - "helmet detection"
   - "helmet no helmet"
   - "rider without helmet"
   - "motorcycle helmet detection"
   - "bike helmet safety"
   
   URL: https://universe.roboflow.com/search?q=helmet+detection
   
   What to look for:
   - Datasets with both "helmet" and "no_helmet" or "without_helmet" classes
   - Pre-annotated in YOLO format
   - 100+ images with no-helmet examples
   - Traffic/motorcycle context
   
   Example datasets:
   - "Helmet Detection" (many have both classes)
   - "Motorcycle Safety Detection"
   - "Rider Helmet Detection"

2. Kaggle - Helmet Safety Datasets
   
   URL: https://www.kaggle.com/search?q=helmet+detection
   
   Popular datasets:
   - "Motorcycle Helmet Detection Dataset"
   - "Helmet/No-Helmet Detection"
   - "Safety Helmet Detection"
   
   Note: May require format conversion to YOLO

3. Custom Collection from Existing Helmet Datasets
   
   Many helmet detection datasets include "no_helmet" class
   Check your existing datasets:
   - Helmet Detection YOLOv8.v1i.yolov8
   - May already have no_helmet annotations

4. Google Open Images Dataset
   
   Search for: "Person" + "Motorcycle" - "Helmet"
   This can find riders without helmets
   Requires manual annotation or OIDv6 tools
""")

print("=" * 80)
print("🔍 ROBOFLOW UNIVERSE - DETAILED INSTRUCTIONS")
print("=" * 80)
print("""
STEP-BY-STEP DOWNLOAD PROCESS:

1. Visit Roboflow Universe
   → https://universe.roboflow.com/

2. Search for datasets
   Try these searches:
   - "helmet detection"
   - "helmet no helmet detection"
   - "motorcycle helmet safety"

3. Filter results
   - Look for datasets with "helmet" AND "no_helmet" classes
   - Check dataset preview to verify both classes exist
   - Aim for 100+ images with no-helmet examples

4. Select a promising dataset
   Click on the dataset card to view details

5. Check class distribution
   - Look at the dataset page
   - Verify it has "no_helmet", "without_helmet", or similar class
   - Check number of annotations for that class

6. Download the dataset
   a) Click "Download" button
   b) Select format: "YOLOv8" ⚠️ IMPORTANT
   c) Choose download location
   d) Download the ZIP file

7. Extract and organize
   a) Extract ZIP to: all_datasets_raw/no_helmet_roboflow/
   b) Verify structure:
      - data.yaml (check class names)
      - train/images/ and train/labels/
      - valid/images/ and valid/labels/

8. Map class names
   If the dataset uses different names (e.g., "without_helmet", "no-helmet"):
   - Note the class name and ID
   - You'll need to update class mapping when merging
""")

print("=" * 80)
print("🔗 QUICK LINKS - CLICK TO OPEN")
print("=" * 80)

links = {
    "Roboflow - Helmet Detection": "https://universe.roboflow.com/search?q=helmet+detection",
    "Roboflow - Motorcycle Safety": "https://universe.roboflow.com/search?q=motorcycle+safety",
    "Roboflow - No Helmet": "https://universe.roboflow.com/search?q=no+helmet",
    "Kaggle - Helmet Detection": "https://www.kaggle.com/search?q=helmet+detection",
    "Kaggle - Motorcycle Helmet": "https://www.kaggle.com/search?q=motorcycle+helmet",
}

for name, url in links.items():
    print(f"\n  {name}")
    print(f"  → {url}")

print("\n" + "=" * 80)
print("✅ VERIFICATION CHECKLIST")
print("=" * 80)
print("""
Before downloading, verify the dataset has:

□ Both "helmet" AND "no_helmet" (or similar) classes
□ Motorcycle/bike context (not construction helmets)
□ At least 100 images with no-helmet annotations
□ YOLO format available (or easy to convert)
□ Clear, good quality images
□ Diverse scenarios (day/night, different angles)
□ Proper bounding box annotations

Dataset quality indicators:
✓ High annotation accuracy
✓ Balanced distribution between helmet/no_helmet
✓ Real-world traffic scenarios
✓ Multiple viewing angles
""")

print("=" * 80)
print("🛠️ AFTER DOWNLOADING")
print("=" * 80)
print("""
1. Extract dataset to: all_datasets_raw/no_helmet_[dataset_name]/

2. Check data.yaml file:
   - Verify class names
   - Note the class ID for "no_helmet" (might be different from 1)
   
3. Map to your classes:
   Your current classes:
   - 0: helmet
   - 1: no_helmet (EMPTY - needs data)
   - 2: mobile_phone
   - 3: triple_riding
   - 4: license_plate
   - 5: motorcycle

4. Create class mapping script:
   If downloaded dataset uses different IDs, you'll need to remap
   Example: If their no_helmet is class 1, map it to your class 1

5. Merge with existing dataset:
   Run: python merge_no_helmet_dataset.py
   (Script will be created after you download)

6. Verify merged dataset:
   Run: python check_dataset_distribution.py
   Should show no_helmet with 100+ instances

7. Retrain model:
   Run: python retrain_with_augmented_data.py
""")

print("=" * 80)
print("💡 PRO TIPS")
print("=" * 80)
print("""
1. Look for "Helmet Detection" datasets, not "Safety Helmet" datasets
   - Safety helmets = construction workers (not what you want)
   - Motorcycle helmets = traffic/riders (what you need)

2. Check dataset preview images before downloading
   - Make sure they show motorcyclists
   - Verify both helmet and no-helmet riders are present

3. Combine multiple small datasets
   - Download 2-3 smaller datasets
   - Merge them together
   - Get more diversity

4. Augmentation after download
   - Once you have 50-100 no_helmet samples
   - Run augmentation to reach 400+ instances
   - Similar to what we did for mobile_phone

5. Class name variations to look for:
   - "no_helmet"
   - "without_helmet"
   - "no-helmet"
   - "WithoutHelmet"
   - "rider_no_helmet"
""")

print("=" * 80)
print("🎯 RECOMMENDED DATASETS (Examples)")
print("=" * 80)
print("""
These are example searches that typically have good results:

1. Search: "helmet detection motorcycle"
   - Usually includes both classes
   - Traffic context
   - Good quality

2. Search: "rider helmet detection"
   - Focused on motorcycle riders
   - Often has no_helmet class
   
3. Search: "helmet safety detection"
   - May include both classes
   - Check if it's motorcycle or construction

4. Look for datasets tagged with:
   - "traffic safety"
   - "motorcycle detection"
   - "rider detection"
   - "helmet violation"
""")

print("=" * 80)
print("📝 NEXT STEPS")
print("=" * 80)
print("""
ACTION PLAN:

1. NOW: Visit Roboflow Universe
   → https://universe.roboflow.com/search?q=helmet+detection

2. Find a dataset with no_helmet class
   - Check dataset preview
   - Verify both helmet and no_helmet exist
   - Look for 100+ no_helmet samples

3. Download in YOLOv8 format
   - Click Download
   - Select "YOLOv8"
   - Save the ZIP

4. Extract to: all_datasets_raw/no_helmet_roboflow/

5. Come back and I'll help you:
   - Create the merge script
   - Map the classes correctly
   - Integrate with your dataset
   - Verify the results

Estimated time: 15-30 minutes
""")

print("=" * 80)
print("✅ GUIDE READY")
print("=" * 80)
print(f"\nDownload directory created: {DOWNLOAD_DIR.absolute()}")
print("\n🚀 Start by visiting: https://universe.roboflow.com/search?q=helmet+detection")
print("\nAfter downloading, let me know and I'll create the merge script!")
print("=" * 80)
