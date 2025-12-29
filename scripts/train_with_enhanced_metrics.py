"""
Enhanced training script with comprehensive metrics tracking
Tracks additional metrics beyond default YOLOv8 output
"""
from ultralytics import YOLO
import yaml
import os
import json
import time
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Configuration
DATA_YAML = r"dataset\data.yaml"
BASE_MODEL = "yolov8n.pt"  # Start from scratch with pretrained COCO weights
EPOCHS = 50
BATCH_SIZE = 16
IMG_SIZE = 640
PATIENCE = 15
DEVICE = 0  # GPU

# Create run directory with timestamp
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
RUN_NAME = f"train_improved_{timestamp}"
OUTPUT_DIR = f"runs/detect/{RUN_NAME}"

if __name__ == '__main__':
    print("=" * 80)
    print("🚀 YOLOV8 TRAINING WITH ENHANCED METRICS")
    print("=" * 80)
    print(f"\nConfiguration:")
    print(f"  Base Model: {BASE_MODEL}")
    print(f"  Data: {DATA_YAML}")
    print(f"  Epochs: {EPOCHS}")
    print(f"  Batch Size: {BATCH_SIZE}")
    print(f"  Image Size: {IMG_SIZE}")
    print(f"  Patience: {PATIENCE}")
    print(f"  Device: GPU {DEVICE}")
    print(f"  Run Name: {RUN_NAME}")
    print()

    # Load model
    print("📦 Loading model...")
    model = YOLO(BASE_MODEL)
    print("✅ Model loaded\n")

    # Training configuration with additional metrics
    print("🎯 Starting training...")
    print("=" * 80)
    print()

    # Custom callback for additional metrics
    class MetricsTracker:
        def __init__(self):
            self.epoch_times = []
            self.learning_rates = []
            self.gpu_memory = []
            self.per_class_metrics = []
            self.start_time = time.time()
            self.epoch_start = None
            
        def on_train_epoch_start(self, trainer):
            """Called at start of each epoch"""
            self.epoch_start = time.time()
            
        def on_train_epoch_end(self, trainer):
            """Called at end of each epoch - collect additional metrics"""
            if self.epoch_start:
                epoch_time = time.time() - self.epoch_start
                self.epoch_times.append(epoch_time)
            
            # Get metrics from trainer
            metrics = trainer.metrics
            epoch = trainer.epoch
            
            # Collect per-class metrics if available
            if hasattr(trainer, 'validator') and trainer.validator:
                validator = trainer.validator
                if hasattr(validator, 'metrics'):
                    class_metrics = {
                        'epoch': epoch,
                        'timestamp': datetime.now().isoformat()
                    }
                    
                    # Try to get per-class AP
                    if hasattr(validator.metrics, 'ap_class_index'):
                        for i, class_idx in enumerate(validator.metrics.ap_class_index):
                            if hasattr(validator.metrics, 'ap'):
                                class_metrics[f'class_{class_idx}_AP50'] = float(validator.metrics.ap[i, 0])
                                class_metrics[f'class_{class_idx}_AP50-95'] = float(validator.metrics.ap[i, :].mean())
                    
                    self.per_class_metrics.append(class_metrics)
            
        def save_metrics(self, output_dir):
            """Save collected metrics to files"""
            metrics_dir = os.path.join(output_dir, 'enhanced_metrics')
            os.makedirs(metrics_dir, exist_ok=True)
            
            # Save epoch times
            if self.epoch_times:
                epoch_times_df = pd.DataFrame({
                    'epoch': range(1, len(self.epoch_times) + 1),
                    'time_seconds': self.epoch_times,
                    'time_minutes': [t/60 for t in self.epoch_times]
                })
                epoch_times_df.to_csv(os.path.join(metrics_dir, 'epoch_times.csv'), index=False)
                
                # Plot epoch times
                plt.figure(figsize=(10, 6))
                plt.plot(epoch_times_df['epoch'], epoch_times_df['time_minutes'], marker='o')
                plt.xlabel('Epoch')
                plt.ylabel('Time (minutes)')
                plt.title('Training Time per Epoch')
                plt.grid(True, alpha=0.3)
                plt.savefig(os.path.join(metrics_dir, 'epoch_times.png'), dpi=150, bbox_inches='tight')
                plt.close()
            
            # Save per-class metrics
            if self.per_class_metrics:
                per_class_df = pd.DataFrame(self.per_class_metrics)
                per_class_df.to_csv(os.path.join(metrics_dir, 'per_class_metrics.csv'), index=False)
            
            # Save summary
            total_time = time.time() - self.start_time
            summary = {
                'total_training_time_seconds': total_time,
                'total_training_time_hours': total_time / 3600,
                'average_epoch_time_seconds': sum(self.epoch_times) / len(self.epoch_times) if self.epoch_times else 0,
                'total_epochs': len(self.epoch_times),
                'timestamp': datetime.now().isoformat()
            }
            
            with open(os.path.join(metrics_dir, 'training_summary.json'), 'w') as f:
                json.dump(summary, f, indent=2)
            
            print(f"\n✅ Enhanced metrics saved to: {metrics_dir}")
    
    # Initialize tracker
    tracker = MetricsTracker()
    
    # Train with comprehensive tracking
    results = model.train(
    data=DATA_YAML,
    epochs=EPOCHS,
    batch=BATCH_SIZE,
    imgsz=IMG_SIZE,
    patience=PATIENCE,
    device=DEVICE,
    
    # Optimization settings
    optimizer='AdamW',
    lr0=0.001,
    lrf=0.01,
    momentum=0.937,
    weight_decay=0.0005,
    warmup_epochs=3,
    warmup_momentum=0.8,
    warmup_bias_lr=0.1,
    
    # Augmentation
    hsv_h=0.015,
    hsv_s=0.7,
    hsv_v=0.4,
    degrees=0.0,
    translate=0.1,
    scale=0.5,
    shear=0.0,
    perspective=0.0,
    flipud=0.0,
    fliplr=0.5,
    mosaic=1.0,
    mixup=0.1,
    copy_paste=0.1,
    
    # Saving and logging
    save=True,
    save_period=5,
    project='runs/detect',
    name=RUN_NAME,
    exist_ok=True,
    pretrained=True,
        verbose=True,
        
        # Additional metrics
        plots=True,
        val=True,
    )
    
    print()
    print("=" * 80)
    print("✅ TRAINING COMPLETE")
    print("=" * 80)

    # Save enhanced metrics
    tracker.save_metrics(OUTPUT_DIR)
    
    # Generate comprehensive metrics and visualizations
    print("\n📊 Generating comprehensive metrics and visualizations...")
    print("=" * 80)

    # Create metrics directory
    metrics_dir = os.path.join(OUTPUT_DIR, 'enhanced_metrics')
    os.makedirs(metrics_dir, exist_ok=True)
    
    # Validate model on validation set to get confusion matrix and per-class metrics
    print("\n🔍 Running validation to generate confusion matrix...")
    val_results = model.val(
    data=DATA_YAML,
    imgsz=IMG_SIZE,
    batch=BATCH_SIZE,
    conf=0.25,
    iou=0.6,
    plots=True,
        save_json=True,
        save_hybrid=True,
    )
    
    # Copy validation plots to enhanced metrics
    val_plots_dir = os.path.join(OUTPUT_DIR)
    if os.path.exists(val_plots_dir):
        import shutil
        for plot_file in ['confusion_matrix.png', 'confusion_matrix_normalized.png', 
                         'F1_curve.png', 'P_curve.png', 'R_curve.png', 'PR_curve.png']:
            src = os.path.join(val_plots_dir, plot_file)
            if os.path.exists(src):
                shutil.copy2(src, os.path.join(metrics_dir, plot_file))
                print(f"✅ Copied {plot_file}")
    
    print("\n📊 Creating additional visualizations...")
    
    # Load and analyze results
    print("\n📊 Analyzing results...")
        results_csv = os.path.join(OUTPUT_DIR, 'results.csv')
    
    if os.path.exists(results_csv):
    df = pd.read_csv(results_csv)
    df.columns = df.columns.str.strip()  # Clean column names
    
    # Create enhanced visualizations
    metrics_dir = os.path.join(OUTPUT_DIR, 'enhanced_metrics')
    
    # 1. Loss curves (all losses together)
    plt.figure(figsize=(14, 8))
    
    loss_cols = [col for col in df.columns if 'loss' in col.lower()]
    for col in loss_cols:
        if col in df.columns:
            plt.plot(df.index, df[col], label=col, linewidth=2)
    
    plt.xlabel('Epoch', fontsize=12)
    plt.ylabel('Loss', fontsize=12)
    plt.title('All Loss Curves', fontsize=14, fontweight='bold')
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.savefig(os.path.join(metrics_dir, 'all_losses.png'), dpi=150, bbox_inches='tight')
    plt.close()
    
    # 2. Performance metrics
    plt.figure(figsize=(14, 8))
    
    perf_cols = ['metrics/precision(B)', 'metrics/recall(B)', 'metrics/mAP50(B)', 'metrics/mAP50-95(B)']
    colors = ['blue', 'green', 'red', 'orange']
    
    for col, color in zip(perf_cols, colors):
        if col in df.columns:
            clean_name = col.replace('metrics/', '').replace('(B)', '')
            plt.plot(df.index, df[col], label=clean_name, color=color, linewidth=2, marker='o', markersize=4)
    
    plt.xlabel('Epoch', fontsize=12)
    plt.ylabel('Score', fontsize=12)
    plt.title('Performance Metrics Over Time', fontsize=14, fontweight='bold')
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.ylim(0, 1)
    plt.savefig(os.path.join(metrics_dir, 'performance_metrics.png'), dpi=150, bbox_inches='tight')
    plt.close()
    
    # 3. Learning rate schedule
    if 'lr/pg0' in df.columns:
        plt.figure(figsize=(12, 6))
        plt.plot(df.index, df['lr/pg0'], color='purple', linewidth=2)
        plt.xlabel('Epoch', fontsize=12)
        plt.ylabel('Learning Rate', fontsize=12)
        plt.title('Learning Rate Schedule', fontsize=14, fontweight='bold')
        plt.grid(True, alpha=0.3)
        plt.yscale('log')
        plt.savefig(os.path.join(metrics_dir, 'learning_rate.png'), dpi=150, bbox_inches='tight')
        plt.close()
    
    # 4. Final metrics summary
    final_metrics = {
        'Final Epoch': len(df),
        'Best mAP50': df['metrics/mAP50(B)'].max() if 'metrics/mAP50(B)' in df.columns else 'N/A',
        'Best mAP50-95': df['metrics/mAP50-95(B)'].max() if 'metrics/mAP50-95(B)' in df.columns else 'N/A',
        'Final Precision': df['metrics/precision(B)'].iloc[-1] if 'metrics/precision(B)' in df.columns else 'N/A',
        'Final Recall': df['metrics/recall(B)'].iloc[-1] if 'metrics/recall(B)' in df.columns else 'N/A',
        'Final Box Loss': df['train/box_loss'].iloc[-1] if 'train/box_loss' in df.columns else 'N/A',
        'Final Class Loss': df['train/cls_loss'].iloc[-1] if 'train/cls_loss' in df.columns else 'N/A',
    }
    
    # Save metrics summary
    with open(os.path.join(metrics_dir, 'final_metrics.json'), 'w') as f:
        json.dump(final_metrics, f, indent=2)
    
    # 5. Precision-Recall curve per class
    if 'metrics/precision(B)' in df.columns and 'metrics/recall(B)' in df.columns:
        plt.figure(figsize=(12, 8))
        plt.scatter(df['metrics/recall(B)'], df['metrics/precision(B)'], 
                   c=df.index, cmap='viridis', s=50, alpha=0.6)
        plt.colorbar(label='Epoch')
        plt.xlabel('Recall', fontsize=12)
        plt.ylabel('Precision', fontsize=12)
        plt.title('Precision-Recall Evolution', fontsize=14, fontweight='bold')
        plt.grid(True, alpha=0.3)
        plt.xlim(0, 1)
        plt.ylim(0, 1)
        plt.savefig(os.path.join(metrics_dir, 'precision_recall_evolution.png'), dpi=150, bbox_inches='tight')
        plt.close()
    
    # 6. F1 Score calculation and plot
    if 'metrics/precision(B)' in df.columns and 'metrics/recall(B)' in df.columns:
        df['F1_Score'] = 2 * (df['metrics/precision(B)'] * df['metrics/recall(B)']) / \
                         (df['metrics/precision(B)'] + df['metrics/recall(B)'] + 1e-6)
        
        plt.figure(figsize=(12, 6))
        plt.plot(df.index, df['F1_Score'], color='purple', linewidth=2, marker='o', markersize=4)
        plt.xlabel('Epoch', fontsize=12)
        plt.ylabel('F1 Score', fontsize=12)
        plt.title('F1 Score Over Time', fontsize=14, fontweight='bold')
        plt.grid(True, alpha=0.3)
        plt.ylim(0, 1)
        plt.savefig(os.path.join(metrics_dir, 'f1_score.png'), dpi=150, bbox_inches='tight')
        plt.close()
        
        final_metrics['Best F1 Score'] = df['F1_Score'].max()
        final_metrics['Final F1 Score'] = df['F1_Score'].iloc[-1]
    
    # 7. Training vs Validation Loss comparison
    train_loss_cols = [col for col in df.columns if col.startswith('train/') and 'loss' in col]
    val_loss_cols = [col for col in df.columns if col.startswith('val/') and 'loss' in col]
    
    if train_loss_cols and val_loss_cols:
        fig, axes = plt.subplots(1, 3, figsize=(18, 5))
        loss_types = ['box_loss', 'cls_loss', 'dfl_loss']
        
        for i, loss_type in enumerate(loss_types):
            train_col = f'train/{loss_type}'
            val_col = f'val/{loss_type}'
            
            if train_col in df.columns and val_col in df.columns:
                axes[i].plot(df.index, df[train_col], label='Train', linewidth=2)
                axes[i].plot(df.index, df[val_col], label='Validation', linewidth=2)
                axes[i].set_xlabel('Epoch', fontsize=11)
                axes[i].set_ylabel('Loss', fontsize=11)
                axes[i].set_title(f'{loss_type.replace("_", " ").title()}', fontsize=12, fontweight='bold')
                axes[i].legend()
                axes[i].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(os.path.join(metrics_dir, 'train_val_loss_comparison.png'), dpi=150, bbox_inches='tight')
        plt.close()
    
    # 8. Overfitting detection chart
    if 'train/box_loss' in df.columns and 'val/box_loss' in df.columns:
        df['loss_gap'] = df['val/box_loss'] - df['train/box_loss']
        
        plt.figure(figsize=(12, 6))
        plt.plot(df.index, df['loss_gap'], color='red', linewidth=2)
        plt.axhline(y=0, color='black', linestyle='--', alpha=0.5)
        plt.xlabel('Epoch', fontsize=12)
        plt.ylabel('Validation Loss - Training Loss', fontsize=12)
        plt.title('Overfitting Detection (Positive = Overfitting)', fontsize=14, fontweight='bold')
        plt.grid(True, alpha=0.3)
        plt.savefig(os.path.join(metrics_dir, 'overfitting_detection.png'), dpi=150, bbox_inches='tight')
        plt.close()
    
    # 9. Comprehensive metrics dashboard
    fig = plt.figure(figsize=(20, 12))
    gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)
    
    # Loss curves
    ax1 = fig.add_subplot(gs[0, :])
    for col in loss_cols[:6]:  # Limit to 6 losses for clarity
        if col in df.columns:
            ax1.plot(df.index, df[col], label=col.replace('train/', 'T_').replace('val/', 'V_'), linewidth=1.5)
    ax1.set_xlabel('Epoch')
    ax1.set_ylabel('Loss')
    ax1.set_title('All Loss Curves', fontweight='bold')
    ax1.legend(ncol=3, fontsize=9)
    ax1.grid(True, alpha=0.3)
    
    # mAP curves
    ax2 = fig.add_subplot(gs[1, 0])
    if 'metrics/mAP50(B)' in df.columns:
        ax2.plot(df.index, df['metrics/mAP50(B)'], color='red', linewidth=2)
        ax2.set_xlabel('Epoch')
        ax2.set_ylabel('mAP@50')
        ax2.set_title('mAP@50', fontweight='bold')
        ax2.grid(True, alpha=0.3)
        ax2.set_ylim(0, 1)
    
    # mAP50-95
    ax3 = fig.add_subplot(gs[1, 1])
    if 'metrics/mAP50-95(B)' in df.columns:
        ax3.plot(df.index, df['metrics/mAP50-95(B)'], color='orange', linewidth=2)
        ax3.set_xlabel('Epoch')
        ax3.set_ylabel('mAP@50-95')
        ax3.set_title('mAP@50-95', fontweight='bold')
        ax3.grid(True, alpha=0.3)
        ax3.set_ylim(0, 1)
    
    # Precision & Recall
    ax4 = fig.add_subplot(gs[1, 2])
    if 'metrics/precision(B)' in df.columns and 'metrics/recall(B)' in df.columns:
        ax4.plot(df.index, df['metrics/precision(B)'], label='Precision', linewidth=2)
        ax4.plot(df.index, df['metrics/recall(B)'], label='Recall', linewidth=2)
        ax4.set_xlabel('Epoch')
        ax4.set_ylabel('Score')
        ax4.set_title('Precision & Recall', fontweight='bold')
        ax4.legend()
        ax4.grid(True, alpha=0.3)
        ax4.set_ylim(0, 1)
    
    # F1 Score
    ax5 = fig.add_subplot(gs[2, 0])
    if 'F1_Score' in df.columns:
        ax5.plot(df.index, df['F1_Score'], color='purple', linewidth=2)
        ax5.set_xlabel('Epoch')
        ax5.set_ylabel('F1 Score')
        ax5.set_title('F1 Score', fontweight='bold')
        ax5.grid(True, alpha=0.3)
        ax5.set_ylim(0, 1)
    
    # Learning Rate
    ax6 = fig.add_subplot(gs[2, 1])
    if 'lr/pg0' in df.columns:
        ax6.plot(df.index, df['lr/pg0'], color='green', linewidth=2)
        ax6.set_xlabel('Epoch')
        ax6.set_ylabel('Learning Rate')
        ax6.set_title('Learning Rate Schedule', fontweight='bold')
        ax6.grid(True, alpha=0.3)
        ax6.set_yscale('log')
    
    # Loss Gap (Overfitting)
    ax7 = fig.add_subplot(gs[2, 2])
    if 'loss_gap' in df.columns:
        ax7.plot(df.index, df['loss_gap'], color='red', linewidth=2)
        ax7.axhline(y=0, color='black', linestyle='--', alpha=0.5)
        ax7.set_xlabel('Epoch')
        ax7.set_ylabel('Val Loss - Train Loss')
        ax7.set_title('Overfitting Indicator', fontweight='bold')
        ax7.grid(True, alpha=0.3)
    
    plt.suptitle('Comprehensive Training Metrics Dashboard', fontsize=16, fontweight='bold', y=0.995)
    plt.savefig(os.path.join(metrics_dir, 'comprehensive_dashboard.png'), dpi=150, bbox_inches='tight')
    plt.close()
    
    # Update final metrics with new calculations
    with open(os.path.join(metrics_dir, 'final_metrics.json'), 'w') as f:
        json.dump(final_metrics, f, indent=2)
    
    print("\n📈 Final Metrics:")
    print("=" * 80)
    for key, value in final_metrics.items():
        if isinstance(value, float):
            print(f"{key:20s}: {value:.4f}")
        else:
            print(f"{key:20s}: {value}")
    print("=" * 80)

