"""
Mobile Phone Data Augmentation Script
Augments existing mobile phone samples to increase training data from 11 to 100+ instances
Uses advanced augmentation techniques specific to phone detection scenarios
"""

import os
import cv2
import numpy as np
import albumentations as A
from pathlib import Path
import shutil
from tqdm import tqdm
import random

# Paths
DATASET_DIR = Path("dataset")
ORIGINAL_IMAGES = DATASET_DIR / "images" / "train"
ORIGINAL_LABELS = DATASET_DIR / "labels" / "train"
OUTPUT_IMAGES = DATASET_DIR / "images" / "train"
OUTPUT_LABELS = DATASET_DIR / "labels" / "train"

# Class mapping (from data.yaml)
CLASS_MAP = {
    0: 'helmet',
    1: 'mobile_phone',
    2: 'license_plate',
    3: 'motorcycle'
}

MOBILE_PHONE_CLASS_ID = 1

print("=" * 80)
print("🔧 MOBILE PHONE DATA AUGMENTATION TOOL")
print("=" * 80)
print(f"Target: Increase mobile phone samples from 11 to 100+ instances")
print(f"Method: Advanced augmentation with realistic transformations")
print("=" * 80)

# ============================================================================
# STEP 1: FIND ALL MOBILE PHONE SAMPLES
# ============================================================================

def find_mobile_phone_samples():
    """Find all images containing mobile phone labels"""
    print("\n📋 Step 1: Finding Mobile Phone Samples...")
    
    mobile_phone_files = []
    
    label_files = list(ORIGINAL_LABELS.glob("*.txt"))
    print(f"Scanning {len(label_files)} label files...")
    
    for label_file in tqdm(label_files, desc="Scanning"):
        with open(label_file, 'r') as f:
            lines = f.readlines()
            
        for line in lines:
            parts = line.strip().split()
            if len(parts) >= 5:
                class_id = int(parts[0])
                if class_id == MOBILE_PHONE_CLASS_ID:
                    # Find corresponding image
                    image_name = label_file.stem
                    for ext in ['.jpg', '.png', '.jpeg', '.JPG', '.PNG']:
                        image_path = ORIGINAL_IMAGES / f"{image_name}{ext}"
                        if image_path.exists():
                            mobile_phone_files.append({
                                'image': image_path,
                                'label': label_file,
                                'name': image_name
                            })
                            break
                    break
    
    print(f"✅ Found {len(mobile_phone_files)} images with mobile phone annotations")
    return mobile_phone_files

# ============================================================================
# STEP 2: ADVANCED AUGMENTATION PIPELINE
# ============================================================================

def create_augmentation_pipeline():
    """Create augmentation pipeline optimized for mobile phone detection"""
    
    # Pipeline 1: Brightness/Contrast variations (simulates different lighting)
    pipeline_brightness = A.Compose([
        A.RandomBrightnessContrast(brightness_limit=0.3, contrast_limit=0.3, p=1.0),
        A.HueSaturationValue(hue_shift_limit=10, sat_shift_limit=20, val_shift_limit=20, p=0.8),
    ], bbox_params=A.BboxParams(format='yolo', label_fields=['class_labels']))
    
    # Pipeline 2: Blur/Noise (simulates motion and camera quality)
    pipeline_blur = A.Compose([
        A.OneOf([
            A.MotionBlur(blur_limit=7, p=1.0),
            A.GaussianBlur(blur_limit=7, p=1.0),
            A.MedianBlur(blur_limit=7, p=1.0),
        ], p=1.0),
        A.GaussNoise(var_limit=(10.0, 50.0), p=0.5),
    ], bbox_params=A.BboxParams(format='yolo', label_fields=['class_labels']))
    
    # Pipeline 3: Geometric transformations
    pipeline_geometric = A.Compose([
        A.ShiftScaleRotate(shift_limit=0.1, scale_limit=0.2, rotate_limit=15, p=1.0),
        A.Perspective(scale=(0.05, 0.1), p=0.5),
    ], bbox_params=A.BboxParams(format='yolo', label_fields=['class_labels']))
    
    # Pipeline 4: Weather/Environmental effects
    pipeline_weather = A.Compose([
        A.OneOf([
            A.RandomRain(brightness_coefficient=0.9, drop_width=1, blur_value=5, p=1.0),
            A.RandomFog(fog_coef_lower=0.1, fog_coef_upper=0.3, p=1.0),
            A.RandomShadow(shadow_roi=(0, 0.5, 1, 1), num_shadows_lower=1, num_shadows_upper=2, p=1.0),
        ], p=1.0),
    ], bbox_params=A.BboxParams(format='yolo', label_fields=['class_labels']))
    
    # Pipeline 5: Color adjustments
    pipeline_color = A.Compose([
        A.RGBShift(r_shift_limit=20, g_shift_limit=20, b_shift_limit=20, p=1.0),
        A.ChannelShuffle(p=0.3),
        A.ToGray(p=0.1),
    ], bbox_params=A.BboxParams(format='yolo', label_fields=['class_labels']))
    
    # Pipeline 6: Advanced effects
    pipeline_advanced = A.Compose([
        A.CLAHE(clip_limit=4.0, tile_grid_size=(8, 8), p=0.5),
        A.Sharpen(alpha=(0.2, 0.5), lightness=(0.5, 1.0), p=0.5),
        A.Emboss(alpha=(0.2, 0.5), strength=(0.2, 0.7), p=0.3),
    ], bbox_params=A.BboxParams(format='yolo', label_fields=['class_labels']))
    
    # Pipeline 7: Combined realistic augmentation
    pipeline_combined = A.Compose([
        A.RandomBrightnessContrast(brightness_limit=0.2, contrast_limit=0.2, p=0.8),
        A.GaussNoise(var_limit=(10.0, 30.0), p=0.3),
        A.ShiftScaleRotate(shift_limit=0.05, scale_limit=0.1, rotate_limit=10, p=0.7),
        A.HueSaturationValue(hue_shift_limit=5, sat_shift_limit=10, val_shift_limit=10, p=0.5),
    ], bbox_params=A.BboxParams(format='yolo', label_fields=['class_labels']))
    
    return [
        pipeline_brightness,
        pipeline_blur,
        pipeline_geometric,
        pipeline_weather,
        pipeline_color,
        pipeline_advanced,
        pipeline_combined
    ]

