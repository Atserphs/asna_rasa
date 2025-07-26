# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

# actions/validate_message_form.py

from typing import Any, Text, Dict
from rasa_sdk import Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
# from rasa_sdk.forms import FormValidationAction
from rasa_sdk.types import DomainDict

class ValidateMessageSendForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_message_send_form"

    known_names = {"रमेश", "सीता", "राजु", "अनु", "बिमल", "सविता", "ram"}

    def validate_message_receiver_name(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:

        latest_intent = tracker.latest_message.get("intent", {}).get("name")

        print(f"slot_value_received = {slot_value}")
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

