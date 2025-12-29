import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

async def check_violation_types():
    client = AsyncIOMotorClient('mongodb://localhost:27017')
    db = client['traffic_management']
    
    # Get all violation types with counts
    pipeline = [
        {"$group": {
            "_id": "$violation_type",
            "count": {"$sum": 1}
        }},
        {"$sort": {"count": -1}}
    ]
    
    result = await db.violations.aggregate(pipeline).to_list(None)
    
    print("\n" + "="*50)
    print("VIOLATION TYPES IN DATABASE")
    print("="*50)
    
    total = 0
    for v in result:
        print(f"{v['_id']}: {v['count']}")
        total += v['count']
    
    print("="*50)
    print(f"TOTAL: {total}")
    print("="*50)
    
    await client.close()

if __name__ == "__main__":
    asyncio.run(check_violation_types())
