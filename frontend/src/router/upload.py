from fastapi import APIRouter, UploadFile, Form, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, database
import os
import shutil

router = APIRouter(prefix="/upload", tags=["Upload"])

UPLOAD_DIR = "app/static/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/")
async def upload_violation(
    vehicle_number: str = Form(...),
    violation_type: str = Form(...),
    file: UploadFile = None,
    db: Session = Depends(database.get_db)
):
    try:
        file_path = None
        if file:
            file_path = os.path.join(UPLOAD_DIR, file.filename)
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)

        new_violation = models.Violation(
            vehicle_number=vehicle_number,
            violation_type=violation_type,
            image_path=file_path
        )
        db.add(new_violation)
        db.commit()
        db.refresh(new_violation)
        return {
            "message": "✅ Violation added successfully!",
            "violation": {
                "id": new_violation.id,
                "vehicle_number": new_violation.vehicle_number,
                "violation_type": new_violation.violation_type,
                "image_path": new_violation.image_path
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {e}")
