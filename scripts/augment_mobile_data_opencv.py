"""
Mobile Phone Data Augmentation Script (OpenCV-based)
Augments existing mobile phone samples using OpenCV only - no albumentations dependency
Increases training data from 11 to 100+ instances
"""

import os
import cv2
import numpy as np
from pathlib import Path
from tqdm import tqdm
import random

# Paths
DATASET_DIR = Path("dataset")
ORIGINAL_IMAGES = DATASET_DIR / "images" / "train"
ORIGINAL_LABELS = DATASET_DIR / "labels" / "train"
OUTPUT_IMAGES = DATASET_DIR / "images" / "train"
OUTPUT_LABELS = DATASET_DIR / "labels" / "train"

MOBILE_PHONE_CLASS_ID = 2  # mobile_phone is class 2 in data.yaml

print("=" * 80)
print("🔧 MOBILE PHONE DATA AUGMENTATION TOOL (OpenCV)")
print("=" * 80)
print(f"Target: Increase mobile phone samples from 11 to 100+ instances")
print(f"Method: Advanced augmentation with realistic transformations")
print("=" * 80)

# ============================================================================
# AUGMENTATION FUNCTIONS
# ============================================================================

def adjust_brightness_contrast(image, alpha=1.0, beta=0):
    """Adjust brightness and contrast"""
    return cv2.convertScaleAbs(image, alpha=alpha, beta=beta)

def add_gaussian_noise(image, mean=0, sigma=25):
    """Add Gaussian noise"""
    noise = np.random.normal(mean, sigma, image.shape).astype(np.uint8)
    return cv2.add(image, noise)

def apply_blur(image, blur_type='gaussian', kernel_size=5):
    """Apply blur effect"""
    if blur_type == 'gaussian':
        return cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)
    elif blur_type == 'median':
        return cv2.medianBlur(image, kernel_size)
    elif blur_type == 'motion':
        # Create motion blur kernel
        kernel = np.zeros((kernel_size, kernel_size))
        kernel[int((kernel_size-1)/2), :] = np.ones(kernel_size)
        kernel = kernel / kernel_size
        return cv2.filter2D(image, -1, kernel)
    return image

def adjust_hsv(image, h_shift=0, s_scale=1.0, v_scale=1.0):
    """Adjust HSV values"""
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV).astype(np.float32)
    hsv[:, :, 0] = (hsv[:, :, 0] + h_shift) % 180
    hsv[:, :, 1] = np.clip(hsv[:, :, 1] * s_scale, 0, 255)
    hsv[:, :, 2] = np.clip(hsv[:, :, 2] * v_scale, 0, 255)
    return cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)

def rotate_image(image, angle, bboxes):
    """Rotate image and adjust bounding boxes"""
    h, w = image.shape[:2]
    center = (w // 2, h // 2)
    
    # Rotation matrix
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h), borderMode=cv2.BORDER_REFLECT)
    
    # Adjust bounding boxes
    new_bboxes = []
    for bbox in bboxes:
        class_id, x_center, y_center, width, height = bbox
        
        # Convert to pixel coordinates
        x_c_px = x_center * w
        y_c_px = y_center * h
        
        # Rotate center point
        cos_a = np.cos(np.radians(angle))
        sin_a = np.sin(np.radians(angle))
        x_c_new = center[0] + (x_c_px - center[0]) * cos_a - (y_c_px - center[1]) * sin_a
        y_c_new = center[1] + (x_c_px - center[0]) * sin_a + (y_c_px - center[1]) * cos_a
        
        # Convert back to normalized coordinates
        x_center_new = x_c_new / w
        y_center_new = y_c_new / h
        
        # Keep width and height (approximate)
        new_bboxes.append([class_id, x_center_new, y_center_new, width, height])
    
    return rotated, new_bboxes

def flip_horizontal(image, bboxes):
    """Flip image horizontally"""
    flipped = cv2.flip(image, 1)
    
    new_bboxes = []
    for bbox in bboxes:
        class_id, x_center, y_center, width, height = bbox
        x_center_new = 1.0 - x_center
        new_bboxes.append([class_id, x_center_new, y_center, width, height])
    
    return flipped, new_bboxes

