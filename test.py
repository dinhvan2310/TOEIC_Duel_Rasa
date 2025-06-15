import os
from google import genai

client = genai.Client(api_key='AIzaSyDslLO4803-g3UvoHhN94hF8CAcZRgWmAE')

response = client.models.generate_content(
    model="gemini-1.5-flash",
    contents=["Hello, world! I want to learn about countable and uncountable nouns"]
)

print(response.text)