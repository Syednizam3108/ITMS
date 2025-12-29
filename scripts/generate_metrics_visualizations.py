"""
Comprehensive Training Metrics Analysis and Visualization Generator
Generates all possible metrics, graphs, and analysis for YOLOv8 training results
"""

import os
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import csv
from datetime import datetime
import shutil

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 10

# Paths
RESULTS_DIR = Path("runs/detect/traffic_violations5")
OUTPUT_DIR = Path("training_metrics_analysis")
OUTPUT_DIR.mkdir(exist_ok=True)

# Create subdirectories
CHARTS_DIR = OUTPUT_DIR / "charts"
DATA_DIR = OUTPUT_DIR / "data"
REPORTS_DIR = OUTPUT_DIR / "reports"

for dir_path in [CHARTS_DIR, DATA_DIR, REPORTS_DIR]:
    dir_path.mkdir(exist_ok=True)

print("🔍 Starting Comprehensive Metrics Analysis...")
print(f"📁 Output Directory: {OUTPUT_DIR}")
print("=" * 80)

# ============================================================================
# 1. LOAD TRAINING RESULTS
# ============================================================================

def load_results_csv():
    """Load training results from CSV"""
    results_file = RESULTS_DIR / "results.csv"
    if not results_file.exists():
        print(f"❌ Results file not found: {results_file}")
        return None
    
    df = pd.read_csv(results_file)
    df.columns = df.columns.str.strip()
    print(f"✅ Loaded training data: {len(df)} epochs")
    return df

# ============================================================================
# 2. GENERATE SUMMARY STATISTICS
# ============================================================================