def add_shadow(image):
    """Add random shadow effect"""
    h, w = image.shape[:2]
    
    # Random shadow position
    x1 = random.randint(0, w // 2)
    y1 = random.randint(0, h // 2)
    x2 = random.randint(w // 2, w)
    y2 = random.randint(h // 2, h)
    
    # Create shadow mask
    mask = np.zeros((h, w), dtype=np.uint8)
    cv2.rectangle(mask, (x1, y1), (x2, y2), 255, -1)
    mask = cv2.GaussianBlur(mask, (51, 51), 0)
    
    # Apply shadow
    shadow_intensity = random.uniform(0.3, 0.7)
    result = image.copy().astype(np.float32)
    for c in range(3):
        result[:, :, c] = result[:, :, c] * (1 - shadow_intensity * mask / 255.0)
    
    return np.clip(result, 0, 255).astype(np.uint8)

def apply_clahe(image):
    """Apply CLAHE (Contrast Limited Adaptive Histogram Equalization)"""
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    lab[:, :, 0] = clahe.apply(lab[:, :, 0])
    return cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)

def scale_image(image, scale, bboxes):
    """Scale image"""
    h, w = image.shape[:2]
    new_h, new_w = int(h * scale), int(w * scale)
    
    scaled = cv2.resize(image, (new_w, new_h))
    
    # Crop or pad to original size
    if scale > 1.0:
        # Crop center
        start_y = (new_h - h) // 2
        start_x = (new_w - w) // 2
        result = scaled[start_y:start_y+h, start_x:start_x+w]
    else:
        # Pad
        result = np.zeros((h, w, 3), dtype=np.uint8)
        start_y = (h - new_h) // 2
        start_x = (w - new_w) // 2
        result[start_y:start_y+new_h, start_x:start_x+new_w] = scaled
    
    return result, bboxes  # Bboxes remain approximately the same in normalized coords

# ============================================================================
# AUGMENTATION PIPELINES
# ============================================================================

def get_augmentation_pipelines():
    """Define augmentation pipelines"""
    return [
        # Pipeline 1: Brightness variations
        lambda img, bbox: (adjust_brightness_contrast(img, alpha=random.uniform(0.7, 1.3), beta=random.randint(-30, 30)), bbox),
        
        # Pipeline 2: Blur
        lambda img, bbox: (apply_blur(img, blur_type=random.choice(['gaussian', 'median', 'motion']), kernel_size=5), bbox),
        
        # Pipeline 3: Rotation
        lambda img, bbox: rotate_image(img, random.uniform(-15, 15), bbox),
        
        # Pipeline 4: HSV adjustment
        lambda img, bbox: (adjust_hsv(img, h_shift=random.randint(-10, 10), s_scale=random.uniform(0.8, 1.2), v_scale=random.uniform(0.8, 1.2)), bbox),
        
        # Pipeline 5: Noise
        lambda img, bbox: (add_gaussian_noise(img, sigma=random.randint(10, 30)), bbox),
        
        # Pipeline 6: Shadow
        lambda img, bbox: (add_shadow(img), bbox),
        
        # Pipeline 7: CLAHE
        lambda img, bbox: (apply_clahe(img), bbox),
        
        # Pipeline 8: Horizontal flip
        lambda img, bbox: flip_horizontal(img, bbox),
        
        # Pipeline 9: Scale
        lambda img, bbox: scale_image(img, random.uniform(0.9, 1.1), bbox),
        
        # Pipeline 10: Combined effects
        lambda img, bbox: (
            add_gaussian_noise(
                adjust_brightness_contrast(
                    adjust_hsv(img, h_shift=random.randint(-5, 5), s_scale=random.uniform(0.9, 1.1), v_scale=random.uniform(0.9, 1.1)),
                    alpha=random.uniform(0.9, 1.1),
                    beta=random.randint(-20, 20)
                ),
                sigma=random.randint(5, 15)
            ),
            bbox
        ),
    ]

# ============================================================================
# FIND MOBILE PHONE SAMPLES
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
# PARSE AND SAVE LABELS
# ============================================================================

def parse_yolo_label(label_file):
    """Parse YOLO format label file"""
    bboxes = []
    
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
            bboxes.append([class_id, x_center, y_center, width, height])
    
    return bboxes

def save_yolo_label(label_file, bboxes):
    """Save YOLO format label file"""
    with open(label_file, 'w') as f:
        for bbox in bboxes:
            class_id, x_center, y_center, width, height = bbox
            # Ensure values are within valid range
            x_center = max(0.0, min(1.0, x_center))
            y_center = max(0.0, min(1.0, y_center))
            width = max(0.0, min(1.0, width))
            height = max(0.0, min(1.0, height))
            
            f.write(f"{class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n")

# ============================================================================
# AUGMENT SAMPLES
# ============================================================================

def augment_mobile_phone_samples(mobile_phone_files, target_count=400):
    """Augment mobile phone samples to reach target count"""
    print(f"\n🔄 Step 2: Augmenting Mobile Phone Samples...")
    print(f"Current samples: {len(mobile_phone_files)}")
    print(f"Target samples: {target_count}")
    print(f"Need to generate: {target_count - len(mobile_phone_files)} augmented samples")
    
    augmentations_per_image = (target_count - len(mobile_phone_files)) // len(mobile_phone_files) + 1
    print(f"Augmentations per image: ~{augmentations_per_image}")
    
    pipelines = get_augmentation_pipelines()
    generated_count = 0
    
    for sample in tqdm(mobile_phone_files, desc="Augmenting"):
        # Load image
        image = cv2.imread(str(sample['image']))
        if image is None:
            print(f"\n⚠️  Failed to load {sample['image']}")
            continue
        
        # Load labels
        bboxes = parse_yolo_label(sample['label'])
        if not bboxes:
            continue
        
        # Generate multiple augmented versions
        for aug_idx in range(augmentations_per_image):
            if generated_count >= target_count - len(mobile_phone_files):
                break
            
            try:
                # Select random pipeline
                pipeline = random.choice(pipelines)
                
                # Apply augmentation
                aug_image, aug_bboxes = pipeline(image.copy(), bboxes.copy())
                
                # Skip if no bboxes after augmentation
                if not aug_bboxes:
                    continue
                
                # Save augmented image
                aug_name = f"{sample['name']}_mobile_aug_{aug_idx}_{generated_count}"
                aug_image_path = OUTPUT_IMAGES / f"{aug_name}.jpg"
                aug_label_path = OUTPUT_LABELS / f"{aug_name}.txt"
                
                cv2.imwrite(str(aug_image_path), aug_image)
                save_yolo_label(aug_label_path, aug_bboxes)
                
                generated_count += 1
                
            except Exception as e:
                print(f"\n⚠️  Error augmenting {sample['name']}: {e}")
                continue
    
    print(f"\n✅ Generated {generated_count} augmented samples")
    print(f"Total mobile phone samples now: {len(mobile_phone_files) + generated_count}")
    return generated_count

# ============================================================================
# VERIFY RESULTS
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
    if mobile_phone_count > 11:
        print(f"  Improvement: {mobile_phone_count - 11} new instances (+{((mobile_phone_count - 11) / 11 * 100):.1f}%)")
    
    return mobile_phone_count

# ============================================================================
# GENERATE REPORT
# ============================================================================

def generate_augmentation_report(original_count, final_count, generated_count):
    """Generate augmentation report"""
    print("\n📝 Generating Augmentation Report...")
    
    report_path = Path("mobile_phone_augmentation_report.txt")
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("MOBILE PHONE DATA AUGMENTATION REPORT\n")
        f.write("=" * 80 + "\n\n")
        f.write(f"Method: OpenCV-based augmentation\n")
        f.write(f"Task: Increase mobile phone detection training data\n\n")
        
        f.write("-" * 80 + "\n")
        f.write("AUGMENTATION SUMMARY\n")
        f.write("-" * 80 + "\n")
        f.write(f"Original mobile phone samples: {original_count}\n")
        f.write(f"Generated augmented samples: {generated_count}\n")
        f.write(f"Total mobile phone instances: {final_count}\n")
        if final_count > original_count:
            f.write(f"Improvement: {final_count - original_count} new instances (+{((final_count - original_count) / original_count * 100):.1f}%)\n\n")
        
        f.write("-" * 80 + "\n")
        f.write("AUGMENTATION TECHNIQUES USED\n")
        f.write("-" * 80 + "\n")
        f.write("1. Brightness/Contrast variations (different lighting conditions)\n")
        f.write("2. Blur effects (motion, gaussian, median)\n")
        f.write("3. Rotation (±15 degrees)\n")
        f.write("4. HSV adjustments (hue, saturation, value)\n")
        f.write("5. Gaussian noise (camera sensor noise)\n")
        f.write("6. Random shadows\n")
        f.write("7. CLAHE (contrast enhancement)\n")
        f.write("8. Horizontal flipping\n")
        f.write("9. Scaling variations\n")
        f.write("10. Combined realistic augmentations\n\n")
        
        f.write("-" * 80 + "\n")
        f.write("NEXT STEPS\n")
        f.write("-" * 80 + "\n")
        f.write("1. ✅ Data augmentation completed\n")
        f.write("2. 🔄 Retrain model: python retrain_with_augmented_data.py\n")
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
    
    # Step 1: Find mobile phone samples
    mobile_phone_files = find_mobile_phone_samples()
    
    if len(mobile_phone_files) == 0:
        print("❌ No mobile phone samples found!")
        return
    
    original_count = len(mobile_phone_files)
    
    # Step 2: Augment samples
    generated_count = augment_mobile_phone_samples(mobile_phone_files, target_count=400)
    
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
    print(f"\n🚀 Next step: Run training script")
    print(f"  python retrain_with_augmented_data.py")
    print("=" * 80)

if __name__ == "__main__":
    main()
