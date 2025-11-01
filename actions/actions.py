from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import datetime
import random
import pytz
    
from typing import Any, Text, Dict, List

class ActionSuggestTopics(Action):
    def name(self) -> Text:
        return "action_suggest_topics"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        last_intent = tracker.latest_message.get("intent", {}).get("name")
        intent_ranking = tracker.latest_message.get("intent_ranking", []) or []

        # Lấy top 3 intent khác intent hiện tại
        suggestions = [i['name'] for i in intent_ranking if i.get('name') and i['name'] != last_intent][:3]

        if suggestions:
            buttons = []
            for sug in suggestions:
                title = sug.replace("_", " ").capitalize()
                payload = f"/{sug}"
                buttons.append({"title": title, "payload": payload})
            dispatcher.utter_message(text="Bạn có muốn hỏi thêm về:", buttons=buttons)
        else:
            dispatcher.utter_message(text="Mình chưa có gợi ý lúc này.")
        return []
