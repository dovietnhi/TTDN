import sqlite3
import json
import os

db_path = "/app/data/rasa.db"
export_path = "/app/data/exported_conversations.json"

# Kết nối SQLite
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Lấy toàn bộ sự kiện user và bot (cột "data" chứ không phải "event")
cursor.execute("""
    SELECT sender_id, type_name, data
    FROM events
    WHERE type_name IN ('user', 'bot')
    ORDER BY sender_id, timestamp
""")

rows = cursor.fetchall()

conversations = {}
for sender_id, type_name, data_json in rows:
    try:
        event = json.loads(data_json)
    except json.JSONDecodeError:
        continue

    text = event.get("text", "")
    if not text:
        continue

    if sender_id not in conversations:
        conversations[sender_id] = []

    conversations[sender_id].append({
        "role": "user" if type_name == "user" else "bot",
        "text": text
    })

# Định dạng lại thành danh sách JSON
output = [{"sender_id": sid, "conversation": conv}
          for sid, conv in conversations.items()]

# Ghi ra file JSON
os.makedirs(os.path.dirname(export_path), exist_ok=True)
with open(export_path, "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=4)

print(f"✅ Đã xuất {len(output)} cuộc hội thoại ra {export_path}")