# ============================================================================
# STEP 3: PARSE AND CONVERT LABELS
# ============================================================================

def parse_yolo_label(label_file):
    """Parse YOLO format label file"""
    bboxes = []
    class_labels = []
    
    with open(label_file, 'r') as f:
        lines = f.readlines()
    
    for line in lines:
        parts = line.strip().split()
        if len(parts) >= 5:
            class_id = int(parts[0])
            x_center = float(parts[1])
            y_center = float(parts[2])
            width = float(parts[3])
            height = float(parts[4])
            
            bboxes.append([x_center, y_center, width, height])
            class_labels.append(class_id)
    
    return bboxes, class_labels

def save_yolo_label(label_file, bboxes, class_labels):
    """Save YOLO format label file"""
    with open(label_file, 'w') as f:
        for bbox, class_id in zip(bboxes, class_labels):
            # Ensure values are within valid range
            x_center = max(0.0, min(1.0, bbox[0]))
            y_center = max(0.0, min(1.0, bbox[1]))
            width = max(0.0, min(1.0, bbox[2]))
            height = max(0.0, min(1.0, bbox[3]))
            
            f.write(f"{class_id} {x_center} {y_center} {width} {height}\n")

# ============================================================================
# STEP 4: AUGMENT SAMPLES
# ============================================================================

def augment_mobile_phone_samples(mobile_phone_files, target_count=100):
    """Augment mobile phone samples to reach target count"""
    print(f"\n🔄 Step 2: Augmenting Mobile Phone Samples...")
    print(f"Current samples: {len(mobile_phone_files)}")
    print(f"Target samples: {target_count}")
    print(f"Need to generate: {target_count - len(mobile_phone_files)} augmented samples")
    
    augmentations_per_image = (target_count - len(mobile_phone_files)) // len(mobile_phone_files) + 1
    print(f"Augmentations per image: {augmentations_per_image}")
    
    pipelines = create_augmentation_pipeline()
    generated_count = 0
    
    for sample in tqdm(mobile_phone_files, desc="Augmenting"):
        # Load image
        image = cv2.imread(str(sample['image']))
        if image is None:
            print(f"⚠️  Failed to load {sample['image']}")
            continue
        
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Load labels
        bboxes, class_labels = parse_yolo_label(sample['label'])
        
        if not bboxes:
            continue
        
        # Generate multiple augmented versions
        for aug_idx in range(augmentations_per_image):
            if generated_count >= target_count - len(mobile_phone_files):
                break
            
            # Select random pipeline
            pipeline = random.choice(pipelines)
            
            try:
                # Apply augmentation
                transformed = pipeline(image=image, bboxes=bboxes, class_labels=class_labels)
                
                aug_image = transformed['image']
                aug_bboxes = transformed['bboxes']
                aug_labels = transformed['class_labels']
                
                # Skip if no mobile phone bbox after augmentation
                if not aug_bboxes:
                    continue
                
                # Save augmented image
                aug_name = f"{sample['name']}_mobile_aug_{aug_idx}"
                aug_image_path = OUTPUT_IMAGES / f"{aug_name}.jpg"
                aug_label_path = OUTPUT_LABELS / f"{aug_name}.txt"
                
                # Convert back to BGR for saving
                aug_image_bgr = cv2.cvtColor(aug_image, cv2.COLOR_RGB2BGR)
                cv2.imwrite(str(aug_image_path), aug_image_bgr)
                
                # Save labels
                save_yolo_label(aug_label_path, aug_bboxes, aug_labels)
                
                generated_count += 1
                
            except Exception as e:
                print(f"\n⚠️  Error augmenting {sample['name']}: {e}")
                continue
    
    print(f"\n✅ Generated {generated_count} augmented samples")
    print(f"Total mobile phone samples now: {len(mobile_phone_files) + generated_count}")
    return generated_count