def generate_summary_statistics(df):
    """Generate comprehensive summary statistics"""
    print("\n📊 Generating Summary Statistics...")
    
    # Overall statistics
    stats = {
        'Training Summary': {
            'Total Epochs': len(df),
            'Best Epoch': df['metrics/mAP50(B)'].idxmax() + 1,
            'Training Duration (hours)': 3.274,  # From your output
            'Early Stopping': 'Yes (patience=10)',
            'Final Epoch': 45
        },
        'Best Validation Metrics': {
            'Precision': df['metrics/precision(B)'].max(),
            'Recall': df['metrics/recall(B)'].max(),
            'mAP@50': df['metrics/mAP50(B)'].max(),
            'mAP@50-95': df['metrics/mAP50-95(B)'].max()
        },
        'Final Epoch Metrics': {
            'Precision': df['metrics/precision(B)'].iloc[-1],
            'Recall': df['metrics/recall(B)'].iloc[-1],
            'mAP@50': df['metrics/mAP50(B)'].iloc[-1],
            'mAP@50-95': df['metrics/mAP50-95(B)'].iloc[-1]
        },
        'Training Loss (Final)': {
            'Box Loss': df['train/box_loss'].iloc[-1],
            'Class Loss': df['train/cls_loss'].iloc[-1],
            'DFL Loss': df['train/dfl_loss'].iloc[-1]
        },
        'Validation Loss (Final)': {
            'Box Loss': df['val/box_loss'].iloc[-1],
            'Class Loss': df['val/cls_loss'].iloc[-1],
            'DFL Loss': df['val/dfl_loss'].iloc[-1]
        },
        'Performance Improvements': {
            'Precision Gain': f"{(df['metrics/precision(B)'].iloc[-1] - df['metrics/precision(B)'].iloc[0]) * 100:.2f}%",
            'Recall Gain': f"{(df['metrics/recall(B)'].iloc[-1] - df['metrics/recall(B)'].iloc[0]) * 100:.2f}%",
            'mAP@50 Gain': f"{(df['metrics/mAP50(B)'].iloc[-1] - df['metrics/mAP50(B)'].iloc[0]) * 100:.2f}%",
            'mAP@50-95 Gain': f"{(df['metrics/mAP50-95(B)'].iloc[-1] - df['metrics/mAP50-95(B)'].iloc[0]) * 100:.2f}%"
        }
    }
    
    # Save to JSON
    with open(DATA_DIR / 'summary_statistics.json', 'w') as f:
        json.dump(stats, f, indent=2)
    
    # Save to text report
    with open(REPORTS_DIR / 'summary_report.txt', 'w') as f:
        f.write("=" * 80 + "\n")
        f.write("YOLOV8 TRAINING SUMMARY REPORT\n")
        f.write("=" * 80 + "\n\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        for section, data in stats.items():
            f.write(f"\n{section}\n")
            f.write("-" * 80 + "\n")
            for key, value in data.items():
                f.write(f"{key:.<40} {value}\n")
    
    print(f"✅ Summary statistics saved to {DATA_DIR / 'summary_statistics.json'}")
    return stats

# ============================================================================
# 3. EPOCH-BY-EPOCH DETAILED METRICS
# ============================================================================

def save_epoch_details(df):
    """Save detailed epoch-by-epoch metrics"""
    print("\n📋 Saving Epoch Details...")
    
    # Save full CSV with renamed columns for clarity
    detailed_df = df.copy()
    detailed_df.index.name = 'Epoch'
    detailed_df.to_csv(DATA_DIR / 'epoch_by_epoch_metrics.csv')
    
    # Save best epochs analysis
    best_epochs = {
        'Best mAP@50 Epoch': int(df['metrics/mAP50(B)'].idxmax() + 1),
        'Best mAP@50-95 Epoch': int(df['metrics/mAP50-95(B)'].idxmax() + 1),
        'Best Precision Epoch': int(df['metrics/precision(B)'].idxmax() + 1),
        'Best Recall Epoch': int(df['metrics/recall(B)'].idxmax() + 1),
        'Lowest Box Loss Epoch': int(df['train/box_loss'].idxmin() + 1),
        'Lowest Class Loss Epoch': int(df['train/cls_loss'].idxmin() + 1)
    }
    
    with open(DATA_DIR / 'best_epochs.json', 'w') as f:
        json.dump(best_epochs, f, indent=2)
    
    print(f"✅ Detailed metrics saved to {DATA_DIR / 'epoch_by_epoch_metrics.csv'}")

# ============================================================================
# 4. VISUALIZATION FUNCTIONS
# ============================================================================

def plot_training_validation_losses(df):
    """Plot all training and validation losses"""
    print("\n📈 Generating Loss Plots...")
    
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Training and Validation Losses Over Epochs', fontsize=16, fontweight='bold')
    
    # Box Loss
    axes[0, 0].plot(df.index + 1, df['train/box_loss'], label='Training', linewidth=2, color='#2E86AB')
    axes[0, 0].plot(df.index + 1, df['val/box_loss'], label='Validation', linewidth=2, color='#A23B72')
    axes[0, 0].set_title('Box Loss', fontweight='bold', fontsize=12)
    axes[0, 0].set_xlabel('Epoch')
    axes[0, 0].set_ylabel('Loss')
    axes[0, 0].legend()
    axes[0, 0].grid(True, alpha=0.3)
    
    # Class Loss
    axes[0, 1].plot(df.index + 1, df['train/cls_loss'], label='Training', linewidth=2, color='#2E86AB')
    axes[0, 1].plot(df.index + 1, df['val/cls_loss'], label='Validation', linewidth=2, color='#A23B72')
    axes[0, 1].set_title('Classification Loss', fontweight='bold', fontsize=12)
    axes[0, 1].set_xlabel('Epoch')
    axes[0, 1].set_ylabel('Loss')
    axes[0, 1].legend()
    axes[0, 1].grid(True, alpha=0.3)
    
    # DFL Loss
    axes[1, 0].plot(df.index + 1, df['train/dfl_loss'], label='Training', linewidth=2, color='#2E86AB')
    axes[1, 0].plot(df.index + 1, df['val/dfl_loss'], label='Validation', linewidth=2, color='#A23B72')
    axes[1, 0].set_title('Distribution Focal Loss (DFL)', fontweight='bold', fontsize=12)
    axes[1, 0].set_xlabel('Epoch')
    axes[1, 0].set_ylabel('Loss')
    axes[1, 0].legend()
    axes[1, 0].grid(True, alpha=0.3)
    
    # Combined Losses
    axes[1, 1].plot(df.index + 1, df['train/box_loss'] + df['train/cls_loss'] + df['train/dfl_loss'], 
                    label='Training Total', linewidth=2, color='#2E86AB')
    axes[1, 1].plot(df.index + 1, df['val/box_loss'] + df['val/cls_loss'] + df['val/dfl_loss'], 
                    label='Validation Total', linewidth=2, color='#A23B72')
    axes[1, 1].set_title('Total Combined Loss', fontweight='bold', fontsize=12)
    axes[1, 1].set_xlabel('Epoch')
    axes[1, 1].set_ylabel('Loss')
    axes[1, 1].legend()
    axes[1, 1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(CHARTS_DIR / 'losses_over_epochs.png', dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✅ Loss plots saved")

def plot_performance_metrics(df):
    """Plot precision, recall, and mAP metrics"""
    print("\n📈 Generating Performance Metrics Plots...")
    
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Model Performance Metrics Over Epochs', fontsize=16, fontweight='bold')
    
    # Precision
    axes[0, 0].plot(df.index + 1, df['metrics/precision(B)'], linewidth=2.5, color='#06A77D', marker='o', markersize=3)
    axes[0, 0].set_title('Precision', fontweight='bold', fontsize=12)
    axes[0, 0].set_xlabel('Epoch')
    axes[0, 0].set_ylabel('Precision')
    axes[0, 0].grid(True, alpha=0.3)
    axes[0, 0].axhline(y=df['metrics/precision(B)'].max(), color='r', linestyle='--', alpha=0.5, label='Best')
    axes[0, 0].legend()
    
    # Recall
    axes[0, 1].plot(df.index + 1, df['metrics/recall(B)'], linewidth=2.5, color='#F18F01', marker='s', markersize=3)
    axes[0, 1].set_title('Recall', fontweight='bold', fontsize=12)
    axes[0, 1].set_xlabel('Epoch')
    axes[0, 1].set_ylabel('Recall')
    axes[0, 1].grid(True, alpha=0.3)
    axes[0, 1].axhline(y=df['metrics/recall(B)'].max(), color='r', linestyle='--', alpha=0.5, label='Best')
    axes[0, 1].legend()
    
    # mAP@50
    axes[1, 0].plot(df.index + 1, df['metrics/mAP50(B)'], linewidth=2.5, color='#C73E1D', marker='^', markersize=3)
    axes[1, 0].set_title('mAP@50', fontweight='bold', fontsize=12)
    axes[1, 0].set_xlabel('Epoch')
    axes[1, 0].set_ylabel('mAP@50')
    axes[1, 0].grid(True, alpha=0.3)
    axes[1, 0].axhline(y=df['metrics/mAP50(B)'].max(), color='r', linestyle='--', alpha=0.5, label='Best')
    axes[1, 0].legend()
    
    # mAP@50-95
    axes[1, 1].plot(df.index + 1, df['metrics/mAP50-95(B)'], linewidth=2.5, color='#6A4C93', marker='D', markersize=3)
    axes[1, 1].set_title('mAP@50-95', fontweight='bold', fontsize=12)
    axes[1, 1].set_xlabel('Epoch')
    axes[1, 1].set_ylabel('mAP@50-95')
    axes[1, 1].grid(True, alpha=0.3)
    axes[1, 1].axhline(y=df['metrics/mAP50-95(B)'].max(), color='r', linestyle='--', alpha=0.5, label='Best')
    axes[1, 1].legend()
    
    plt.tight_layout()
    plt.savefig(CHARTS_DIR / 'performance_metrics.png', dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✅ Performance metrics plots saved")

def plot_combined_metrics(df):
    """Plot all key metrics in one chart"""
    print("\n📈 Generating Combined Metrics Plot...")
    
    plt.figure(figsize=(16, 10))
    
    plt.subplot(2, 1, 1)
    plt.plot(df.index + 1, df['metrics/precision(B)'], label='Precision', linewidth=2, marker='o', markersize=4)
    plt.plot(df.index + 1, df['metrics/recall(B)'], label='Recall', linewidth=2, marker='s', markersize=4)
    plt.plot(df.index + 1, df['metrics/mAP50(B)'], label='mAP@50', linewidth=2, marker='^', markersize=4)
    plt.plot(df.index + 1, df['metrics/mAP50-95(B)'], label='mAP@50-95', linewidth=2, marker='D', markersize=4)
    plt.title('All Performance Metrics Over Training', fontweight='bold', fontsize=14)
    plt.xlabel('Epoch')
    plt.ylabel('Metric Value')
    plt.legend(loc='best')
    plt.grid(True, alpha=0.3)
    
    plt.subplot(2, 1, 2)
    plt.plot(df.index + 1, df['train/box_loss'], label='Train Box Loss', linewidth=2, alpha=0.7)
    plt.plot(df.index + 1, df['train/cls_loss'], label='Train Class Loss', linewidth=2, alpha=0.7)
    plt.plot(df.index + 1, df['train/dfl_loss'], label='Train DFL Loss', linewidth=2, alpha=0.7)
    plt.plot(df.index + 1, df['val/box_loss'], label='Val Box Loss', linewidth=2, linestyle='--', alpha=0.7)
    plt.plot(df.index + 1, df['val/cls_loss'], label='Val Class Loss', linewidth=2, linestyle='--', alpha=0.7)
    plt.plot(df.index + 1, df['val/dfl_loss'], label='Val DFL Loss', linewidth=2, linestyle='--', alpha=0.7)
    plt.title('All Loss Metrics Over Training', fontweight='bold', fontsize=14)
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend(loc='best', ncol=2)
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(CHARTS_DIR / 'all_metrics_combined.png', dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✅ Combined metrics plot saved")

def plot_learning_rate(df):
    """Plot learning rate schedule"""
    print("\n📈 Generating Learning Rate Plot...")
    
    if 'lr/pg0' in df.columns:
        plt.figure(figsize=(12, 6))
        plt.plot(df.index + 1, df['lr/pg0'], linewidth=2, color='#E63946')
        if 'lr/pg1' in df.columns:
            plt.plot(df.index + 1, df['lr/pg1'], linewidth=2, color='#457B9D', alpha=0.7)
        if 'lr/pg2' in df.columns:
            plt.plot(df.index + 1, df['lr/pg2'], linewidth=2, color='#1D3557', alpha=0.7)
        
        plt.title('Learning Rate Schedule', fontweight='bold', fontsize=14)
        plt.xlabel('Epoch')
        plt.ylabel('Learning Rate')
        plt.grid(True, alpha=0.3)
        plt.legend(['Parameter Group 0', 'Parameter Group 1', 'Parameter Group 2'])
        plt.tight_layout()
        plt.savefig(CHARTS_DIR / 'learning_rate_schedule.png', dpi=300, bbox_inches='tight')
        plt.close()
        print(f"✅ Learning rate plot saved")

def plot_precision_recall_curve(df):
    """Plot precision-recall relationship"""
    print("\n📈 Generating Precision-Recall Analysis...")
    
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    
    # Precision vs Recall scatter
    axes[0].scatter(df['metrics/recall(B)'], df['metrics/precision(B)'], 
                    c=df.index, cmap='viridis', s=100, alpha=0.6, edgecolors='black')
    axes[0].set_xlabel('Recall', fontweight='bold')
    axes[0].set_ylabel('Precision', fontweight='bold')
    axes[0].set_title('Precision vs Recall (Color = Epoch)', fontweight='bold', fontsize=12)
    axes[0].grid(True, alpha=0.3)
    cbar = plt.colorbar(axes[0].collections[0], ax=axes[0])
    cbar.set_label('Epoch', fontweight='bold')
    
    # F1 Score calculation and plot
    f1_scores = 2 * (df['metrics/precision(B)'] * df['metrics/recall(B)']) / \
                (df['metrics/precision(B)'] + df['metrics/recall(B)'])
    
    axes[1].plot(df.index + 1, f1_scores, linewidth=2.5, color='#06A77D', marker='o', markersize=4)
    axes[1].set_xlabel('Epoch', fontweight='bold')
    axes[1].set_ylabel('F1 Score', fontweight='bold')
    axes[1].set_title('F1 Score Over Epochs', fontweight='bold', fontsize=12)
    axes[1].grid(True, alpha=0.3)
    axes[1].axhline(y=f1_scores.max(), color='r', linestyle='--', alpha=0.5, label=f'Max: {f1_scores.max():.3f}')
    axes[1].legend()
    
    plt.tight_layout()
    plt.savefig(CHARTS_DIR / 'precision_recall_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # Save F1 scores
    f1_df = pd.DataFrame({
        'Epoch': df.index + 1,
        'F1_Score': f1_scores,
        'Precision': df['metrics/precision(B)'],
        'Recall': df['metrics/recall(B)']
    })
    f1_df.to_csv(DATA_DIR / 'f1_scores.csv', index=False)
    
    print(f"✅ Precision-Recall analysis saved")

def plot_loss_comparison(df):
    """Compare training vs validation losses"""
    print("\n📈 Generating Loss Comparison Plot...")
    
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    
    losses = [('box_loss', 'Box Loss'), ('cls_loss', 'Class Loss'), ('dfl_loss', 'DFL Loss')]
    
    for idx, (loss_name, title) in enumerate(losses):
        train_col = f'train/{loss_name}'
        val_col = f'val/{loss_name}'
        
        axes[idx].plot(df.index + 1, df[train_col], label='Training', linewidth=2.5, color='#2E86AB')
        axes[idx].plot(df.index + 1, df[val_col], label='Validation', linewidth=2.5, color='#A23B72')
        axes[idx].fill_between(df.index + 1, df[train_col], df[val_col], alpha=0.2)
        axes[idx].set_title(title, fontweight='bold', fontsize=12)
        axes[idx].set_xlabel('Epoch')
        axes[idx].set_ylabel('Loss')
        axes[idx].legend()
        axes[idx].grid(True, alpha=0.3)
    
    plt.suptitle('Training vs Validation Loss Comparison', fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.savefig(CHARTS_DIR / 'train_val_loss_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✅ Loss comparison plot saved")

def plot_metric_improvements(df):
    """Plot improvement rates of metrics"""
    print("\n📈 Generating Metric Improvement Analysis...")
    
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    
    metrics = {
        'Precision': 'metrics/precision(B)',
        'Recall': 'metrics/recall(B)',
        'mAP@50': 'metrics/mAP50(B)',
        'mAP@50-95': 'metrics/mAP50-95(B)'
    }
    
    positions = [(0, 0), (0, 1), (1, 0), (1, 1)]
    
    for (name, col), (i, j) in zip(metrics.items(), positions):
        # Calculate rolling average
        rolling_avg = df[col].rolling(window=5, min_periods=1).mean()
        
        axes[i, j].plot(df.index + 1, df[col], label='Actual', linewidth=2, alpha=0.6, color='#457B9D')
        axes[i, j].plot(df.index + 1, rolling_avg, label='5-Epoch Moving Avg', 
                        linewidth=2.5, color='#E63946')
        axes[i, j].set_title(f'{name} - Trend Analysis', fontweight='bold', fontsize=12)
        axes[i, j].set_xlabel('Epoch')
        axes[i, j].set_ylabel(name)
        axes[i, j].legend()
        axes[i, j].grid(True, alpha=0.3)
        
        # Mark best epoch
        best_epoch = df[col].idxmax()
        axes[i, j].axvline(x=best_epoch + 1, color='green', linestyle='--', alpha=0.5)
        axes[i, j].annotate(f'Best: Epoch {best_epoch + 1}', 
                            xy=(best_epoch + 1, df[col].iloc[best_epoch]),
                            xytext=(10, 10), textcoords='offset points',
                            bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5),
                            arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))
    
    plt.suptitle('Metric Improvement Trends with Moving Averages', fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.savefig(CHARTS_DIR / 'metric_improvement_trends.png', dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✅ Metric improvement analysis saved")

def plot_overfitting_analysis(df):
    """Analyze overfitting through train/val gap"""
    print("\n📈 Generating Overfitting Analysis...")
    
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    
    # Calculate gaps
    box_gap = df['train/box_loss'] - df['val/box_loss']
    cls_gap = df['train/cls_loss'] - df['val/cls_loss']
    dfl_gap = df['train/dfl_loss'] - df['val/dfl_loss']
    
    axes[0].plot(df.index + 1, box_gap, linewidth=2, color='#E63946')
    axes[0].axhline(y=0, color='black', linestyle='--', alpha=0.5)
    axes[0].fill_between(df.index + 1, 0, box_gap, where=(box_gap > 0), alpha=0.3, color='red', label='Overfitting')
    axes[0].fill_between(df.index + 1, 0, box_gap, where=(box_gap < 0), alpha=0.3, color='green', label='Underfitting')
    axes[0].set_title('Box Loss Gap (Train - Val)', fontweight='bold')
    axes[0].set_xlabel('Epoch')
    axes[0].set_ylabel('Loss Difference')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)
    
    axes[1].plot(df.index + 1, cls_gap, linewidth=2, color='#F18F01')
    axes[1].axhline(y=0, color='black', linestyle='--', alpha=0.5)
    axes[1].fill_between(df.index + 1, 0, cls_gap, where=(cls_gap > 0), alpha=0.3, color='red')
    axes[1].fill_between(df.index + 1, 0, cls_gap, where=(cls_gap < 0), alpha=0.3, color='green')
    axes[1].set_title('Class Loss Gap (Train - Val)', fontweight='bold')
    axes[1].set_xlabel('Epoch')
    axes[1].set_ylabel('Loss Difference')
    axes[1].grid(True, alpha=0.3)
    
    axes[2].plot(df.index + 1, dfl_gap, linewidth=2, color='#06A77D')
    axes[2].axhline(y=0, color='black', linestyle='--', alpha=0.5)
    axes[2].fill_between(df.index + 1, 0, dfl_gap, where=(dfl_gap > 0), alpha=0.3, color='red')
    axes[2].fill_between(df.index + 1, 0, dfl_gap, where=(dfl_gap < 0), alpha=0.3, color='green')
    axes[2].set_title('DFL Loss Gap (Train - Val)', fontweight='bold')
    axes[2].set_xlabel('Epoch')
    axes[2].set_ylabel('Loss Difference')
    axes[2].grid(True, alpha=0.3)
    
    plt.suptitle('Overfitting/Underfitting Analysis', fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.savefig(CHARTS_DIR / 'overfitting_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # Save gap data
    gap_df = pd.DataFrame({
        'Epoch': df.index + 1,
        'Box_Loss_Gap': box_gap,
        'Class_Loss_Gap': cls_gap,
        'DFL_Loss_Gap': dfl_gap
    })
    gap_df.to_csv(DATA_DIR / 'train_val_gaps.csv', index=False)
    
    print(f"✅ Overfitting analysis saved")

def plot_correlation_heatmap(df):
    """Plot correlation heatmap of all metrics"""
    print("\n📈 Generating Correlation Heatmap...")
    
    # Select numeric columns
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    correlation_matrix = df[numeric_cols].corr()
    
    plt.figure(figsize=(14, 12))
    sns.heatmap(correlation_matrix, annot=True, fmt='.2f', cmap='coolwarm', 
                center=0, square=True, linewidths=1, cbar_kws={"shrink": 0.8})
    plt.title('Correlation Matrix of All Training Metrics', fontweight='bold', fontsize=14, pad=20)
    plt.tight_layout()
    plt.savefig(CHARTS_DIR / 'correlation_heatmap.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # Save correlation matrix
    correlation_matrix.to_csv(DATA_DIR / 'correlation_matrix.csv')
    
    print(f"✅ Correlation heatmap saved")

def plot_box_plots(df):
    """Create box plots for metric distributions"""
    print("\n📈 Generating Box Plot Distributions...")
    
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    
    metrics = {
        'Precision': 'metrics/precision(B)',
        'Recall': 'metrics/recall(B)',
        'mAP@50': 'metrics/mAP50(B)',
        'mAP@50-95': 'metrics/mAP50-95(B)',
        'Box Loss': 'train/box_loss',
        'Class Loss': 'train/cls_loss'
    }
    
    positions = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2)]
    
    for (name, col), (i, j) in zip(metrics.items(), positions):
        box = axes[i, j].boxplot([df[col]], labels=[name], patch_artist=True)
        box['boxes'][0].set_facecolor('#457B9D')
        box['boxes'][0].set_alpha(0.7)
        axes[i, j].set_title(f'{name} Distribution', fontweight='bold')
        axes[i, j].grid(True, alpha=0.3, axis='y')
        
        # Add statistics
        stats_text = f'Mean: {df[col].mean():.4f}\nStd: {df[col].std():.4f}\nMin: {df[col].min():.4f}\nMax: {df[col].max():.4f}'
        axes[i, j].text(0.98, 0.98, stats_text, transform=axes[i, j].transAxes,
                        verticalalignment='top', horizontalalignment='right',
                        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5),
                        fontsize=9)
    
    plt.suptitle('Metric Distribution Analysis (Box Plots)', fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.savefig(CHARTS_DIR / 'metric_distributions.png', dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✅ Box plot distributions saved")

def generate_performance_dashboard(df):
    """Create a comprehensive dashboard"""
    print("\n📈 Generating Performance Dashboard...")
    
    fig = plt.figure(figsize=(20, 12))
    gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)
    
    # Top row - Main metrics
    ax1 = fig.add_subplot(gs[0, :2])
    ax1.plot(df.index + 1, df['metrics/mAP50(B)'], label='mAP@50', linewidth=3, color='#E63946')
    ax1.plot(df.index + 1, df['metrics/mAP50-95(B)'], label='mAP@50-95', linewidth=3, color='#457B9D')
    ax1.set_title('Primary Performance Metrics', fontweight='bold', fontsize=14)
    ax1.set_xlabel('Epoch')
    ax1.set_ylabel('mAP')
    ax1.legend(fontsize=12)
    ax1.grid(True, alpha=0.3)
    
    # Best epoch marker
    ax2 = fig.add_subplot(gs[0, 2])
    best_epoch = df['metrics/mAP50(B)'].idxmax() + 1
    best_metrics = df.iloc[df['metrics/mAP50(B)'].idxmax()]
    ax2.text(0.5, 0.9, 'Best Epoch', ha='center', va='top', fontsize=14, fontweight='bold', transform=ax2.transAxes)
    ax2.text(0.5, 0.75, f'{best_epoch}', ha='center', va='top', fontsize=40, fontweight='bold', 
             color='#E63946', transform=ax2.transAxes)
    ax2.text(0.1, 0.5, f'mAP@50: {best_metrics["metrics/mAP50(B)"]:.3f}\n'
                       f'mAP@50-95: {best_metrics["metrics/mAP50-95(B)"]:.3f}\n'
                       f'Precision: {best_metrics["metrics/precision(B)"]:.3f}\n'
                       f'Recall: {best_metrics["metrics/recall(B)"]:.3f}',
             ha='left', va='center', fontsize=11, transform=ax2.transAxes,
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    ax2.axis('off')
    
    # Middle row - Losses
    ax3 = fig.add_subplot(gs[1, 0])
    ax3.plot(df.index + 1, df['train/box_loss'], label='Train', linewidth=2)
    ax3.plot(df.index + 1, df['val/box_loss'], label='Val', linewidth=2)
    ax3.set_title('Box Loss', fontweight='bold')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    
    ax4 = fig.add_subplot(gs[1, 1])
    ax4.plot(df.index + 1, df['train/cls_loss'], label='Train', linewidth=2)
    ax4.plot(df.index + 1, df['val/cls_loss'], label='Val', linewidth=2)
    ax4.set_title('Class Loss', fontweight='bold')
    ax4.legend()
    ax4.grid(True, alpha=0.3)
    
    ax5 = fig.add_subplot(gs[1, 2])
    ax5.plot(df.index + 1, df['train/dfl_loss'], label='Train', linewidth=2)
    ax5.plot(df.index + 1, df['val/dfl_loss'], label='Val', linewidth=2)
    ax5.set_title('DFL Loss', fontweight='bold')
    ax5.legend()
    ax5.grid(True, alpha=0.3)
    
    # Bottom row - Precision/Recall
    ax6 = fig.add_subplot(gs[2, :2])
    ax6.plot(df.index + 1, df['metrics/precision(B)'], label='Precision', linewidth=2.5, marker='o', markersize=4)
    ax6.plot(df.index + 1, df['metrics/recall(B)'], label='Recall', linewidth=2.5, marker='s', markersize=4)
    f1 = 2 * (df['metrics/precision(B)'] * df['metrics/recall(B)']) / (df['metrics/precision(B)'] + df['metrics/recall(B)'])
    ax6.plot(df.index + 1, f1, label='F1 Score', linewidth=2.5, marker='^', markersize=4)
    ax6.set_title('Precision, Recall, F1 Score', fontweight='bold', fontsize=14)
    ax6.set_xlabel('Epoch')
    ax6.set_ylabel('Score')
    ax6.legend(fontsize=11)
    ax6.grid(True, alpha=0.3)
    
    # Final metrics
    ax7 = fig.add_subplot(gs[2, 2])
    final_metrics = df.iloc[-1]
    ax7.text(0.5, 0.9, 'Final Epoch', ha='center', va='top', fontsize=14, fontweight='bold', transform=ax7.transAxes)
    ax7.text(0.5, 0.75, f'{len(df)}', ha='center', va='top', fontsize=40, fontweight='bold', 
             color='#457B9D', transform=ax7.transAxes)
    ax7.text(0.1, 0.5, f'mAP@50: {final_metrics["metrics/mAP50(B)"]:.3f}\n'
                       f'mAP@50-95: {final_metrics["metrics/mAP50-95(B)"]:.3f}\n'
                       f'Precision: {final_metrics["metrics/precision(B)"]:.3f}\n'
                       f'Recall: {final_metrics["metrics/recall(B)"]:.3f}',
             ha='left', va='center', fontsize=11, transform=ax7.transAxes,
             bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.5))
    ax7.axis('off')
    
    plt.suptitle('YOLOv8 Training Performance Dashboard', fontsize=18, fontweight='bold', y=0.98)
    plt.savefig(CHARTS_DIR / 'performance_dashboard.png', dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✅ Performance dashboard saved")

# ============================================================================
# 5. PER-CLASS METRICS
# ============================================================================

def generate_class_metrics():
    """Generate per-class performance metrics"""
    print("\n📊 Generating Per-Class Metrics...")
    
    class_metrics = {
        'helmet': {
            'Precision': 0.856,
            'Recall': 0.676,
            'mAP@50': 0.791,
            'mAP@50-95': 0.373,
            'Instances': 185
        },
        'mobile_phone': {
            'Precision': 0.327,
            'Recall': 0.182,
            'mAP@50': 0.331,
            'mAP@50-95': 0.110,
            'Instances': 11
        },
        'license_plate': {
            'Precision': 0.933,
            'Recall': 0.894,
            'mAP@50': 0.942,
            'mAP@50-95': 0.664,
            'Instances': 204
        },
        'motorcycle': {
            'Precision': 0.656,
            'Recall': 0.926,
            'mAP@50': 0.925,
            'mAP@50-95': 0.832,
            'Instances': 27
        }
    }
    
    # Save to JSON
    with open(DATA_DIR / 'class_metrics.json', 'w') as f:
        json.dump(class_metrics, f, indent=2)
    
    # Create DataFrame
    class_df = pd.DataFrame(class_metrics).T
    class_df.to_csv(DATA_DIR / 'class_metrics.csv')
    
    # Plot per-class metrics
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    classes = list(class_metrics.keys())
    
    # Precision
    precisions = [class_metrics[c]['Precision'] for c in classes]
    axes[0, 0].bar(classes, precisions, color=['#06A77D', '#E63946', '#457B9D', '#F18F01'])
    axes[0, 0].set_title('Precision by Class', fontweight='bold', fontsize=12)
    axes[0, 0].set_ylabel('Precision')
    axes[0, 0].set_ylim(0, 1)
    axes[0, 0].grid(True, alpha=0.3, axis='y')
    for i, v in enumerate(precisions):
        axes[0, 0].text(i, v + 0.02, f'{v:.3f}', ha='center', fontweight='bold')
    
    # Recall
    recalls = [class_metrics[c]['Recall'] for c in classes]
    axes[0, 1].bar(classes, recalls, color=['#06A77D', '#E63946', '#457B9D', '#F18F01'])
    axes[0, 1].set_title('Recall by Class', fontweight='bold', fontsize=12)
    axes[0, 1].set_ylabel('Recall')
    axes[0, 1].set_ylim(0, 1)
    axes[0, 1].grid(True, alpha=0.3, axis='y')
    for i, v in enumerate(recalls):
        axes[0, 1].text(i, v + 0.02, f'{v:.3f}', ha='center', fontweight='bold')
    
    # mAP@50
    map50s = [class_metrics[c]['mAP@50'] for c in classes]
    axes[1, 0].bar(classes, map50s, color=['#06A77D', '#E63946', '#457B9D', '#F18F01'])
    axes[1, 0].set_title('mAP@50 by Class', fontweight='bold', fontsize=12)
    axes[1, 0].set_ylabel('mAP@50')
    axes[1, 0].set_ylim(0, 1)
    axes[1, 0].grid(True, alpha=0.3, axis='y')
    for i, v in enumerate(map50s):
        axes[1, 0].text(i, v + 0.02, f'{v:.3f}', ha='center', fontweight='bold')
    
    # mAP@50-95
    map50_95s = [class_metrics[c]['mAP@50-95'] for c in classes]
    axes[1, 1].bar(classes, map50_95s, color=['#06A77D', '#E63946', '#457B9D', '#F18F01'])
    axes[1, 1].set_title('mAP@50-95 by Class', fontweight='bold', fontsize=12)
    axes[1, 1].set_ylabel('mAP@50-95')
    axes[1, 1].set_ylim(0, 1)
    axes[1, 1].grid(True, alpha=0.3, axis='y')
    for i, v in enumerate(map50_95s):
        axes[1, 1].text(i, v + 0.02, f'{v:.3f}', ha='center', fontweight='bold')
    
    plt.suptitle('Per-Class Performance Metrics (Best Model)', fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.savefig(CHARTS_DIR / 'class_performance_metrics.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # Create grouped bar chart
    fig, ax = plt.subplots(figsize=(14, 8))
    x = np.arange(len(classes))
    width = 0.2
    
    ax.bar(x - 1.5*width, precisions, width, label='Precision', color='#06A77D')
    ax.bar(x - 0.5*width, recalls, width, label='Recall', color='#F18F01')
    ax.bar(x + 0.5*width, map50s, width, label='mAP@50', color='#457B9D')
    ax.bar(x + 1.5*width, map50_95s, width, label='mAP@50-95', color='#E63946')
    
    ax.set_xlabel('Class', fontweight='bold', fontsize=12)
    ax.set_ylabel('Score', fontweight='bold', fontsize=12)
    ax.set_title('Comprehensive Per-Class Metrics Comparison', fontweight='bold', fontsize=14)
    ax.set_xticks(x)
    ax.set_xticklabels(classes, fontweight='bold')
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3, axis='y')
    ax.set_ylim(0, 1.1)
    
    plt.tight_layout()
    plt.savefig(CHARTS_DIR / 'class_metrics_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"✅ Per-class metrics saved")

# ============================================================================
# 6. COMPREHENSIVE TEXT REPORT
# ============================================================================

def generate_comprehensive_report(df, stats):
    """Generate detailed text report"""
    print("\n📝 Generating Comprehensive Report...")
    
    with open(REPORTS_DIR / 'training_analysis_report.txt', 'w', encoding='utf-8') as f:
        f.write("=" * 100 + "\n")
        f.write(" " * 30 + "YOLOV8 TRAINING COMPREHENSIVE ANALYSIS REPORT\n")
        f.write("=" * 100 + "\n\n")
        f.write(f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Model: YOLOv8n (Nano)\n")
        f.write(f"Task: Traffic Violations Detection\n")
        f.write(f"Classes: helmet, mobile_phone, license_plate, motorcycle\n\n")
        
        f.write("-" * 100 + "\n")
        f.write("1. TRAINING OVERVIEW\n")
        f.write("-" * 100 + "\n")
        f.write(f"Total Epochs Completed: {len(df)}\n")
        f.write(f"Planned Epochs: 50\n")
        f.write(f"Early Stopping: Triggered at epoch {len(df)} (patience: 10 epochs)\n")
        f.write(f"Best Model Epoch: {df['metrics/mAP50(B)'].idxmax() + 1}\n")
        f.write(f"Training Duration: 3.274 hours\n")
        f.write(f"Average Time per Epoch: {(3.274 * 60) / len(df):.2f} minutes\n\n")
        
        f.write("-" * 100 + "\n")
        f.write("2. BEST MODEL PERFORMANCE (Epoch {})".format(df['metrics/mAP50(B)'].idxmax() + 1) + "\n")
        f.write("-" * 100 + "\n")
        best_idx = df['metrics/mAP50(B)'].idxmax()
        best = df.iloc[best_idx]
        f.write(f"Precision:        {best['metrics/precision(B)']:.4f}\n")
        f.write(f"Recall:           {best['metrics/recall(B)']:.4f}\n")
        f.write(f"mAP@50:           {best['metrics/mAP50(B)']:.4f}\n")
        f.write(f"mAP@50-95:        {best['metrics/mAP50-95(B)']:.4f}\n")
        f.write(f"F1 Score:         {2 * (best['metrics/precision(B)'] * best['metrics/recall(B)']) / (best['metrics/precision(B)'] + best['metrics/recall(B)']):.4f}\n\n")
        
        f.write("-" * 100 + "\n")
        f.write("3. FINAL EPOCH PERFORMANCE (Epoch {})\n".format(len(df)))
        f.write("-" * 100 + "\n")
        final = df.iloc[-1]
        f.write(f"Precision:        {final['metrics/precision(B)']:.4f}\n")
        f.write(f"Recall:           {final['metrics/recall(B)']:.4f}\n")
        f.write(f"mAP@50:           {final['metrics/mAP50(B)']:.4f}\n")
        f.write(f"mAP@50-95:        {final['metrics/mAP50-95(B)']:.4f}\n")
        f.write(f"F1 Score:         {2 * (final['metrics/precision(B)'] * final['metrics/recall(B)']) / (final['metrics/precision(B)'] + final['metrics/recall(B)']):.4f}\n\n")
        
        f.write("-" * 100 + "\n")
        f.write("4. LOSS ANALYSIS\n")
        f.write("-" * 100 + "\n")
        f.write("Final Training Losses:\n")
        f.write(f"  Box Loss:       {final['train/box_loss']:.4f}\n")
        f.write(f"  Class Loss:     {final['train/cls_loss']:.4f}\n")
        f.write(f"  DFL Loss:       {final['train/dfl_loss']:.4f}\n\n")
        f.write("Final Validation Losses:\n")
        f.write(f"  Box Loss:       {final['val/box_loss']:.4f}\n")
        f.write(f"  Class Loss:     {final['val/cls_loss']:.4f}\n")
        f.write(f"  DFL Loss:       {final['val/dfl_loss']:.4f}\n\n")
        f.write("Loss Improvements (First -> Last):\n")
        f.write(f"  Box Loss:       {((df['train/box_loss'].iloc[0] - final['train/box_loss']) / df['train/box_loss'].iloc[0] * 100):.2f}%\n")
        f.write(f"  Class Loss:     {((df['train/cls_loss'].iloc[0] - final['train/cls_loss']) / df['train/cls_loss'].iloc[0] * 100):.2f}%\n")
        f.write(f"  DFL Loss:       {((df['train/dfl_loss'].iloc[0] - final['train/dfl_loss']) / df['train/dfl_loss'].iloc[0] * 100):.2f}%\n\n")
        
        f.write("-" * 100 + "\n")
        f.write("5. PER-CLASS PERFORMANCE (Best Model)\n")
        f.write("-" * 100 + "\n")
        f.write(f"{'Class':<20} {'Precision':>12} {'Recall':>12} {'mAP@50':>12} {'mAP@50-95':>12} {'Instances':>12}\n")
        f.write("-" * 100 + "\n")
        f.write(f"{'helmet':<20} {0.856:>12.3f} {0.676:>12.3f} {0.791:>12.3f} {0.373:>12.3f} {185:>12}\n")
        f.write(f"{'mobile_phone':<20} {0.327:>12.3f} {0.182:>12.3f} {0.331:>12.3f} {0.110:>12.3f} {11:>12}\n")
        f.write(f"{'license_plate':<20} {0.933:>12.3f} {0.894:>12.3f} {0.942:>12.3f} {0.664:>12.3f} {204:>12}\n")
        f.write(f"{'motorcycle':<20} {0.656:>12.3f} {0.926:>12.3f} {0.925:>12.3f} {0.832:>12.3f} {27:>12}\n")
        f.write("-" * 100 + "\n\n")
        
        f.write("-" * 100 + "\n")
        f.write("6. TRAINING STABILITY ANALYSIS\n")
        f.write("-" * 100 + "\n")
        f.write(f"Precision - Mean: {df['metrics/precision(B)'].mean():.4f}, Std: {df['metrics/precision(B)'].std():.4f}\n")
        f.write(f"Recall    - Mean: {df['metrics/recall(B)'].mean():.4f}, Std: {df['metrics/recall(B)'].std():.4f}\n")
        f.write(f"mAP@50    - Mean: {df['metrics/mAP50(B)'].mean():.4f}, Std: {df['metrics/mAP50(B)'].std():.4f}\n")
        f.write(f"mAP@50-95 - Mean: {df['metrics/mAP50-95(B)'].mean():.4f}, Std: {df['metrics/mAP50-95(B)'].std():.4f}\n\n")
        
        f.write("-" * 100 + "\n")
        f.write("7. KEY FINDINGS AND RECOMMENDATIONS\n")
        f.write("-" * 100 + "\n")
        f.write("✅ Strengths:\n")
        f.write("   • License plate detection is excellent (mAP@50: 0.942)\n")
        f.write("   • Motorcycle detection has very high recall (0.926)\n")
        f.write("   • Helmet detection shows good precision (0.856)\n")
        f.write("   • Training converged smoothly with early stopping\n\n")
        f.write("⚠️  Areas for Improvement:\n")
        f.write("   • Mobile phone detection needs more training data (only 11 instances)\n")
        f.write("   • Consider data augmentation for mobile_phone class\n")
        f.write("   • Helmet recall could be improved (0.676)\n\n")
        f.write("📌 Recommendations:\n")
        f.write("   1. Collect more mobile phone usage samples (target: 100+ instances)\n")
        f.write("   2. Apply class-weighted training to balance performance\n")
        f.write("   3. Consider test-time augmentation for improved inference\n")
        f.write("   4. Fine-tune on domain-specific traffic footage\n\n")
        
        f.write("=" * 100 + "\n")
        f.write("END OF REPORT\n")
        f.write("=" * 100 + "\n")
    
    print(f"✅ Comprehensive report saved to {REPORTS_DIR / 'training_analysis_report.txt'}")

# ============================================================================
# 7. COPY EXISTING VISUALIZATIONS
# ============================================================================

def copy_existing_visualizations():
    """Copy existing confusion matrix and other plots"""
    print("\n📁 Copying Existing Visualizations...")
    
    existing_files = [
        'confusion_matrix.png',
        'confusion_matrix_normalized.png',
        'F1_curve.png',
        'P_curve.png',
        'R_curve.png',
        'PR_curve.png',
        'results.png',
        'labels.jpg',
        'labels_correlogram.jpg',
        'train_batch0.jpg',
        'train_batch1.jpg',
        'train_batch2.jpg',
        'val_batch0_labels.jpg',
        'val_batch0_pred.jpg',
        'val_batch1_labels.jpg',
        'val_batch1_pred.jpg',
        'val_batch2_labels.jpg',
        'val_batch2_pred.jpg'
    ]
    
    for filename in existing_files:
        src = RESULTS_DIR / filename
        if src.exists():
            dst = CHARTS_DIR / filename
            shutil.copy2(src, dst)
            print(f"  ✅ Copied {filename}")
    
    print(f"✅ Existing visualizations copied")

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main execution function"""
    
    # Load data
    df = load_results_csv()
    if df is None:
        print("❌ Cannot proceed without results data")
        return
    
    # Generate all metrics and visualizations
    stats = generate_summary_statistics(df)
    save_epoch_details(df)
    
    # Generate all plots
    plot_training_validation_losses(df)
    plot_performance_metrics(df)
    plot_combined_metrics(df)
    plot_learning_rate(df)
    plot_precision_recall_curve(df)
    plot_loss_comparison(df)
    plot_metric_improvements(df)
    plot_overfitting_analysis(df)
    plot_correlation_heatmap(df)
    plot_box_plots(df)
    generate_performance_dashboard(df)
    
    # Generate class metrics
    generate_class_metrics()
    
    # Generate comprehensive report
    generate_comprehensive_report(df, stats)
    
    # Copy existing visualizations
    copy_existing_visualizations()
    
    print("\n" + "=" * 80)
    print("✅ ALL METRICS AND VISUALIZATIONS GENERATED SUCCESSFULLY!")
    print("=" * 80)
    print(f"\n📁 Output Directory: {OUTPUT_DIR.absolute()}")
    print(f"\n📊 Charts:  {CHARTS_DIR.absolute()}")
    print(f"📈 Data:    {DATA_DIR.absolute()}")
    print(f"📝 Reports: {REPORTS_DIR.absolute()}")
    print("\n" + "=" * 80)

if __name__ == "__main__":
    main()
