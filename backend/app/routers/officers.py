from fastapi import APIRouter, HTTPException
from typing import List, Optional
from datetime import datetime
from bson import ObjectId
from .. import models
from ..database import officers_collection

router = APIRouter(prefix="/officers", tags=["Officers"])

def officer_helper(officer) -> dict:
    """Convert MongoDB document to dict"""
    return {
        "id": str(officer["_id"]),
        "name": officer["name"],
        "badge_number": officer["badge_number"],
        "email": officer["email"],
        "phone": officer["phone"],
        "status": officer["status"],
        "assigned_zone": officer.get("assigned_zone"),
        "created_at": officer["created_at"]
    }

@router.get("/")
async def get_officers(
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None
):
    """Get all officers with optional filtering"""
    query = {}
    if status:
        query["status"] = status
    
    officers = []
    async for officer in officers_collection.find(query).skip(skip).limit(limit):
        officers.append(officer_helper(officer))
    
    total = await officers_collection.count_documents(query)
    
    return {
        "total": total,
        "officers": officers
    }

@router.get("/{officer_id}")
async def get_officer(officer_id: str):
    """Get a specific officer by ID"""
    if not ObjectId.is_valid(officer_id):
        raise HTTPException(status_code=400, detail="Invalid officer ID")
    
    officer = await officers_collection.find_one({"_id": ObjectId(officer_id)})
    
    if not officer:
        raise HTTPException(status_code=404, detail="Officer not found")
    
    return officer_helper(officer)

@router.post("/")
async def create_officer(
    name: str,
    badge_number: str,
    email: str,
    phone: str,
    assigned_zone: Optional[str] = None
):
    """Create a new officer"""
    # Check if badge number or email already exists
    existing = await officers_collection.find_one({
        "$or": [
            {"badge_number": badge_number},
            {"email": email}
        ]
    })
    
    if existing:
        raise HTTPException(status_code=400, detail="Officer with this badge number or email already exists")
    
    officer_data = {
        "name": name,
        "badge_number": badge_number,
        "email": email,
        "phone": phone,
        "status": "active",
        "assigned_zone": assigned_zone,
        "created_at": datetime.utcnow()
    }
    
    result = await officers_collection.insert_one(officer_data)
    created_officer = await officers_collection.find_one({"_id": result.inserted_id})
    
    return {
        "message": "Officer created successfully",
        "officer": officer_helper(created_officer)
    }

@router.put("/{officer_id}")
async def update_officer(
    officer_id: str,
    name: Optional[str] = None,
    phone: Optional[str] = None,
    status: Optional[str] = None,
    assigned_zone: Optional[str] = None
):
    """Update officer details"""
    if not ObjectId.is_valid(officer_id):
        raise HTTPException(status_code=400, detail="Invalid officer ID")
    
    officer = await officers_collection.find_one({"_id": ObjectId(officer_id)})
    
    if not officer:
        raise HTTPException(status_code=404, detail="Officer not found")
    
    update_data = {}
    if name:
        update_data["name"] = name
    if phone:
        update_data["phone"] = phone
    if status:
        update_data["status"] = status
    if assigned_zone:
        update_data["assigned_zone"] = assigned_zone
    
    if update_data:
        await officers_collection.update_one(
            {"_id": ObjectId(officer_id)},
            {"$set": update_data}
        )
    
    updated_officer = await officers_collection.find_one({"_id": ObjectId(officer_id)})
    
    return {
        "message": "Officer updated successfully",
        "officer": officer_helper(updated_officer)
    }

@router.delete("/{officer_id}")
async def delete_officer(officer_id: str):
    """Delete an officer"""
    if not ObjectId.is_valid(officer_id):
        raise HTTPException(status_code=400, detail="Invalid officer ID")
    
    officer = await officers_collection.find_one({"_id": ObjectId(officer_id)})
    
    if not officer:
        raise HTTPException(status_code=404, detail="Officer not found")
    
    await officers_collection.delete_one({"_id": ObjectId(officer_id)})
    
    return {"message": "Officer deleted successfully"}