# ============================================================================
# STEP 5: VERIFY RESULTS
# ============================================================================

def verify_augmentation():
    """Verify the augmentation results"""
    print("\n✅ Step 3: Verifying Augmentation Results...")
    
    mobile_phone_count = 0
    total_instances = 0
    
    label_files = list(ORIGINAL_LABELS.glob("*.txt"))
    
    for label_file in tqdm(label_files, desc="Verifying"):
        with open(label_file, 'r') as f:
            lines = f.readlines()
        
        for line in lines:
            parts = line.strip().split()
            if len(parts) >= 5:
                class_id = int(parts[0])
                total_instances += 1
                if class_id == MOBILE_PHONE_CLASS_ID:
                    mobile_phone_count += 1
    
    print(f"\n📊 Final Statistics:")
    print(f"  Total annotations: {total_instances}")
    print(f"  Mobile phone instances: {mobile_phone_count}")
    print(f"  Improvement: {mobile_phone_count - 11} new instances (+{((mobile_phone_count - 11) / 11 * 100):.1f}%)")
    
    return mobile_phone_count

# ============================================================================
# STEP 6: GENERATE REPORT
# ============================================================================

def generate_augmentation_report(original_count, final_count, generated_count):
    """Generate augmentation report"""
    print("\n📝 Generating Augmentation Report...")
    
    report_path = Path("mobile_phone_augmentation_report.txt")
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("MOBILE PHONE DATA AUGMENTATION REPORT\n")
        f.write("=" * 80 + "\n\n")
        f.write(f"Generated: {Path(__file__).name}\n")
        f.write(f"Task: Increase mobile phone detection training data\n\n")
        
        f.write("-" * 80 + "\n")
        f.write("AUGMENTATION SUMMARY\n")
        f.write("-" * 80 + "\n")
        f.write(f"Original mobile phone samples: {original_count}\n")
        f.write(f"Generated augmented samples: {generated_count}\n")
        f.write(f"Total mobile phone instances: {final_count}\n")
        f.write(f"Improvement: {final_count - original_count} new instances (+{((final_count - original_count) / original_count * 100):.1f}%)\n\n")
        
        f.write("-" * 80 + "\n")
        f.write("AUGMENTATION TECHNIQUES USED\n")
        f.write("-" * 80 + "\n")
        f.write("1. Brightness/Contrast variations (different lighting conditions)\n")
        f.write("2. Blur and noise (motion blur, camera quality simulation)\n")
        f.write("3. Geometric transformations (rotation, scaling, perspective)\n")
        f.write("4. Weather effects (rain, fog, shadows)\n")
        f.write("5. Color adjustments (RGB shift, channel shuffle)\n")
        f.write("6. Advanced effects (CLAHE, sharpening, emboss)\n")
        f.write("7. Combined realistic augmentations\n\n")
        
        f.write("-" * 80 + "\n")
        f.write("NEXT STEPS\n")
        f.write("-" * 80 + "\n")
        f.write("1. ✅ Data augmentation completed\n")
        f.write("2. 🔄 Retrain model with augmented dataset\n")
        f.write("3. 📊 Compare performance metrics\n")
        f.write("4. 🎯 Evaluate mobile phone detection improvement\n\n")
        
        f.write("=" * 80 + "\n")
        f.write("END OF REPORT\n")
        f.write("=" * 80 + "\n")
    
    print(f"✅ Report saved to {report_path}")

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main execution function"""
    
    # Check if albumentations is available
    try:
        import albumentations
    except ImportError:
        print("\n❌ Error: 'albumentations' package not found")
        print("Installing albumentations...")
        os.system("pip install albumentations")
        print("\n✅ Please run the script again")
        return
    
    # Step 1: Find mobile phone samples
    mobile_phone_files = find_mobile_phone_samples()
    
    if len(mobile_phone_files) == 0:
        print("❌ No mobile phone samples found!")
        return
    
    original_count = len(mobile_phone_files)
    
    # Step 2: Augment samples
    generated_count = augment_mobile_phone_samples(mobile_phone_files, target_count=100)
    
    # Step 3: Verify results
    final_count = verify_augmentation()
    
    # Step 4: Generate report
    generate_augmentation_report(original_count, final_count, generated_count)
    
    print("\n" + "=" * 80)
    print("✅ MOBILE PHONE DATA AUGMENTATION COMPLETED!")
    print("=" * 80)
    print(f"\n📊 Summary:")
    print(f"  Original samples: {original_count}")
    print(f"  Generated samples: {generated_count}")
    print(f"  Total instances: {final_count}")
    print(f"\n🚀 Ready to retrain the model with improved dataset!")
    print("=" * 80)

if __name__ == "__main__":
    main()
