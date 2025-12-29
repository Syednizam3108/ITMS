import os
import shutil
import yaml
from glob import glob
from functools import partial
from collections import defaultdict

# === FINAL CLASS NAMES (Option A) ===
FINAL_CLASSES = [
    "helmet",
    "no_helmet",
    "mobile_phone",
    "triple_riding",
    "license_plate",
    "motorcycle"
]

# FIXED CLASS MAPPING (Based on your data.yaml files)
CLASS_MAPPING = {
    "helmet": 0,

    "licenseplate": 4,
    "license_plate": 4,
    "number_plate": 4,

    "0": 5,                   # motorcycle dataset incorrectly named "0"
    "motorcycle": 5,
    "bike": 5,
    "motorbike": 5,

    "phone": 2,
    "mobile_phone": 2,

    # Triple riding dataset
    "class_name_rename_delete_0__1_motorcycle__motorcycle__person": 3,
    "class_name_rename_delete_0__1_motorcycle_motorcycle_person": 3,
    "triple_riding": 3,
    "three_person": 3,

    # IGNORE
    "person": None,
}

# === Dataset folders (EXACT paths you requested) ===
DATASET_FOLDERS = [
    "Helmet Detection YOLOv8.v1i.yolov8",
    "license plate detection.v2-8-2.yolov8",
    "motorcycles.v2-combinedmotorcycles.yolov8",
    "Phone Usage Detection.v2i.yolov8",
    "Triple riding.v2-original.yolov8"
]

RAW_DATASETS = "all_datasets_raw"
FINAL_DATASET = "dataset"

# === Output folders ===
IMG_TRAIN = os.path.join(FINAL_DATASET, "images/train")
IMG_VAL   = os.path.join(FINAL_DATASET, "images/val")
LBL_TRAIN = os.path.join(FINAL_DATASET, "labels/train")
LBL_VAL   = os.path.join(FINAL_DATASET, "labels/val")

os.makedirs(IMG_TRAIN, exist_ok=True)
os.makedirs(IMG_VAL, exist_ok=True)
os.makedirs(LBL_TRAIN, exist_ok=True)
os.makedirs(LBL_VAL, exist_ok=True)

# === METRICS STORAGE ===
metrics = {
    "total_images": 0,
    "total_labels": 0,
    "missing_label_files": 0,
    "ignored_annotations": 0,
    "invalid_label_lines": 0,
    "class_distribution": defaultdict(int),
    "dataset_contribution": defaultdict(int)
}

print("\n=== STARTING CLEAN MERGE (Optimized for Apple M1) ===\n")

def process_label(lbl_path, out_lbl, raw_classes, mapping, metrics_shared, out_file_name):
    """Process label file (mapped + cleaned)."""
    try:
        with open(lbl_path, "r") as lf, open(os.path.join(out_lbl, out_file_name), "w") as out:
            for line in lf:
                parts = line.strip().split()
                if len(parts) != 5:
                    metrics_shared["invalid_label_lines"] += 1
                    continue

                old_id = int(parts[0])
                bbox = parts[1:]

                cls_name = raw_classes[old_id]

                if cls_name not in mapping:
                    metrics_shared["ignored_annotations"] += 1
                    continue

                new_id = mapping[cls_name]

                if new_id is None:
                    metrics_shared["ignored_annotations"] += 1
                    continue

                out.write(f"{new_id} {' '.join(bbox)}\n")

                metrics_shared["class_distribution"][new_id] += 1
                metrics_shared["total_labels"] += 1

    except Exception:
        pass


# === MAIN MERGE LOOP ===
for folder in DATASET_FOLDERS:
    dataset_path = os.path.join(RAW_DATASETS, folder)

    if not os.path.isdir(dataset_path):
        print(f"❌ Missing dataset folder: {folder}")
        continue

    print(f"\n📁 Processing: {folder}")

    yaml_path = os.path.join(dataset_path, "data.yaml")
    if not os.path.exists(yaml_path):
        print("⚠️ No data.yaml found — skipping")
        continue

    with open(yaml_path, "r") as f:
        data = yaml.safe_load(f)

    raw_classes = [c.lower().replace(" ", "_") for c in data["names"]]
    print("➡ Classes:", raw_classes)

    # Train + Valid folders
    for subset in ["train", "valid"]:
        img_dir = os.path.join(dataset_path, subset, "images")
        lbl_dir = os.path.join(dataset_path, subset, "labels")

        if not os.path.exists(img_dir):
            continue

        out_img = IMG_TRAIN if subset == "train" else IMG_VAL
        out_lbl = LBL_TRAIN if subset == "train" else LBL_VAL

        for img_path in glob(os.path.join(img_dir, "*.*")):
            filename = os.path.basename(img_path)
            name, ext = os.path.splitext(filename)

            new_img = f"{folder.replace(' ', '_')}_{name}{ext}"
            new_lbl = f"{folder.replace(' ', '_')}_{name}.txt"

            shutil.copyfile(img_path, os.path.join(out_img, new_img))

            metrics["total_images"] += 1
            metrics["dataset_contribution"][folder] += 1

            lbl_path = os.path.join(lbl_dir, f"{name}.txt")

            if not os.path.exists(lbl_path):
                metrics["missing_label_files"] += 1
                continue

            # Process label
            process_label(
                lbl_path, out_lbl, raw_classes,
                CLASS_MAPPING, metrics, new_lbl
            )

print("\n🎉 CLEAN MERGE COMPLETE!")

# === Write final data.yaml ===
final_yaml = {
    "train": "images/train",
    "val": "images/val",
    "nc": len(FINAL_CLASSES),
    "names": FINAL_CLASSES
}

with open(os.path.join(FINAL_DATASET, "data.yaml"), "w") as f:
    yaml.dump(final_yaml, f)

print("\n📄 Final data.yaml created successfully!")

# === PRINT METRICS ===
print("\n=== DATASET METRICS SUMMARY ===\n")
print(f"📌 Total Images: {metrics['total_images']}")
print(f"📌 Total Valid Labels: {metrics['total_labels']}")
print(f"⚠ Missing Label Files: {metrics['missing_label_files']}")
print(f"⚠ Invalid Label Lines Skipped: {metrics['invalid_label_lines']}")
print(f"⚠ Ignored Annotations: {metrics['ignored_annotations']}")

print("\n📊 Class Distribution:")
for cid, count in metrics["class_distribution"].items():
    print(f"  - {FINAL_CLASSES[cid]}: {count}")

print("\n📦 Dataset Contribution:")
for ds, count in metrics["dataset_contribution"].items():
    print(f"  - {ds}: {count} images")

print("\n=== DONE ===\n")
