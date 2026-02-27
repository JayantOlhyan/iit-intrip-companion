from google import genai
import os
import json
from dotenv import load_dotenv

from app.models import Trip

load_dotenv()

# Updated per instructions to look for GEMINI_API_KEY specifically
API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("API_KEY") 
client = genai.Client(api_key=API_KEY) if API_KEY else None

def generate_text(prompt: str) -> str:
    if not client:
        raise ValueError("API Key is missing")
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt,
    )
    return response.text

def generate_chat_answer(trip: Trip, message: str) -> str:
    if not client:
        return "I am operating in simulated mode. I can see you have a flight and a hotel booked, but I cannot answer complex queries without a GEMINI_API_KEY configured."

    trip_context = trip.model_dump_json()

    prompt = f"""
    You are a helpful travel companion AI. You must ONLY rely on the following 
    trip JSON data to answer the user's question. 

    TRIP DATA:
    {trip_context}

    IMPORTANT RULES:
    1. Do NOT claim you have real-time flight status. Only use the delay/time data provided in the JSON.
    2. Provide your answers with clear assumptions if the data is limited.
    3. Be concise and structured in your suggestions.

    USER QUESTION:
    {message}
    """
    
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        return response.text
    except Exception as e:
        return f"An error occurred while generating a response: {str(e)}"
