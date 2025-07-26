# actions/ValidateMessageSendForm.py

from typing import Any, Text, Dict
from rasa_sdk import Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormValidationAction

class ValidateMessageSendForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_message_send_form"

    known_names = {"रमेश", "सीता", "राजु", "अनु", "बिमल", "सविता"}

    def validate_message_receiver_name(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict,
    ) -> Dict[Text, Any]:

        latest_intent = tracker.latest_message.get("intent", {}).get("name")

        # 👇 If user denies, cancel the form
        if latest_intent == "deny":
            dispatcher.utter_message(text="ठिक छ, सन्देश प्रक्रिया रद्द गरियो।")
            return {"message_receiver_name": None}

        cleaned_value = slot_value.strip()

        # 👇 Check against known name dictionary
        if cleaned_value not in self.known_names:
            dispatcher.utter_message(text=f'"{cleaned_value}" नाम सम्पर्क सूचीमा भेटिएन। कृपया अर्को नाम प्रयास गर्नुहोस्।')
            return {"message_receiver_name": None}

        # ✅ Valid name
        return {"message_receiver_name": cleaned_value}