print(f"\n📁 All results saved to: {OUTPUT_DIR}")
print(f"📁 Enhanced metrics in: {os.path.join(OUTPUT_DIR, 'enhanced_metrics')}")
print(f"🏆 Best model: {os.path.join(OUTPUT_DIR, 'weights', 'best.pt')}")
print(f"💾 Last model: {os.path.join(OUTPUT_DIR, 'weights', 'last.pt')}")

print("\n" + "=" * 80)
print("📊 GENERATED VISUALIZATIONS")
print("=" * 80)
print("\n✅ Confusion Matrix (normalized & absolute)")
print("✅ Precision-Recall Curve")
print("✅ F1 Curve")
print("✅ P Curve, R Curve")
print("✅ All Loss Curves")
print("✅ Performance Metrics Over Time")
print("✅ Learning Rate Schedule")
print("✅ Epoch Times Analysis")
print("✅ Precision-Recall Evolution")
print("✅ F1 Score Progression")
print("✅ Train vs Validation Loss Comparison")
print("✅ Overfitting Detection Chart")
print("✅ Comprehensive Metrics Dashboard")

print("\n" + "=" * 80)
print("🎯 NEXT STEPS")
print("=" * 80)
print("\n1. Review all metrics in:")
print(f"   {os.path.join(OUTPUT_DIR, 'enhanced_metrics')}")
print("\n2. Test on validation set:")
print(f"   yolo val model={os.path.join(OUTPUT_DIR, 'weights', 'best.pt')} data={DATA_YAML}")
print("\n3. Test inference on images:")
print("   yolo predict model=... source=test_image.jpg")
print("\n4. Deploy the model for real-time detection")
print("=" * 80)
