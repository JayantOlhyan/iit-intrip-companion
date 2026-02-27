import os
from fastapi import FastAPI
from dotenv import load_dotenv
from google import genai

load_dotenv()

app = FastAPI()

API_KEY = os.getenv("API_KEY")
client = genai.Client(api_key=API_KEY) if API_KEY else None

@app.get("/")
def read_root():
    return {"Hello": "World", "api_key_loaded": bool(API_KEY)}

@app.get("/generate")
def generate(prompt: str = "Explain the importance of APIs in one short sentence."):
    if not client:
        return {"error": "API Key is missing."}
    
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        return {"prompt": prompt, "response": response.text}
    except Exception as e:
        return {"error": str(e)}
