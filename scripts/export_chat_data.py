from pymongo import MongoClient
import json
import os
import pymongo
from datetime import datetime

# --- Kết nối MongoDB ---
mongo_url = os.getenv("MONGO_URL", "mongodb://mongodb:27017/rasa")
client = pymongo.MongoClient(mongo_url)
db = client["rasa"]
collection = db["conversations"]

# --- Đọc dữ liệu mới từ MongoDB ---
conversations = []
for conv in collection.find():
    convo = []
    for e in conv.get("events", []):
        if e.get("event") == "user":
            convo.append({
                "sender": "user",
                "text": e.get("text"),
                "intent": e.get("parse_data", {}).get("intent", {}).get("name")
            })
        elif e.get("event") == "bot":
            convo.append({
                "sender": "bot",
                "text": e.get("text")
            })
    if convo:
        conversations.append(convo)

# --- Gộp dữ liệu cũ nếu có ---
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
file_path = f"/app/chat_data/chat_data_{timestamp}.json"

if os.path.exists(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        try:
            old_data = json.load(f)
        except json.JSONDecodeError:
            old_data = []
else:
    old_data = []

# --- Hợp nhất ---
merged_data = old_data + conversations

# --- Ghi lại file JSON ---
with open(file_path, "w", encoding="utf-8") as f:
    json.dump(merged_data, f, ensure_ascii=False, indent=2)

print(f"✅ Đã xuất {len(conversations)} cuộc hội thoại mới (tổng {len(merged_data)}) vào {file_path}")
print(f"✅ Đã xuất dữ liệu vào {datetime.now()}")
