import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime, timedelta
import random

async def add_historical_violations():
    client = AsyncIOMotorClient('mongodb://localhost:27017')
    db = client['traffic_management']
    
    print("\n" + "="*60)
    print("ADDING HISTORICAL VIOLATION DATA FOR TRENDS")
    print("="*60)
    
    violation_types = [
        "No Helmet Violation",
        "Phone Usage While Riding", 
        "Triple Riding Violation"
    ]
    
    fine_amounts = {
        "No Helmet Violation": 500.0,
        "Phone Usage While Riding": 1000.0,
        "Triple Riding Violation": 1500.0
    }
    
    added_count = 0
    
    # Add violations for the past 7 days
    for days_ago in range(7, 0, -1):
        violation_date = datetime.now() - timedelta(days=days_ago)
        
        # Random number of violations per day (3-8 violations)
        daily_violations = random.randint(3, 8)
        
        for _ in range(daily_violations):
            violation_type = random.choice(violation_types)
            
            violation_doc = {
                "vehicle_number": f"VEH_{violation_date.strftime('%Y%m%d')}_{random.randint(1000, 9999)}",
                "violation_type": violation_type,
                "timestamp": violation_date,
                "location": "Historical Data",
                "status": "pending",
                "fine_amount": fine_amounts[violation_type],
                "confidence": round(random.uniform(0.60, 0.95), 2),
                "image_path": None
            }
            
            await db.violations.insert_one(violation_doc)
            added_count += 1
        
        print(f"✅ {violation_date.strftime('%Y-%m-%d')}: Added {daily_violations} violations")
    
    print("="*60)
    print(f"TOTAL HISTORICAL VIOLATIONS ADDED: {added_count}")
    print("="*60)
    
    # Show new totals
    total = await db.violations.count_documents({})
    helmet = await db.violations.count_documents({"violation_type": "No Helmet Violation"})
    mobile = await db.violations.count_documents({"violation_type": "Phone Usage While Riding"})
    triple = await db.violations.count_documents({"violation_type": "Triple Riding Violation"})
    
    print(f"\nNEW TOTALS:")
    print(f"  Total: {total}")
    print(f"  No Helmet: {helmet}")
    print(f"  Mobile Usage: {mobile}")
    print(f"  Triple Riding: {triple}")
    print("="*60 + "\n")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(add_historical_violations())
