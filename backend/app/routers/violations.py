from fastapi import APIRouter, HTTPException
from typing import List, Optional
from datetime import datetime
from bson import ObjectId
from .. import models
from ..database import violations_collection
from ..email_service import get_email_service

router = APIRouter(prefix="/violations", tags=["Violations"])

def violation_helper(violation) -> dict:
    """Convert MongoDB document to dict"""
    return {
        "id": str(violation["_id"]),
        "vehicle_number": violation["vehicle_number"],
        "violation_type": violation["violation_type"],
        "location": violation.get("location"),
        "officer_id": violation.get("officer_id"),
        "status": violation["status"],
        "fine_amount": violation["fine_amount"],
        "image_path": violation.get("image_path"),
        "timestamp": violation["timestamp"],
        "confidence": violation.get("confidence"),
        "detection_class": violation.get("detection_class"),
        "bbox": violation.get("bbox")
    }

@router.get("/")
async def get_violations(
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None
):
    """Get all violations with optional filtering - returns flat array"""
    query = {}
    if status:
        query["status"] = status
    
    violations = []
    async for violation in violations_collection.find(query).sort("timestamp", -1).skip(skip).limit(limit):
        violations.append(violation_helper(violation))
    
    return violations

@router.get("/{violation_id}")
async def get_violation(violation_id: str):
    """Get a specific violation by ID"""
    if not ObjectId.is_valid(violation_id):
        raise HTTPException(status_code=400, detail="Invalid violation ID")
    
    violation = await violations_collection.find_one({"_id": ObjectId(violation_id)})
    
    if not violation:
        raise HTTPException(status_code=404, detail="Violation not found")
    
    return violation_helper(violation)

@router.post("/")
async def create_violation(
    vehicle_number: str,
    violation_type: str,
    location: Optional[str] = None,
    officer_id: Optional[str] = None,
    fine_amount: float = 0.0
):
    """Create a new violation"""
    violation_data = {
        "vehicle_number": vehicle_number,
        "violation_type": violation_type,
        "location": location,
        "officer_id": officer_id,
        "fine_amount": fine_amount,
        "status": "pending",
        "timestamp": datetime.utcnow(),
        "image_path": None
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
            location=location or "N/A",
            timestamp=violation_data["timestamp"],
            violation_id=str(result.inserted_id),
            image_path=None,
            confidence=None
        )
    except Exception as email_err:
        print(f"⚠️ Failed to send email notification: {email_err}")
    
    return {
        "message": "Violation created successfully",
        "violation": violation_helper(created_violation)
    }

@router.put("/{violation_id}")
async def update_violation(
    violation_id: str,
    status: Optional[str] = None
):
    """Update violation status"""
    if not ObjectId.is_valid(violation_id):
        raise HTTPException(status_code=400, detail="Invalid violation ID")
    
    violation = await violations_collection.find_one({"_id": ObjectId(violation_id)})
    
    if not violation:
        raise HTTPException(status_code=404, detail="Violation not found")
    
    update_data = {}
    if status:
        update_data["status"] = status
    
    if update_data:
        await violations_collection.update_one(
            {"_id": ObjectId(violation_id)},
            {"$set": update_data}
        )
    
    updated_violation = await violations_collection.find_one({"_id": ObjectId(violation_id)})
    
    return {
        "message": "Violation updated successfully",
        "violation": violation_helper(updated_violation)
    }

@router.delete("/{violation_id}")
async def delete_violation(violation_id: str):
    """Delete a violation"""
    if not ObjectId.is_valid(violation_id):
        raise HTTPException(status_code=400, detail="Invalid violation ID")
    
    violation = await violations_collection.find_one({"_id": ObjectId(violation_id)})
    
    if not violation:
        raise HTTPException(status_code=404, detail="Violation not found")
    
    await violations_collection.delete_one({"_id": ObjectId(violation_id)})
    
    return {"message": "Violation deleted successfully"}
