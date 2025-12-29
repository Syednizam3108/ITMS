from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from ..database import violations_collection
from ..email_service import get_email_service
from bson import ObjectId
import os
import shutil
from datetime import datetime
from PIL import Image
import base64
from io import BytesIO
from .detection import get_detector

router = APIRouter(prefix="/upload", tags=["Upload"])

UPLOAD_DIR = "app/static/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def get_fine_amount(violation_type: str) -> float:
    """Get fine amount based on violation type"""
    fine_map = {
        "No Helmet": 500.0,
        "Mobile Usage": 1000.0,
        "Triple Riding": 1500.0,
        "No Helmet Violation": 500.0,
        "Phone Usage While Riding": 1000.0,
        "Triple Riding Violation": 1500.0
    }
    return fine_map.get(violation_type, 0.0)

@router.post("/violation")
async def upload_violation(
    vehicle_number: str = Form(...),
    violation_type: str = Form(...),
    location: str = Form("Manual Upload"),
    officer_id: str = Form(None),
    file: UploadFile = File(...)
):
    """Upload a violation with YOLOv8n detection"""
    filepath = None
    
    try:
        # Read and save the uploaded image
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        file_extension = os.path.splitext(file.filename)[1]
        filename = f"violation_{timestamp}_{violation_type.replace(' ', '_')}{file_extension}"
        filepath = os.path.join(UPLOAD_DIR, filename)
        
        # Save image file
        with open(filepath, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Run YOLOv8n detection on the uploaded image
        detector = get_detector()
        
        # Convert image to base64 for detector
        with Image.open(filepath) as img:
            buffered = BytesIO()
            img.save(buffered, format="JPEG")
            img_base64 = base64.b64encode(buffered.getvalue()).decode()
            frame_data = f"data:image/jpeg;base64,{img_base64}"
        
        # Process with YOLOv8n
        detection_result = detector.process_frame(frame_data, return_annotated=False)
        
        # Extract confidence from detection results
        confidence = 0.0
        detected_violations = detection_result.get("violations", [])
        
    except Exception as e:
        # Clean up file if any error occurs during processing
        if filepath and os.path.exists(filepath):
            os.remove(filepath)
        raise HTTPException(status_code=500, detail=f"Upload processing failed: {str(e)}")
    
    # EDGE CASE 1: No violations detected at all
    if not detected_violations or len(detected_violations) == 0:
        # Clean up uploaded file since no violation was detected
        if os.path.exists(filepath):
            os.remove(filepath)
        
        raise HTTPException(
            status_code=400, 
            detail=f"❌ No traffic violations detected by AI in the uploaded image. Please upload an image containing a clear {violation_type} violation."
        )
    
    # Get highest confidence from detected violations
    confidence = max([v.get("confidence", 0.0) for v in detected_violations])
    
    # Verify detected violation matches user's selection with SMART MATCHING
    detected_types = [v.get("type") for v in detected_violations]
    detected_classes = [v.get("class") for v in detected_violations]
    
    violation_type_map = {
        "No Helmet": "No Helmet Violation",
        "Mobile Usage": "Phone Usage While Riding",
        "Triple Riding": "Triple Riding Violation"
    }
    
    expected_type = violation_type_map.get(violation_type)
    
    # EDGE CASE 2: User selected wrong violation type
    if expected_type and expected_type not in detected_types:
        # Clean up uploaded file
        if os.path.exists(filepath):
            os.remove(filepath)
        
        # Build helpful error message
        detected_violations_str = ", ".join([f"{v.get('class')} ({v.get('confidence'):.0%})" for v in detected_violations])
        
        raise HTTPException(
            status_code=400,
            detail=f"❌ Violation type mismatch! You selected '{violation_type}' but AI detected: {detected_violations_str}. Please select the correct violation type matching the image content."
        )
    
    # EDGE CASE 3: Multiple violations detected - use the one matching user's selection
    matched_violation = None
    for v in detected_violations:
        if v.get("type") == expected_type:
            matched_violation = v
            confidence = v.get("confidence", 0.0)
            break
    
    # EDGE CASE 4: Low confidence detection (< 50%)
    if confidence < 0.5:
        print(f"⚠️ Low confidence detection: {confidence:.0%} - proceeding with caution")
    
    # Determine fine amount
    fine_amount = get_fine_amount(violation_type)
    
    try:
        
        # Create violation record in MongoDB
        violation_data = {
            "vehicle_number": vehicle_number,
            "violation_type": violation_type,
            "location": location,
            "officer_id": officer_id,
            "fine_amount": fine_amount,
            "status": "pending",
            "image_path": f"/static/uploads/{filename}",
            "timestamp": datetime.now(),
            "confidence": round(confidence, 2) if confidence > 0 else None,
            "detection_result": {
                "violation_count": detection_result.get("violation_count", 0),
                "detected": detected_violations
            }
        }
        
        result = await violations_collection.insert_one(violation_data)
        created_violation = await violations_collection.find_one({"_id": result.inserted_id})
        
        # Send email notification with penalty slip
        try:
            email_service = get_email_service()
            await email_service.send_violation_email(
                vehicle_number=vehicle_number,
                violation_type=violation_type,
                fine_amount=fine_amount,
                location=location,
                timestamp=violation_data["timestamp"],
                violation_id=str(result.inserted_id),
                image_path=filepath,
                confidence=confidence
            )
        except Exception as email_err:
            print(f"⚠️ Failed to send email notification: {email_err}")
        
        # Build success message with AI confirmation
        detected_class = detected_violations[0].get("class", "violation")
        
        return {
            "message": f"✅ Violation confirmed by AI: {detected_class} detected with {confidence:.0%} confidence",
            "violation": {
                "id": str(created_violation["_id"]),
                "vehicle_number": created_violation["vehicle_number"],
                "violation_type": created_violation["violation_type"],
                "location": created_violation.get("location"),
                "image_path": created_violation.get("image_path"),
                "confidence": created_violation.get("confidence"),
                "fine_amount": created_violation.get("fine_amount"),
                "timestamp": created_violation["timestamp"]
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

@router.post("/image")
async def upload_image(file: UploadFile = File(...)):
    """Upload an image file"""
    try:
        if not file.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_{file.filename}"
        file_path = os.path.join(UPLOAD_DIR, filename)
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        return {
            "message": "Image uploaded successfully",
            "filename": filename,
            "path": file_path
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")
