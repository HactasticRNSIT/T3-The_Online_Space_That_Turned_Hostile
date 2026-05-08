# modules/database.py
from pymongo import MongoClient
from datetime import datetime
import os

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")

def get_db():
    client = MongoClient(MONGO_URI)
    return client["harassment_detector"]

def save_moderation_event(user_id: str, message: str, toxicity_score: float, alert_level: str):
    db = get_db()
    event = {
        "user_id": user_id,
        "message": message,
        "toxicity_score": toxicity_score,
        "alert_level": alert_level,
        "timestamp": datetime.utcnow()
    }
    db["moderation_events"].insert_one(event)
    return event

def get_recent_events(limit: int = 20):
    db = get_db()
    events = list(
        db["moderation_events"]
        .find({}, {"_id": 0})
        .sort("timestamp", -1)
        .limit(limit)
    )
    return events

def get_events_by_alert_level(level: str):
    db = get_db()
    return list(
        db["moderation_events"]
        .find({"alert_level": level}, {"_id": 0})
        .sort("timestamp", -1)
    )