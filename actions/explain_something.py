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
        user_messages = [e['text'] for e in tracker.events[-5:] if e.get('event') == 'user' and 'text' in e]
        prompt = f"""
You are an English teacher specializing in TOEIC. Please provide a clear, concise, and engaging explanation tailored to the user's query below. Your explanation should:
- Focus on grammar rules, vocabulary usage, sentence structures, or other relevant topics as needed.
- Be written in simple English, suitable for TOEIC learners.
- Use Markdown formatting and emojis for engagement.
- Include practical examples and tips to help the user understand and apply the concept.
- Avoid repeating previous explanations or unnecessary details.

User Query: {current_input}
History: {user_messages}

Standardized Explanation:
"""
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=[prompt]
        )
        rephrased = response.text
        dispatcher.utter_message(text=rephrased)
        return []