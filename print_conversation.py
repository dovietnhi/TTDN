import sqlite3
import sys
import json

# Đường dẫn đến SQLite database
DB_PATH = "/app/data/rasa.db"

# Sender_id cần xem conversation
SENDER_ID = "54b0def1183c4f82a1ee51699be2cf41"  # thay bằng sender_id Webchat thực tế

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Lấy toàn bộ event của sender_id theo thời gian
query = """
SELECT timestamp, type_name, intent_name, action_name, data
FROM events
WHERE sender_id = ?
ORDER BY timestamp ASC
"""
cursor.execute(query, (SENDER_ID,))
rows = cursor.fetchall()

for row in rows:
    timestamp, type_name, intent_name, action_name, data_json = row
    text = None
    if data_json:
        try:
            data = json.loads(data_json)
            text = data.get("text")
        except:
            text = None

    if type_name == "user":
        print(f"User ({intent_name}): {text}")
    elif type_name == "bot":
        print(f"Bot: {text}")
    elif type_name == "action":
        print(f"Action: {action_name}")
    elif type_name == "slot":
        print(f"Slot set: {action_name} = {text}")
    else:
        # các type khác như user_featurization, etc
        print(f"{type_name}: {text}")

conn.close()
