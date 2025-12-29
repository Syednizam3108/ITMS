"""
Augment mobile_phone class to reach 5% threshold
Only augments in training set
"""
import os
import cv2
import numpy as np
from pathlib import Path
import random
from tqdm import tqdm

# Configuration
DATASET_DIR = r"dataset"
TRAIN_IMAGES_DIR = os.path.join(DATASET_DIR, 'images', 'train')
TRAIN_LABELS_DIR = os.path.join(DATASET_DIR, 'labels', 'train')
MOBILE_PHONE_CLASS_ID = 2
TARGET_INSTANCES = 337  # Need at least 8 more instances
CURRENT_INSTANCES = 329

INSTANCES_TO_ADD = TARGET_INSTANCES - CURRENT_INSTANCES + 20  # Add 20 extra for buffer

random.seed(42)

print("=" * 80)
print("📱 MOBILE PHONE CLASS AUGMENTATION")
print("=" * 80)
print(f"\nCurrent instances: {CURRENT_INSTANCES}")
print(f"Target instances: {TARGET_INSTANCES}")
print(f"Will generate: {INSTANCES_TO_ADD} new instances")
print()

# Find all images with mobile_phone class
mobile_phone_images = []

print("🔍 Finding images with mobile_phone class...")
for label_file in os.listdir(TRAIN_LABELS_DIR):
    if not label_file.endswith('.txt'):
        continue
    
    label_path = os.path.join(TRAIN_LABELS_DIR, label_file)
    
    with open(label_path, 'r') as f:
        for line in f:
            parts = line.strip().split()
            if parts and int(parts[0]) == MOBILE_PHONE_CLASS_ID:
                # Found mobile_phone instance
                image_name = os.path.splitext(label_file)[0]
                # Find corresponding image
                for ext in ['.jpg', '.jpeg', '.png', '.JPG', '.JPEG', '.PNG']:
                    img_path = os.path.join(TRAIN_IMAGES_DIR, image_name + ext)
                    if os.path.exists(img_path):
                        mobile_phone_images.append((img_path, label_path))
                        break
                break  # Only count each image once

print(f"✅ Found {len(mobile_phone_images)} images with mobile_phone\n")

if len(mobile_phone_images) == 0:
    print("❌ No mobile_phone images found!")
    exit(1)

# Augmentation functions
def augment_brightness_contrast(img):
    """Random brightness and contrast adjustment"""
    alpha = random.uniform(0.8, 1.3)  # Contrast
    beta = random.randint(-30, 30)    # Brightness
    return cv2.convertScaleAbs(img, alpha=alpha, beta=beta)

def augment_blur(img):
    """Apply Gaussian blur"""
    kernel_size = random.choice([3, 5])
    return cv2.GaussianBlur(img, (kernel_size, kernel_size), 0)

def augment_hsv(img):
    """Adjust HSV values"""
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV).astype(np.float32)
    hsv[:, :, 0] *= random.uniform(0.9, 1.1)  # Hue
    hsv[:, :, 1] *= random.uniform(0.9, 1.1)  # Saturation
    hsv[:, :, 2] *= random.uniform(0.9, 1.1)  # Value
    hsv = np.clip(hsv, 0, 255).astype(np.uint8)
    return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

def augment_noise(img):
    """Add random noise"""
    noise = np.random.normal(0, 10, img.shape).astype(np.uint8)
    return cv2.add(img, noise)

def augment_flip(img, labels):
    """Horizontal flip with label adjustment"""
    flipped_img = cv2.flip(img, 1)
    
    # Flip bounding box x coordinates
    flipped_labels = []
    for line in labels:
        parts = line.strip().split()
        if parts:
            class_id = parts[0]
            x_center = 1.0 - float(parts[1])  # Flip x coordinate
            y_center = parts[2]
            width = parts[3]
            height = parts[4]
            flipped_labels.append(f"{class_id} {x_center} {y_center} {width} {height}\n")
    
    return flipped_img, flipped_labels

def augment_rotation(img, labels, angle_range=10):
    """Slight rotation"""
    angle = random.uniform(-angle_range, angle_range)
    h, w = img.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(img, M, (w, h), borderMode=cv2.BORDER_REFLECT)
    # Note: Not adjusting bounding boxes for simplicity (small rotations)
    return rotated, labels

# Augmentation pipeline
augmentations = [
    ('brightness', lambda img, lbl: (augment_brightness_contrast(img), lbl)),
    ('blur', lambda img, lbl: (augment_blur(img), lbl)),
    ('hsv', lambda img, lbl: (augment_hsv(img), lbl)),
    ('noise', lambda img, lbl: (augment_noise(img), lbl)),
    ('flip', augment_flip),
    ('rotation', augment_rotation),
    ('combined', lambda img, lbl: (augment_noise(augment_hsv(augment_brightness_contrast(img))), lbl)),
]

# Generate augmented samples
print("🔄 Generating augmented samples...")
print()

generated_count = 0
augmentation_stats = {name: 0 for name, _ in augmentations}

pbar = tqdm(total=INSTANCES_TO_ADD, desc="Augmenting")

while generated_count < INSTANCES_TO_ADD:
    # Randomly select an image
    img_path, label_path = random.choice(mobile_phone_images)
    
    # Read image
    img = cv2.imread(img_path)
    if img is None:
        continue
    
    # Read labels
    with open(label_path, 'r') as f:
        labels = f.readlines()
    
    # Randomly select augmentation
    aug_name, aug_func = random.choice(augmentations)
    
    # Apply augmentation
    aug_img, aug_labels = aug_func(img, labels)
    
    # Generate unique filename
    base_name = os.path.splitext(os.path.basename(img_path))[0]
    ext = os.path.splitext(img_path)[1]
    new_img_name = f"{base_name}_aug_{aug_name}_{generated_count}{ext}"
    new_label_name = f"{base_name}_aug_{aug_name}_{generated_count}.txt"
    
    new_img_path = os.path.join(TRAIN_IMAGES_DIR, new_img_name)
    new_label_path = os.path.join(TRAIN_LABELS_DIR, new_label_name)
    
    # Save augmented image
    cv2.imwrite(new_img_path, aug_img)
    
    # Save augmented labels
    with open(new_label_path, 'w') as f:
        f.writelines(aug_labels)
    
    generated_count += 1
    augmentation_stats[aug_name] += 1
    pbar.update(1)

pbar.close()

print()
print("=" * 80)
print("✅ AUGMENTATION COMPLETE")
print("=" * 80)
print(f"\nGenerated {generated_count} new samples")
print(f"New total mobile_phone instances: ~{CURRENT_INSTANCES + generated_count}")
print()
print("Augmentation breakdown:")
for aug_name, count in sorted(augmentation_stats.items(), key=lambda x: x[1], reverse=True):
    print(f"  {aug_name:12s}: {count:3d} samples")
print()
print("=" * 80)
print("🔍 NEXT STEPS")
print("=" * 80)
print("\n1. Verify new distribution:")
print("   python check_dataset_distribution.py")
print()
print("2. Start training:")
print("   python retrain_with_augmented_data.py")
print()
print("=" * 80)
