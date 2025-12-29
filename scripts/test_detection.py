"""
Test what the current YOLO model is actually detecting
"""
from ultralytics import YOLO
import os

# Load the trained model
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
model_path = os.path.join(project_root, 'runs', 'detect', 'train_20251204_225231', 'weights', 'best.pt')
model = YOLO(model_path)
print(f"\n✅ Loaded trained model from: {model_path}")

# Get class names
print("\n📋 Custom Trained Model Classes:")
print(f"Total classes: {len(model.names)}")
print("\nAll classes:")
for i in range(len(model.names)):
    print(f"  {i}: {model.names[i]}")

print("\n" + "="*50)
print("✅ MODEL INFORMATION:")
print("="*50)
print(f"Model path: {model_path}")
print(f"Classes detected: {list(model.names.values())}")

# Test the model on a sample image if available
test_image_dirs = [
    os.path.join(project_root, 'dataset', 'images', 'test'),
    os.path.join(project_root, 'dataset', 'images', 'val'),
    os.path.join(project_root, 'all_datasets_raw', 'no_helmet_roboflow', 'test', 'images')
]

test_image_path = None
for test_dir in test_image_dirs:
    if os.path.exists(test_dir):
        images = [f for f in os.listdir(test_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        if images:
            test_image_path = os.path.join(test_dir, images[0])
            break

if test_image_path:
    print(f"\n🔍 Testing on sample image: {test_image_path}")
    results = model(test_image_path)
    
    print("\n📊 Detection Results:")
    if len(results[0].boxes) > 0:
        for box in results[0].boxes:
            cls_id = int(box.cls[0])
            conf = float(box.conf[0])
            print(f"  - {model.names[cls_id]}: {conf:.2%} confidence")
    else:
        print("  No detections found in this image")
else:
    print("\n⚠️  No test images found. Add images to test the model.")

