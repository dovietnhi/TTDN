import json
from pymongo import MongoClient
import os

# ------------------------------
# Cấu hình kết nối MongoDB
# ------------------------------
mongo_host = "chatbot-app-mongodb"  # container MongoDB trong Compose
mongo_port = 27017
mongo_db_name = "rasa"               # database bạn dùng trong tracker store
mongo_collection = "events"          # collection chứa events Webchat

export_path = "/app/data/exported_mongo_conversations.json"  # nơi xuất JSON

# ------------------------------
# Kết nối MongoDB
# ------------------------------
client = MongoClient(f"mongodb://{mongo_host}:{mongo_port}")
db = client[mongo_db_name]
collection = db[mongo_collection]

# ------------------------------
# Lấy dữ liệu user + bot
# ------------------------------
cursor = collection.find({"type_name": {"$in": ["user", "bot"]}}).sort("timestamp", 1)

conversations = {}

for doc in cursor:
    sender_id = doc.get("sender_id")
    type_name = doc.get("type_name")
    data = doc.get("data", {})

    text = data.get("text", "")
    if not text:
        continue  # bỏ event không có text

    if sender_id not in conversations:
        conversations[sender_id] = []

    conversations[sender_id].append({
        "role": "user" if type_name == "user" else "bot",
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
