from supabase import create_client, Client
from bs4 import BeautifulSoup
import os

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def get_word_description(word: str):
    response = supabase.table("dictionary").select("*").eq("word", word.lower()).execute()
    if response.data:
        entries = ''
        for entry in response.data:
            if entry['description']:
                entries += f", {entry['description']}" if entries else entry['description']
        return entries
    return None

def get_word_details(word: str):
    response = supabase.table("dictionary").select("*").eq("word", word.lower()).execute()
    if response.data:
        entries = ''
        for entry in response.data:
            if entry['html']:
                soup = BeautifulSoup(entry['html'], 'html.parser')
                entries += f" \n{soup.get_text(separator=' ')}" if entries else soup.get_text(separator=" ")
        return entries
    return None

def get_question_data(question_id: int, part_number: int):
    response = supabase.table("questions").select("content, part_number, id").eq("id", question_id).eq("part_number", part_number).execute()
    if response.data:
        return response.data[0]
    return None

def get_question_detail(question_id: int, part_number: int):
    response = supabase.table("question_details").select('content, correct_answer, option_a, option_b, option_c, option_d,explain_en').eq("question_id", question_id).eq("part_number", part_number).execute()
    if response.data:
        return response.data
    return None

def get_full_question(question_id: int, part_number: int):
    question = get_question_data(question_id, part_number)
    detail = get_question_detail(question_id, part_number)
    return {"question": question, "detail": detail}

if __name__ == "__main__":
    print(get_full_question(1, 2))