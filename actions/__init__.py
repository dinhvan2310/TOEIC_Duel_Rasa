from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

class ActionShowQuestionDetails(Action):
    def name(self):
        return "action_show_question_details"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain):
        # Example: retrieve from slots or database
        main_question = tracker.get_slot("main_question") or "Main question text here."
        detail_questions = tracker.get_slot("detail_questions") or [
            "Detail question 1",
            "Detail question 2",
            "Detail question 3"
        ]
        message = f"Main question:\n{main_question}\n\n"
        message += "Detail questions:\n"
        for idx, q in enumerate(detail_questions, 1):
            message += f"{idx}. {q}\n"
        dispatcher.utter_message(text=message)
        return []
