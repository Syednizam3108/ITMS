from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from typing import Optional
from bson import ObjectId
from passlib.context import CryptContext

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, field_schema):
        field_schema.update(type="string")

# User Models for Authentication
class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    role: str = "officer"  # officer, admin
    is_active: bool = True

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class User(UserBase):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    hashed_password: str

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class UserResponse(UserBase):
    id: str
    created_at: datetime

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

# Violation Models
class ViolationBase(BaseModel):
    vehicle_number: str
    violation_type: str
    location: Optional[str] = None
    officer_id: Optional[str] = None
    status: str = "pending"
    fine_amount: float = 0.0
    image_path: Optional[str] = None

class ViolationCreate(ViolationBase):
    pass

class ViolationUpdate(BaseModel):
    vehicle_number: Optional[str] = None
    violation_type: Optional[str] = None
    location: Optional[str] = None
    officer_id: Optional[str] = None
    status: Optional[str] = None
    fine_amount: Optional[float] = None
    image_path: Optional[str] = None

class Violation(ViolationBase):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class OfficerBase(BaseModel):
    name: str
    badge_number: str
    email: str
    phone: str
    status: str = "active"
    assigned_zone: Optional[str] = None

class OfficerCreate(OfficerBase):
    pass

class OfficerUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    status: Optional[str] = None
    assigned_zone: Optional[str] = None

class Officer(OfficerBase):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

# Utility functions for password hashing
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)
