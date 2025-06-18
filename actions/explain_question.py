from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from google import genai
from actions.supabase_client import get_full_question

class ActionExplainQuestionWithLLM(Action):
    def name(self):
        return "action_explain_question_with_llm"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain):
        question_number = tracker.get_slot("question_number")
        part_number = tracker.get_slot("part_number")
        
        if question_number is None or part_number is None:
            dispatcher.utter_message(text="I'm sorry, I can't explain that question.")
            return []
        
        question_data = get_full_question(question_number, part_number)
        
        client = genai.Client(api_key='AIzaSyDslLO4803-g3UvoHhN94hF8CAcZRgWmAE')
        current_input = tracker.latest_message.get('text')
        user_messages = [e['text'] for e in tracker.events[-2:] if e.get('event') == 'user' and 'text' in e]
        prompt = f"""
You are an English teacher specializing in TOEIC. Depending on question:
{question_data}

- Format of data is:
    - question:
        - part_number: part number of question
        - id: id of question
        - content: question content of question, it should be None if part_number is 1, 2, 3, 4
    - detail: is a list of child of question, part 3, 4, 6, 7 has multiple detail, part 1, 2, 5 has only one detail
        - content: content of detail
        - correct_answer: correct answer of detail
        - option_a: option A of detail
        - option_b: option B of detail
        - option_c: option C of detail
        - option_d: option D of detail
        - explain_en: explanation of detail in English, if part_number is 1, 2, 3, 4, it is transcription of the audio

- Please analyze and explain this question clearly, including:
1. Explain all details of question depending on data above
2. A detailed explanation of why the correct answer is correct

Your answer should be clear, concise, and helpful for learners.
- Be written in simple English, suitable for TOEIC learners.
- Do not use redundant lead-in sentences or repeat the question; focus on explaining the question itself. For listening exercises, do not answer with phrases like 'The key is to accurately match what you hear to what you see in the picture'
- Use Markdown formatting and emojis for engagement.
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