from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from actions.supabase_client import get_word_description, get_word_details
import random

class ActionLookupWordMeaning(Action):
    def name(self) -> Text:
        return "action_lookup_word_meaning"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        word = tracker.get_slot("word")
        word = word.lower()
        details = get_word_details(word)
        if details:
            return [SlotSet("word_meaning", details)]
        else:
            return [SlotSet("word_meaning", None)]

class ActionExplainMore(Action):
    def name(self) -> Text:
        return "action_explain_more"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        word = tracker.get_slot("word")
        word = word.lower()
        details = get_word_details(word)
        
        return [
            SlotSet("word_explanation", details),
            SlotSet("word_option", "explain")
        ]