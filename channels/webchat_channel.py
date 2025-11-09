from rasa.core.channels.channel import InputChannel, UserMessage, OutputChannel
from sanic import Blueprint, response

class WebchatInput(InputChannel):
    def blueprint(self, on_new_message):
        custom_webchat = Blueprint("webchat_webhook", __name__)

        @custom_webchat.route("/webhook", methods=["POST"])
        async def receive(request):
            data = request.json
            sender_id = data.get("sender", "default")
            text = data.get("message")
            await on_new_message(UserMessage(text, OutputChannel(), sender_id=sender_id))
            return response.json({"status": "ok"})

        return custom_webchat
