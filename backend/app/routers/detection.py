from fastapi import APIRouter, WebSocket, WebSocketDisconnect, UploadFile, File
from ..yolo_detector import get_detector
from ..database import violations_collection
from ..email_service import get_email_service
from datetime import datetime, timedelta
import json
import base64
import os

router = APIRouter(prefix="/detection", tags=["Detection"])

UPLOAD_DIR = "app/static/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Deduplication: Track recent violations to avoid duplicates
COOLDOWN_SECONDS = 30  # Don't register same violation type within 30 seconds
MIN_CONFIDENCE = 0.50  # Minimum confidence threshold for saving violations

async def is_duplicate_violation(violation_type: str, vehicle_number: str = None, cooldown_seconds: int = COOLDOWN_SECONDS) -> bool:
    """Check if the same violation was registered recently - IMPROVED with vehicle tracking"""
    cutoff_time = datetime.now() - timedelta(seconds=cooldown_seconds)
    
    query = {
        "violation_type": violation_type,
        "timestamp": {"$gte": cutoff_time}
    }
    
    # EDGE CASE: If vehicle number provided, check same vehicle + same violation
    if vehicle_number and not vehicle_number.startswith("VEH_"):
        query["vehicle_number"] = vehicle_number
    
    recent_violation = await violations_collection.find_one(query)
    
    return recent_violation is not None

@router.post("/detect-snapshot")
async def detect_snapshot(frame_data: dict):
    """Detect violations from snapshot and save to database - COMPREHENSIVE EDGE CASE HANDLING"""
    try:
        detector = get_detector()
        
        # Process frame WITHOUT annotation for speed (return_annotated=False)
        result = detector.process_frame(frame_data.get("frame"), return_annotated=False)
        
        # EDGE CASE 1: Detection failed or no results
        if not result.get("success"):
            return {
                "success": False,
                "error": result.get("error", "Detection failed"),
                "violations": [],
                "violation_count": 0,
                "saved_to_db": 0
            }
        
        # Extract vehicle number from license plates or generate unique ID
        license_plates = result.get("license_plates", [])
        vehicle_number = None
        
        if license_plates and len(license_plates) > 0:
            # Use highest confidence plate
            best_plate = max(license_plates, key=lambda p: p.get('confidence', 0))
            # Use actual plate detection info for vehicle number
            vehicle_number = f"LP_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            print(f"📋 License plate detected with {best_plate['confidence']:.0%} confidence")
        else:
            # Fallback: Generate unique vehicle ID from timestamp
            vehicle_number = f"VEH_{datetime.now().strftime('%Y%m%d%H%M%S%f')}"
        
        saved_count = 0
        skipped_count = 0
        
        # EDGE CASE 2: No violations detected
        violations = result.get("violations", [])
        if not violations or len(violations) == 0:
            return {
                "success": True,
                "violations": [],
                "violation_count": 0,
                "timestamp": datetime.now().isoformat(),
                "saved_to_db": 0,
                "message": "No violations detected in frame"
            }
        
        # Process each detected violation
        for violation in violations:
            violation_type = violation.get("type")
            confidence = violation.get("confidence", 0.0)
            
            print(f"🔍 Processing violation: {violation_type} @ {confidence:.0%} confidence")
            
            # EDGE CASE 3: Low confidence detection - skip if below threshold
            if confidence < MIN_CONFIDENCE:
                print(f"⚠️ Skipping {violation_type}: confidence {confidence:.0%} below threshold {MIN_CONFIDENCE:.0%}")
                skipped_count += 1
                continue
            
            print(f"✅ {violation_type} passed confidence threshold")
            
            # EDGE CASE 4: Duplicate detection - check recent violations
            if await is_duplicate_violation(violation_type, vehicle_number):
                print(f"⚠️ Skipping {violation_type}: duplicate within {COOLDOWN_SECONDS}s cooldown")
                skipped_count += 1
                continue
            
            # Save violation image
            try:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
                filename = f"violation_{timestamp}_{violation['class']}.jpg"
                filepath = os.path.join(UPLOAD_DIR, filename)
                
                # Decode and save original image (not annotated for performance)
                frame_str = frame_data.get("frame")
                if frame_str:
                    img_data = frame_str.split('base64,')[1] if 'base64,' in frame_str else frame_str
                    img_bytes = base64.b64decode(img_data)
                    with open(filepath, 'wb') as f:
                        f.write(img_bytes)
                else:
                    print(f"⚠️ No frame data to save for {violation_type}")
                    filepath = None
                
            except Exception as img_err:
                print(f"⚠️ Failed to save image for {violation_type}: {img_err}")
                filepath = None
            
            # Create violation record in MongoDB
            try:
                violation_record = {
                    "vehicle_number": vehicle_number,
                    "violation_type": violation_type,
                    "location": "Live Camera Feed",
                    "officer_id": None,
                    "fine_amount": get_fine_amount(violation_type),
                    "status": "pending",
                    "image_path": f"/static/uploads/{filename}" if filepath else None,
                    "timestamp": datetime.now(),
                    "confidence": round(confidence, 2),
                    "detection_class": violation.get("class"),
                    "bbox": violation.get("bbox", [])
                }
                
                result = await violations_collection.insert_one(violation_record)
                violation_id = str(result.inserted_id)
                saved_count += 1
                print(f"✅ Saved {violation_type} violation: {confidence:.0%} confidence")
                
                # Send email notification with penalty slip
                try:
                    email_service = get_email_service()
                    full_image_path = filepath if filepath else None
                    await email_service.send_violation_email(
                        vehicle_number=vehicle_number,
                        violation_type=violation_type,
                        fine_amount=get_fine_amount(violation_type),
                        location="Live Camera Feed",
                        timestamp=datetime.now(),
                        violation_id=violation_id,
                        image_path=full_image_path,
                        confidence=confidence
                    )
                except Exception as email_err:
                    print(f"⚠️ Failed to send email notification: {email_err}")
                
            except Exception as db_err:
                print(f"❌ Failed to save {violation_type} to database: {db_err}")
        
        # Return comprehensive response
        return {
            "success": True,
            "violations": violations,
            "violation_count": len(violations),
            "timestamp": datetime.now().isoformat(),
            "saved_to_db": saved_count,
            "skipped": skipped_count,
            "license_plates": len(license_plates),
            "stats": {
                "total_detected": len(violations),
                "saved": saved_count,
                "skipped_low_confidence": sum(1 for v in violations if v.get("confidence", 0) < MIN_CONFIDENCE),
                "skipped_duplicate": skipped_count - sum(1 for v in violations if v.get("confidence", 0) < MIN_CONFIDENCE)
            }
        }
        
    except Exception as e:
        print(f"❌ Detection error: {e}")
        return {
            "success": False,
            "error": str(e),
            "violations": [],
            "violation_count": 0
        }

