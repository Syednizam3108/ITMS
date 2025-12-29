# GPU Training Setup Guide

## Check if you have NVIDIA GPU

Run this in PowerShell:
```powershell
nvidia-smi
```

If you see GPU info, you have NVIDIA GPU. If error, you don't have compatible GPU.

## Step 1: Install CUDA Toolkit

1. Check your GPU compatibility: https://developer.nvidia.com/cuda-gpus
2. Download CUDA Toolkit 11.8: https://developer.nvidia.com/cuda-11-8-0-download-archive
3. Install CUDA Toolkit (follow installer)

## Step 2: Install PyTorch with CUDA Support

**Stop current training first** (Ctrl+C in terminal)

Then run:
```powershell
C:/Users/Lenovo/Desktop/Zain/Intelligent-Traffic-Management-System/ITMS/.venv/Scripts/pip.exe uninstall torch torchvision -y

C:/Users/Lenovo/Desktop/Zain/Intelligent-Traffic-Management-System/ITMS/.venv/Scripts/pip.exe install torch torchvision --index-url https://download.pytorch.org/whl/cu118
```

## Step 3: Verify GPU Setup

```powershell
C:/Users/Lenovo/Desktop/Zain/Intelligent-Traffic-Management-System/ITMS/.venv/Scripts/python.exe -c "import torch; print(f'CUDA Available: {torch.cuda.is_available()}'); print(f'GPU: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else None}')"
```

## Step 4: Start Training with GPU

```powershell
cd C:\Users\Lenovo\Desktop\Zain\Intelligent-Traffic-Management-System\ITMS
C:/Users/Lenovo/Desktop/Zain/Intelligent-Traffic-Management-System/ITMS/.venv/Scripts/python.exe train_model.py
```

You should see:
- ✅ CUDA available: True
- ✅ GPU Device: NVIDIA GeForce GTX/RTX...
- Training will be **10-30x faster**

## Speed Comparison

| Hardware | Time per Epoch | Total Time (50 epochs) |
|----------|----------------|------------------------|
| CPU      | ~30 minutes    | ~25 hours             |
| GPU      | ~1-2 minutes   | ~1-2 hours            |

## Troubleshooting

**"CUDA out of memory"**
- Reduce batch size in train_model.py: `batch=8` or `batch=4`

**"No GPU detected"**
- Your laptop might not have NVIDIA GPU
- Intel integrated graphics won't work for CUDA
- Check: Settings → System → Display → Advanced Display → Display Adapter Properties

**CUDA version mismatch**
- Make sure CUDA Toolkit version matches PyTorch version
- For PyTorch with cu118, use CUDA 11.8
