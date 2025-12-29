from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient
import os

# MongoDB connection URL
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DATABASE_NAME = "traffic_management"

# Async MongoDB client (for FastAPI async endpoints)
client = AsyncIOMotorClient(MONGODB_URL)
database = client[DATABASE_NAME]

# Collections
violations_collection = database["violations"]
officers_collection = database["officers"]

# Helper function to get database
def get_database():
    return database
