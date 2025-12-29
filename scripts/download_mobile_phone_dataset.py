"""
Download Additional Mobile Phone Detection Datasets
Searches and downloads public datasets for mobile phone usage detection
"""

import os
import requests
from pathlib import Path
import zipfile
import shutil

print("=" * 80)
print("📥 MOBILE PHONE DATASET DOWNLOADER")
print("=" * 80)
print("\nThis script helps you download additional mobile phone detection datasets")
print("from various sources to supplement your training data.\n")

# Create download directory
DOWNLOAD_DIR = Path("mobile_phone_datasets")
DOWNLOAD_DIR.mkdir(exist_ok=True)

print(f"Download directory: {DOWNLOAD_DIR.absolute()}\n")

print("=" * 80)
print("📋 AVAILABLE DATASET SOURCES")
print("=" * 80)
print("""
1. Roboflow Universe - Cell Phone Detection Datasets
   URL: https://universe.roboflow.com/search?q=cell+phone+detection
   - Multiple datasets available
   - Pre-annotated in YOLO format
   - Free tier: 10,000 exports/month
   
2. Kaggle - Driver Phone Usage Datasets
   URL: https://www.kaggle.com/search?q=driver+phone+usage
   - State Farm Distracted Driver Detection
   - Driver Behavior datasets
   - Requires Kaggle account
   
3. Open Images Dataset - Phone Category
   URL: https://storage.googleapis.com/openimages/web/index.html
   - Search for "Mobile phone", "Telephone"
   - Large-scale dataset with annotations
   - Requires OIDv6 tools
   
4. COCO Dataset - Cell Phone Category
   URL: https://cocodataset.org/
   - Category ID: 77 (cell phone)
   - High-quality annotations
   - Requires COCO API

5. Custom Collection Sources:
   - Dashcam footage (YouTube with permission)
   - Traffic camera feeds (public domain)
   - Stock photo websites (with licensing)
""")

print("=" * 80)
print("🔧 MANUAL DOWNLOAD INSTRUCTIONS")
print("=" * 80)
print("""
RECOMMENDED APPROACH - Roboflow Universe:

1. Visit: https://universe.roboflow.com/
2. Search for: "mobile phone detection" OR "cell phone driver" OR "phone usage"
3. Select a dataset (look for YOLO format, 100+ images)
4. Click "Download" → Select "YOLO v8" format
5. Download the ZIP file
6. Extract to: all_datasets_raw/mobile_phone_additional/

Example datasets to search for:
- "Driver Cell Phone Detection"
- "Mobile Phone Usage Detection"
- "Distracted Driver Phone Dataset"
- "Phone While Driving Detection"

After downloading:
- Run the merge script to integrate with existing dataset
- Retrain the model with combined data
""")

print("=" * 80)
print("🔗 QUICK LINKS")
print("=" * 80)

quick_links = {
    "Roboflow Cell Phone Search": "https://universe.roboflow.com/search?q=cell+phone+detection",
    "Roboflow Driver Phone Search": "https://universe.roboflow.com/search?q=driver+phone",
    "Kaggle Distracted Driver": "https://www.kaggle.com/c/state-farm-distracted-driver-detection",
    "Open Images": "https://storage.googleapis.com/openimages/web/index.html",
    "COCO Dataset": "https://cocodataset.org/#explore",
}

for name, url in quick_links.items():
    print(f"  {name}")
    print(f"  → {url}\n")

print("=" * 80)
print("💡 TIPS FOR DATASET COLLECTION")
print("=" * 80)
print("""
1. Quality over Quantity:
   - Focus on diverse scenarios (day/night, different angles)
   - Ensure clear phone visibility
   - Variety in phone types and positions

2. Annotation Quality:
   - Verify bounding boxes are tight and accurate
   - Check for consistent labeling
   - Remove poor quality annotations

3. Dataset Balance:
   - Target: 100-200 mobile phone samples
   - Mix of training and validation sets
   - Diverse backgrounds and lighting conditions

4. Integration:
   - Place new datasets in all_datasets_raw/
   - Run merge_dataset.py to combine with existing data
   - Verify class mapping matches (mobile_phone = class 1)

5. Data Augmentation:
   - Use augment_mobile_phone_data.py after downloading
   - Augmentation can multiply your dataset 5-10x
   - Maintains annotation accuracy
""")

print("=" * 80)
print("📝 NEXT STEPS")
print("=" * 80)
print("""
After downloading datasets:

1. Extract to all_datasets_raw/[dataset_name]/
2. Verify YOLO format (images/ and labels/ folders)
3. Update dataset/data.yaml if needed
4. Run: python merge_dataset.py
5. Run: python augment_mobile_phone_data.py
6. Run: python retrain_with_augmented_data.py
7. Compare performance metrics

Estimated time to collect 100+ samples: 30-60 minutes
""")

print("=" * 80)
print("✅ DOWNLOAD GUIDE COMPLETE")
print("=" * 80)
print(f"\nDownload directory created: {DOWNLOAD_DIR.absolute()}")
print("\nReady to collect additional mobile phone training data!")
print("=" * 80)
