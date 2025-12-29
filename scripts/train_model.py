"""
Train YOLOv8 model on custom traffic violation dataset
"""
from ultralytics import YOLO
import os
import torch

if __name__ == '__main__':
    print(f"\n🔍 Checking GPU availability...")
    print(f"PyTorch version: {torch.__version__}")
    print(f"CUDA available: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"CUDA version: {torch.version.cuda}")
        print(f"GPU Device: {torch.cuda.get_device_name(0)}")
        print(f"GPU Memory: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.2f} GB")
        device = 'cuda'
    else:
        print("⚠️ No GPU detected. Training will use CPU (very slow)")
        print("To use GPU, install CUDA-enabled PyTorch:")
        print("  pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118")
        device = 'cpu'

    # Update paths in data.yaml to absolute Windows paths
    data_yaml_path = os.path.abspath("dataset/data.yaml")

    # Read and update data.yaml with correct paths
    with open(data_yaml_path, 'r') as f:
        content = f.read()

    # Get absolute paths
    base_path = os.path.abspath("dataset")
    train_path = os.path.join(base_path, "images", "train")
    val_path = os.path.join(base_path, "images", "val")

    # Update yaml content
    updated_content = f"""train: {train_path}
val: {val_path}

nc: 6
names:
  - helmet
  - no_helmet
  - mobile_phone
  - triple_riding
  - license_plate
  - motorcycle
"""

    with open(data_yaml_path, 'w') as f:
        f.write(updated_content)

    print("✅ Updated data.yaml with correct paths")
    print(f"Train path: {train_path}")
    print(f"Val path: {val_path}")

    # Initialize YOLOv8 model
    model = YOLO('yolov8n.pt')  # Start from pretrained weights

    print("\n🚀 Starting training...")
    print("This will take some time depending on your hardware (GPU recommended)")

    # Train the model
    results = model.train(
        data=data_yaml_path,
        epochs=50,              # Number of training epochs
        imgsz=640,              # Image size
        batch=16,               # Batch size (increase to 32 or 64 with GPU)
        name='traffic_violations',
        patience=5,            # Early stopping patience
        save=True,
        device=device,          # Use GPU if available, else CPU
        workers=0,              # Set to 0 for Windows to avoid multiprocessing issues
        cache=False,            # Set to True with GPU for faster training
        project='runs/detect',
        verbose=True
    )

    print("\n✅ Training complete!")
    print(f"Best model saved at: runs/detect/traffic_violations/weights/best.pt")
    print("\nTo use this model, update yolo_detector.py:")
    print("model_path='runs/detect/traffic_violations/weights/best.pt'")

