from fastapi import APIRouter, Query
from datetime import datetime, timedelta
from typing import Optional
from ..database import violations_collection, officers_collection

router = APIRouter(prefix="/analytics", tags=["Analytics"])
stats_router = APIRouter(prefix="/stats", tags=["Statistics"])

@router.get("/dashboard")
async def get_dashboard_stats():
    """Get overall dashboard statistics"""
    
    # Total violations
    total_violations = await violations_collection.count_documents({})
    
    # Violations by status
    pending_violations = await violations_collection.count_documents({"status": "pending"})
    resolved_violations = await violations_collection.count_documents({"status": "resolved"})
    
    # Total officers
    total_officers = await officers_collection.count_documents({})
    active_officers = await officers_collection.count_documents({"status": "active"})
    
    # Today's violations
    today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    today_violations = await violations_collection.count_documents({
        "timestamp": {"$gte": today}
    })
    
    # Total fines collected
    pipeline = [
        {"$group": {"_id": None, "total": {"$sum": "$fine_amount"}}}
    ]
    result = await violations_collection.aggregate(pipeline).to_list(1)
    total_fines = result[0]["total"] if result else 0
    
    return {
        "total_violations": total_violations,
        "pending_violations": pending_violations,
        "resolved_violations": resolved_violations,
        "total_officers": total_officers,
        "active_officers": active_officers,
        "today_violations": today_violations,
        "total_fines": total_fines
    }

@router.get("/violations-by-type")
async def get_violations_by_type():
    """Get violations grouped by type"""
    
    pipeline = [
        {"$group": {
            "_id": "$violation_type",
            "count": {"$sum": 1}
        }}
    ]
    
    violations = await violations_collection.aggregate(pipeline).to_list(None)
    
    return [
        {"type": v["_id"], "count": v["count"]}
        for v in violations
    ]

@router.get("/violations-trend")
async def get_violations_trend(days: int = 7):
    """Get violations trend for the last N days"""
    
    start_date = datetime.utcnow() - timedelta(days=days)
    
    pipeline = [
        {"$match": {"timestamp": {"$gte": start_date}}},
        {"$group": {
            "_id": {
                "$dateToString": {
                    "format": "%Y-%m-%d",
                    "date": "$timestamp"
                }
            },
            "count": {"$sum": 1}
        }},
        {"$sort": {"_id": 1}}
    ]
    
    violations = await violations_collection.aggregate(pipeline).to_list(None)
    
    return [
        {"date": v["_id"], "count": v["count"]}
        for v in violations
    ]

@router.get("/top-violations")
async def get_top_violations(limit: int = 5):
    """Get top violation types"""
    
    pipeline = [
        {"$group": {
            "_id": "$violation_type",
            "count": {"$sum": 1}
        }},
        {"$sort": {"count": -1}},
        {"$limit": limit}
    ]
    
    violations = await violations_collection.aggregate(pipeline).to_list(None)
    
    return [
        {"violation_type": v["_id"], "count": v["count"]}
        for v in violations
    ]

@router.get("/officer-performance")
async def get_officer_performance():
    """Get violations reported by each officer"""
    
    pipeline = [
        {"$match": {"officer_id": {"$ne": None}}},
        {"$group": {
            "_id": "$officer_id",
            "violations_reported": {"$sum": 1}
        }}
    ]
    
    violations = await violations_collection.aggregate(pipeline).to_list(None)
    
    return [
        {"officer_id": v["_id"], "violations_reported": v["violations_reported"]}
        for v in violations
    ]

# Stats endpoints for frontend Analytics page
@stats_router.get("/")
async def get_stats():
    """Get summary statistics for analytics cards"""
    
    # Count violations by type
    helmet_count = await violations_collection.count_documents({"violation_type": "No Helmet Violation"})
    mobile_count = await violations_collection.count_documents({"violation_type": "Phone Usage While Riding"})
    triple_count = await violations_collection.count_documents({"violation_type": "Triple Riding Violation"})
    total_count = await violations_collection.count_documents({})
    
    return {
        "total": total_count,
        "helmet": helmet_count,
        "mobile": mobile_count,
        "triple": triple_count
    }

@stats_router.get("/dashboard")
async def get_dashboard_trends(type: Optional[str] = Query(None)):
    """Get trend data for dashboard charts with optional filtering"""
    
    # Get last 7 days of data
    start_date = datetime.utcnow() - timedelta(days=7)
    
    # Build match query
    match_query = {"timestamp": {"$gte": start_date}}
    if type and type != "All":
        match_query["violation_type"] = type
    
    # Aggregate by date and violation type
    pipeline = [
        {"$match": match_query},
        {"$group": {
            "_id": {
                "date": {
                    "$dateToString": {
                        "format": "%Y-%m-%d",
                        "date": "$timestamp"
                    }
                },
                "type": "$violation_type"
            },
            "count": {"$sum": 1}
        }},
        {"$sort": {"_id.date": 1}}
    ]
    
    violations = await violations_collection.aggregate(pipeline).to_list(None)
    
    # Group by date
    trends_map = {}
    for v in violations:
        date = v["_id"]["date"]
        vtype = v["_id"]["type"]
        count = v["count"]
        
        if date not in trends_map:
            trends_map[date] = {"date": date, "helmet": 0, "mobile": 0, "triple": 0}
        
        # Map violation types to chart data
        if vtype == "No Helmet Violation":
            trends_map[date]["helmet"] = count
        elif vtype == "Phone Usage While Riding":
            trends_map[date]["mobile"] = count
        elif vtype == "Triple Riding Violation":
            trends_map[date]["triple"] = count
    
    # Convert to list and sort by date
    trends = list(trends_map.values())
    trends.sort(key=lambda x: x["date"])
    
    return {"trends": trends}
