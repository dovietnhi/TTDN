from rasa.core.channels.channel import InputChannel, UserMessage, OutputChannel
from sanic import Blueprint, response
from sanic.request import Request
import json
import psycopg2
import os
from datetime import datetime

class PostgresLogger:
    def __init__(self):
        self.pg_url = os.getenv("POSTGRES_URL", "postgresql://rasa:rasa_password@postgres:5432/rasa_db")
        self._create_table()

    def _create_table(self):
        conn = psycopg2.connect(self.pg_url)
        cur = conn.cursor()
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
        conn.commit()
        cur.close()
        conn.close()

    def save(self, sender_id, text, is_bot=False, intent=None, buttons=None, timestamp=None):
        timestamp = timestamp or datetime.now()
        conn = psycopg2.connect(self.pg_url)
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO chat_history (sender_id, is_bot, text, intent, buttons, timestamp)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (sender_id, is_bot, text, intent, json.dumps(buttons) if buttons else None, timestamp))
        conn.commit()
        cur.close()
        conn.close()

logger = PostgresLogger()

class WebchatOutput(OutputChannel):
    def __init__(self, sender_id: str):
        self.sender_id = sender_id

    async def send_text_message(self, recipient_id: str, text: str):
        logger.save(self.sender_id, text, is_bot=True)
        # gửi về client
        return {"text": text}

    async def send_text_with_buttons(self, recipient_id: str, text: str, buttons, **kwargs):
        logger.save(self.sender_id, text, is_bot=True, buttons=buttons)
        return {"text": text, "buttons": buttons}

class WebchatInput(InputChannel):
    @classmethod
    def name(cls):
        return "custom_webchat"

    def blueprint(self, on_new_message):
        webchat_webhook = Blueprint('webchat_webhook', __name__)

        @webchat_webhook.route("/webchat", methods=['POST'])
        async def receive(request: Request):
            data = request.json
            sender_id = data.get("sender", "webchat_user")
            text = data.get("message")
            intent = None

            # Lưu message user
            logger.save(sender_id, text, is_bot=False)

            # Forward vào Rasa
            collector = WebchatOutput(sender_id)
            user_msg = UserMessage(text, collector, sender_id, input_channel=self.name())
            await on_new_message(user_msg)
            return response.json({"status": "ok"})

        return webchat_webhook
