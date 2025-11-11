import json
from pymongo import MongoClient
import os

# ------------------------------
# Cấu hình kết nối MongoDB
# ------------------------------
mongo_host = "localhost"       # host MongoDB (host Windows)
mongo_port = 27017
mongo_db_name = "rasa"
mongo_collection = "rasa_tracker"

export_path = "./data/exported_mongo_conversations.json"

# ------------------------------
# Kết nối MongoDB
# ------------------------------
client = MongoClient(f"mongodb://{mongo_host}:{mongo_port}")
db = client[mongo_db_name]
collection = db[mongo_collection]

# ------------------------------
# Lấy dữ liệu user + bot
# ------------------------------
conversations = {}

for doc in collection.find():
    sender_id = doc.get("sender_id")
    if not sender_id:
        continue

    events = doc.get("events", [])
    for event in events:
        event_type = event.get("event")
        if event_type not in ["user", "bot"]:
            continue

        # user message
        if event_type == "user":
            text = event.get("text", "")
        # bot message
        else:
            text = event.get("text") or event.get("data", {}).get("text", "")

        if not text:
            continue

        if sender_id not in conversations:
            conversations[sender_id] = []

        conversations[sender_id].append({
            "role": "user" if event_type == "user" else "bot",
            "text": text
        })

# ------------------------------
# Chuyển sang danh sách JSON
# ------------------------------
output = [{"sender_id": sid, "conversation": conv} for sid, conv in conversations.items()]

# ------------------------------
# Ghi ra file JSON
# ------------------------------
os.makedirs(os.path.dirname(export_path), exist_ok=True)
with open(export_path, "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=4)

print(f"✅ Đã xuất {len(output)} cuộc hội thoại ra {export_path}")
