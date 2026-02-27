from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
client = genai.Client(api_key=API_KEY) if API_KEY else None

def generate_text(prompt: str) -> str:
    if not client:
        raise ValueError("API Key is missing")
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt,
    )
    return response.text
