from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import psycopg2
from datetime import datetime
import os
import json

app = FastAPI(title="Webchat -> PostgreSQL API")

# --- CORS để webchat có thể gọi API ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Hoặc chỉ domain webchat
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Cấu hình PostgreSQL ---
PG_URL = os.getenv("POSTGRES_URL", "postgresql://rasa:rasa_password@localhost:5432/rasa_db")

# --- Model nhận dữ liệu từ webchat ---
from typing import Optional, List, Any

class Message(BaseModel):
    sender_id: str
    is_bot: bool
    text: Optional[str] = None
    intent: Optional[str] = None
    buttons: Optional[List[Any]] = None  # <- chấp nhận dict, string hoặc object phức tạp
    timestamp: Optional[str] = None

@app.post("/save_message/")
def save_message(msg: Message):
    try:
        conn = psycopg2.connect(PG_URL)
        cur = conn.cursor()

        # Tạo table nếu chưa có
        cur.execute("""
            CREATE TABLE IF NOT EXISTS chat_history (
                id SERIAL PRIMARY KEY,
                sender_id TEXT NOT NULL,
                is_bot BOOLEAN NOT NULL,
                text TEXT,
                intent TEXT,
                buttons JSONB,
                timestamp TIMESTAMP NOT NULL
            );
        """)

        # Xử lý timestamp
        if msg.timestamp:
            timestamp = datetime.fromisoformat(msg.timestamp.replace("Z", "+00:00"))
        else:
            timestamp = datetime.utcnow()

        # Xử lý buttons
        buttons_json = json.dumps(msg.buttons, ensure_ascii=False) if msg.buttons else None

        # Insert vào DB
        cur.execute("""
            INSERT INTO chat_history (sender_id, is_bot, text, intent, buttons, timestamp)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (msg.sender_id, msg.is_bot, msg.text, msg.intent, buttons_json, timestamp))

        conn.commit()
        cur.close()
        conn.close()

        print(f"[DEBUG] Saved message from {msg.sender_id}: {msg.text}")

        return {"status": "ok", "message": "Saved to DB"}

    except Exception as e:
        print("[ERROR]", e)
        return {"status": "error", "message": str(e)}
