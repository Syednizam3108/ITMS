import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime

async def add_sample_officers():
    client = AsyncIOMotorClient('mongodb://localhost:27017')
    db = client['traffic_management']
    
    print("\n" + "="*60)
    print("ADDING SAMPLE TRAFFIC OFFICERS")
    print("="*60)
    
    sample_officers = [
        {
            "name": "Rajesh Kumar",
            "badge_number": "TP001",
            "email": "rajesh.kumar@traffic.gov.in",
            "phone": "+91-9876543210",
            "status": "active",
            "assigned_zone": "Zone A - Central District",
            "created_at": datetime.now()
        },
        {
            "name": "Priya Sharma",
            "badge_number": "TP002",
            "email": "priya.sharma@traffic.gov.in",
            "phone": "+91-9876543211",
            "status": "active",
            "assigned_zone": "Zone B - North District",
            "created_at": datetime.now()
        },
        {
            "name": "Amit Patel",
            "badge_number": "TP003",
            "email": "amit.patel@traffic.gov.in",
            "phone": "+91-9876543212",
            "status": "active",
            "assigned_zone": "Zone C - South District",
            "created_at": datetime.now()
        },
        {
            "name": "Sneha Reddy",
            "badge_number": "TP004",
            "email": "sneha.reddy@traffic.gov.in",
            "phone": "+91-9876543213",
            "status": "pending",
            "assigned_zone": "Zone D - East District",
            "created_at": datetime.now()
        },
        {
            "name": "Vikram Singh",
            "badge_number": "TP005",
            "email": "vikram.singh@traffic.gov.in",
            "phone": "+91-9876543214",
            "status": "active",
            "assigned_zone": "Zone E - West District",
            "created_at": datetime.now()
        },
        {
            "name": "Anjali Verma",
            "badge_number": "TP006",
            "email": "anjali.verma@traffic.gov.in",
            "phone": "+91-9876543215",
            "status": "active",
            "assigned_zone": "Zone A - Central District",
            "created_at": datetime.now()
        },
        {
            "name": "Suresh Nair",
            "badge_number": "TP007",
            "email": "suresh.nair@traffic.gov.in",
            "phone": "+91-9876543216",
            "status": "inactive",
            "assigned_zone": "Zone B - North District",
            "created_at": datetime.now()
        },
        {
            "name": "Kavita Desai",
            "badge_number": "TP008",
            "email": "kavita.desai@traffic.gov.in",
            "phone": "+91-9876543217",
            "status": "active",
            "assigned_zone": "Zone C - South District",
            "created_at": datetime.now()
        }
    ]
    
    result = await db.officers.insert_many(sample_officers)
    
    print(f"✅ Successfully added {len(result.inserted_ids)} officers")
    print("\nOfficers added:")
    for officer in sample_officers:
        print(f"  - {officer['name']} ({officer['badge_number']}) - {officer['status'].upper()}")
    
    # Show totals
    total = await db.officers.count_documents({})
    active = await db.officers.count_documents({"status": "active"})
    pending = await db.officers.count_documents({"status": "pending"})
    inactive = await db.officers.count_documents({"status": "inactive"})
    
    print("="*60)
    print(f"TOTAL OFFICERS: {total}")
    print(f"  Active: {active}")
    print(f"  Pending: {pending}")
    print(f"  Inactive: {inactive}")
    print("="*60 + "\n")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(add_sample_officers())
