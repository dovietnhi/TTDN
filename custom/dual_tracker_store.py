# custom/dual_tracker_store.py

from rasa.core.tracker_store import TrackerStore
from rasa.core.trackers import DialogueStateTracker
from rasa.shared.core.domain import Domain
from pymongo import MongoClient
import sqlite3
import json

class DualTrackerStore(TrackerStore):
    """Tracker store lưu song song vào MongoDB và SQLite."""

    def __init__(self, domain: Domain, sqlite_path: str, mongo_url: str):
        super().__init__(domain)
        
        # MongoDB
        self.mongo = MongoClient(mongo_url).rasa.conversations
        
        # SQLite
        self.sqlite_path = sqlite_path
        self.conn = sqlite3.connect(sqlite_path, check_same_thread=False)
        c = self.conn.cursor()
        # Tạo bảng tracker nếu chưa có
        c.execute("""
            CREATE TABLE IF NOT EXISTS tracker (
                sender_id TEXT PRIMARY KEY,
                events TEXT
            )
        """)
        self.conn.commit()

    def save(self, tracker: DialogueStateTracker) -> None:
        """Lưu tracker vào cả MongoDB và SQLite."""
        events_json = json.dumps([e.as_dict() for e in tracker.events])
        
        # MongoDB
        self.mongo.update_one(
            {"sender_id": tracker.sender_id},
            {"$set": {"events": events_json}},
            upsert=True
        )
        
        # SQLite
        c = self.conn.cursor()
        c.execute(
            "INSERT OR REPLACE INTO tracker (sender_id, events) VALUES (?, ?)",
            (tracker.sender_id, events_json)
        )
        self.conn.commit()

    def retrieve(self, sender_id: str) -> DialogueStateTracker:
        """Lấy tracker từ MongoDB nếu có, nếu không lấy SQLite."""
        data = self.mongo.find_one({"sender_id": sender_id})
        if data and "events" in data:
            events = json.loads(data["events"])
        else:
            # Lấy từ SQLite
            c = self.conn.cursor()
            c.execute("SELECT events FROM tracker WHERE sender_id = ?", (sender_id,))
            row = c.fetchone()
            if row:
                events = json.loads(row[0])
            else:
                events = []
        
        return DialogueStateTracker.from_dict(sender_id, events, self.domain)
