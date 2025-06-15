from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from google import genai
from rasa_sdk.events import SlotSet

# --- Thêm action mới cho explain_something ---
class ActionExplainSomethingWithLLM(Action):
    def name(self):
        return "action_explain_something_with_llm"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain):
        client = genai.Client(api_key='AIzaSyDslLO4803-g3UvoHhN94hF8CAcZRgWmAE')
        current_input = tracker.latest_message.get('text')
        print(current_input)
        prompt = f"""
Rephrase the following explanation for a TOEIC learner in simple English. Focus on clarity (grammar, vocabulary, sentence structure). Use Markdown and emojis for engagement. Avoid repeating previous explanations or unnecessary details.

User Input: {current_input}

Rephrased Explanation:
"""
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=[prompt]
        )
        rephrased = response.text
        dispatcher.utter_message(text=rephrased)
        return [SlotSet("user_query_continue_or_exit", None)]