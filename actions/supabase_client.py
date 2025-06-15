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

if __name__ == "__main__":
    print(get_word_details("go"))