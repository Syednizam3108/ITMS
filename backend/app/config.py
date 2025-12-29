"""
Configuration file for traffic violation detection system
Handles all edge cases and detection thresholds
"""

# Detection Confidence Thresholds
MIN_CONFIDENCE_HELMET = 0.50        # Minimum confidence for helmet detection
MIN_CONFIDENCE_NO_HELMET = 0.50     # Minimum confidence for no-helmet violation
MIN_CONFIDENCE_MOBILE = 0.50        # Minimum confidence for mobile phone usage
MIN_CONFIDENCE_TRIPLE = 0.50        # Minimum confidence for triple riding
MIN_CONFIDENCE_LICENSE = 0.40       # License plates can be lower (harder to detect)
MIN_CONFIDENCE_MOTORCYCLE = 0.50    # Minimum confidence for motorcycle detection

# General Detection Settings
MIN_CONFIDENCE_GENERAL = 0.50       # Default minimum confidence for all detections
YOLO_IOU_THRESHOLD = 0.45          # IoU threshold for NMS (non-max suppression)

# Violation Registration Settings
COOLDOWN_SECONDS = 30              # Seconds to wait before registering same violation type again
MAX_VIOLATIONS_PER_FRAME = 5       # Maximum violations to register from single frame

# Edge Case Handling Rules
TRIPLE_RIDING_RULES = {
    "always_violation": True,       # Triple riding is ALWAYS a violation (overloading)
    "ignore_helmet_status": True    # Helmet status doesn't matter for triple riding
}

MOBILE_PHONE_RULES = {
    "always_violation": True,       # Mobile phone usage is ALWAYS a violation
    "ignore_helmet_status": True    # Helmet status doesn't matter for phone usage
}

NO_HELMET_RULES = {
    "require_motorcycle": False,    # No helmet is violation even without motorcycle in frame
    "min_detections": 1             # Minimum no_helmet detections to register violation
}

# Database Settings
DUPLICATE_CHECK_ENABLED = True      # Enable duplicate violation checking
DUPLICATE_CHECK_VEHICLE = True      # Check duplicates by vehicle number too
SAVE_LOW_CONFIDENCE = False         # Don't save detections below MIN_CONFIDENCE_GENERAL

# Fine Amounts (in currency units)
FINE_AMOUNTS = {
    "No Helmet Violation": 500.0,
    "Phone Usage While Riding": 1000.0,
    "Triple Riding Violation": 1500.0,
    "No Helmet": 500.0,
    "Mobile Usage": 1000.0,
    "Triple Riding": 1500.0,
}

# Image Storage Settings
IMAGE_QUALITY = 85                  # JPEG quality (0-100)
MAX_IMAGE_SIZE_MB = 10             # Maximum upload size in MB
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'webp'}

# Logging Settings
VERBOSE_LOGGING = True              # Enable detailed detection logs
LOG_SKIPPED_DETECTIONS = True       # Log violations that were skipped

# Model Settings
MODEL_PATH = "../runs/detect/train_20251204_225231/weights/best.pt"
FALLBACK_MODEL = "yolov8n.pt"      # Fallback if custom model not found

# Class IDs (from trained model)
CLASS_IDS = {
    "helmet": 0,
    "no_helmet": 1,
    "mobile_phone": 2,
    "triple_riding": 3,
    "license_plate": 4,
    "motorcycle": 5
}

# Violation Type Mappings
VIOLATION_TYPE_MAP = {
    "No Helmet": "No Helmet Violation",
    "Mobile Usage": "Phone Usage While Riding",
    "Triple Riding": "Triple Riding Violation"
}

REVERSE_VIOLATION_MAP = {
    "No Helmet Violation": "No Helmet",
    "Phone Usage While Riding": "Mobile Usage",
    "Triple Riding Violation": "Triple Riding"
}

# API Response Messages
ERROR_MESSAGES = {
    "no_violation": "❌ No traffic violations detected by AI in the uploaded image.",
    "type_mismatch": "❌ Violation type mismatch! Selected '{selected}' but AI detected: {detected}",
    "low_confidence": "⚠️ Detection confidence too low ({confidence:.0%}). Please upload a clearer image.",
    "upload_failed": "❌ Upload failed: {error}",
    "detection_failed": "❌ Detection processing failed: {error}",
    "duplicate": "⚠️ This violation was already registered recently.",
}

SUCCESS_MESSAGES = {
    "violation_saved": "✅ Violation confirmed by AI: {violation} detected with {confidence:.0%} confidence",
    "multiple_saved": "✅ {count} violations saved to database",
}

# Performance Optimization
ENABLE_GPU = True                   # Use GPU if available
BATCH_SIZE = 1                      # Batch size for detection (1 for real-time)
ASYNC_DETECTION = False             # Enable async detection (experimental)