def get_fine_amount(violation_type: str) -> float:
    """Get fine amount based on violation type"""
    fine_map = {
        "No Helmet Violation": 500.0,
        "Phone Usage While Riding": 1000.0,
        "Triple Riding Violation": 1500.0
    }
    return fine_map.get(violation_type, 0.0)

@router.post("/detect-frame")
async def detect_frame(file: UploadFile = File(...)):
    """Detect violations in a single image frame"""
    try:
        detector = get_detector()
        
        # Read image file
        contents = await file.read()
        
        # Process frame
        result = detector.process_frame(contents)
        
        return result
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "violations": [],
            "violation_count": 0
        }

@router.post("/detect-base64")
async def detect_base64(frame_data: dict):
    """Detect violations from base64 encoded frame - with annotation"""
    try:
        detector = get_detector()
        
        # Process frame WITH annotation for preview (return_annotated=True)
        result = detector.process_frame(frame_data.get("frame"), return_annotated=True)
        
        return result
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "violations": [],
            "violation_count": 0
        }

@router.websocket("/ws/live-detection")
async def websocket_detection(websocket: WebSocket):
    """WebSocket endpoint for real-time violation detection"""
    await websocket.accept()
    detector = get_detector()
    
    try:
        while True:
            # Receive frame data from client
            data = await websocket.receive_text()
            frame_data = json.loads(data)
            
            # Process frame
            result = detector.process_frame(frame_data.get("frame"))
            
            # Send results back
            await websocket.send_json(result)
            
    except WebSocketDisconnect:
        print("WebSocket disconnected")
    except Exception as e:
        print(f"WebSocket error: {e}")
        await websocket.close()
