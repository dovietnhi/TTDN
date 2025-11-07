import psycopg2
import json
import os
from datetime import datetime
import traceback

# --- Kết nối PostgreSQL ---
try:
    # URL kết nối từ environment variable
    # Ví dụ: postgresql://rasa:rasa_password@postgres:5432/rasa_db
    pg_url = os.getenv("POSTGRES_URL", "postgresql://rasa:rasa_password@postgres:5432/rasa_db")
    
    # Parse URL
    import re
    m = re.match(r'postgresql://([^:]+):([^@]+)@([^:]+):(\d+)/(.+)', pg_url)
    if not m:
        raise ValueError("POSTGRES_URL không hợp lệ")
    user, password, host, port, dbname = m.groups()

    conn = psycopg2.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        dbname=dbname
    )
    cursor = conn.cursor()
    print("✅ Kết nối PostgreSQL thành công")

except Exception as e:
    print("❌ Không thể kết nối PostgreSQL:", e)
    traceback.print_exc()
    exit(1)

# --- Đọc dữ liệu conversation ---
try:
    # Bảng events trong PostgreSQL tracker store của Rasa
    # Mỗi event có sender_id, event, text, parse_data (JSON)
    query = """
        SELECT sender_id, event, text, parse_data
        FROM events
        ORDER BY sender_id, timestamp
    """
    cursor.execute(query)
    rows = cursor.fetchall()

    conversations_dict = {}
    for sender_id, event_type, text, parse_data in rows:
        if sender_id not in conversations_dict:
            conversations_dict[sender_id] = []
        if event_type == 'user':
            intent = parse_data.get('intent', {}).get('name') if parse_data else None
            conversations_dict[sender_id].append({
                "sender": "user",
                "text": text,
                "intent": intent
            })
        elif event_type == 'bot':
            conversations_dict[sender_id].append({
                "sender": "bot",
                "text": text
            })

    # Chuyển dict thành list
    conversations = list(conversations_dict.values())
    print(f"✅ Đọc {len(conversations)} cuộc hội thoại từ PostgreSQL")

except Exception as e:
    print("❌ Lỗi khi đọc dữ liệu từ PostgreSQL:", e)
    traceback.print_exc()
    conversations = []

finally:
    cursor.close()
    conn.close()

# --- Xuất ra JSON ---
try:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = f"/app/chat_data/chat_data_{timestamp}.json"

    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            try:
                old_data = json.load(f)
            except json.JSONDecodeError:
                print("⚠️ File JSON cũ bị lỗi, tạo mới")
                old_data = []
    else:
        old_data = []

    merged_data = old_data + conversations

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(merged_data, f, ensure_ascii=False, indent=2)

    print(f"✅ Đã xuất {len(conversations)} cuộc hội thoại mới (tổng {len(merged_data)}) vào {file_path}")
    print(f"✅ Thời gian xuất: {datetime.now()}")

except Exception as e:
    print("❌ Lỗi khi ghi file JSON:", e)
    traceback.print_exc()
