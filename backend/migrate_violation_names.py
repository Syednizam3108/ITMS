import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

async def migrate_violation_names():
    client = AsyncIOMotorClient('mongodb://localhost:27017')
    db = client['traffic_management']
    
    print("\n" + "="*60)
    print("MIGRATING OLD VIOLATION NAMES TO NEW FORMAT")
    print("="*60)
    
    # Update "Triple Riding" → "Triple Riding Violation"
    result1 = await db.violations.update_many(
        {"violation_type": "Triple Riding"},
        {"$set": {"violation_type": "Triple Riding Violation"}}
    )
    print(f"✅ Updated 'Triple Riding' → 'Triple Riding Violation': {result1.modified_count} records")
    
    # Update "Mobile Usage" → "Phone Usage While Riding"
    result2 = await db.violations.update_many(
        {"violation_type": "Mobile Usage"},
        {"$set": {"violation_type": "Phone Usage While Riding"}}
    )
    print(f"✅ Updated 'Mobile Usage' → 'Phone Usage While Riding': {result2.modified_count} records")
    
    print("="*60)
    print(f"TOTAL UPDATED: {result1.modified_count + result2.modified_count} violations")
    print("="*60)
    
    # Verify the changes
    print("\nVerifying updated violation types:")
    pipeline = [
        {"$group": {
            "_id": "$violation_type",
            "count": {"$sum": 1}
        }},
        {"$sort": {"count": -1}}
    ]
    
    result = await db.violations.aggregate(pipeline).to_list(None)
    
    print("\n" + "="*60)
    print("CURRENT VIOLATION TYPES IN DATABASE")
    print("="*60)
    
    total = 0
    for v in result:
        print(f"{v['_id']}: {v['count']}")
        total += v['count']
    
    print("="*60)
    print(f"TOTAL: {total}")
    print("="*60 + "\n")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(migrate_violation_names())
