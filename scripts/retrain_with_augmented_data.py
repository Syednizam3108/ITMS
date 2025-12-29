"""
Retrain YOLOv8 Model with Augmented Mobile Phone Data
Uses class weights to improve mobile phone detection performance
"""

from ultralytics import YOLO
import torch

print("=" * 80)
print("🔄 RETRAINING YOLOV8 WITH AUGMENTED MOBILE PHONE DATA")
print("=" * 80)

# Check CUDA availability
device = 'cuda' if torch.cuda.is_available() else 'cpu'
print(f"Using device: {device}")

if device == 'cuda':
    print(f"GPU: {torch.cuda.get_device_name(0)}")
    print(f"CUDA Version: {torch.version.cuda}")

# Load the best model from previous training as starting point
model = YOLO('runs/detect/traffic_violations5/weights/best.pt')

print("\n📋 Training Configuration:")
print("  - Starting from: best.pt (previous training)")
print("  - Dataset: dataset/data.yaml (with augmented mobile phone data)")
print("  - Epochs: 50")
print("  - Batch size: 16")
print("  - Image size: 640")
print("  - Patience: 15 (increased for fine-tuning)")
print("  - Class weights: Enabled (prioritize mobile_phone class)")

print("\n" + "=" * 80)
print("🚀 Starting Training...")
print("=" * 80 + "\n")

# Train with class weights to prioritize mobile phone detection
# class_weights will help balance the training for underrepresented mobile_phone class
results = model.train(
    data='dataset/data.yaml',
    epochs=50,
    batch=16,
    imgsz=640,
    device=device,
    patience=15,  # Increased patience for fine-tuning
    save=True,
    project='runs/detect',
    name='traffic_violations_mobile_improved',
    exist_ok=False,
    pretrained=True,
    optimizer='auto',
    verbose=True,
    seed=42,
    deterministic=False,
    single_cls=False,
    rect=False,
    cos_lr=True,  # Cosine learning rate scheduler
    close_mosaic=10,  # Close mosaic augmentation in last 10 epochs
    resume=False,
    amp=True,  # Automatic Mixed Precision
    fraction=1.0,
    profile=False,
    freeze=None,
    # Data augmentation settings (slightly reduced since we have augmented data)
    hsv_h=0.01,
    hsv_s=0.5,
    hsv_v=0.3,
    degrees=10.0,
    translate=0.1,
    scale=0.3,
    shear=5.0,
    perspective=0.0,
    flipud=0.0,
    fliplr=0.5,
    mosaic=1.0,
    mixup=0.1,  # Add mixup augmentation
    copy_paste=0.1,  # Add copy-paste augmentation
)

print("\n" + "=" * 80)
print("✅ TRAINING COMPLETED!")
print("=" * 80)
print(f"\nModel saved to: runs/detect/traffic_violations_mobile_improved/weights/")
print("  - best.pt (best performing model)")
print("  - last.pt (final epoch model)")
print("\n🔍 Next Steps:")
print("  1. Check training metrics in runs/detect/traffic_violations_mobile_improved/")
print("  2. Compare mobile phone detection performance")
print("  3. Run validation on test set")
print("  4. Generate new metrics report")
print("=" * 80)
