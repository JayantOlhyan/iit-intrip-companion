import os
import json
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from app.models import Trip, ChatRequest, ChatResponse, Card
from app.engine import compute_nudges
from app.llm import generate_text

load_dotenv()

app = FastAPI()

# Add CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_KEY = os.getenv("API_KEY")

@app.get("/")
def read_root():
    return {"Hello": "World", "api_key_loaded": bool(API_KEY)}

@app.get("/status")
def get_status(trip_id: str):
    if trip_id != "demo":
        raise HTTPException(status_code=404, detail="Trip not found")
        
    try:
        with open("data/trip.json", "r") as f:
            trip_data = json.load(f)
            trip = Trip(**trip_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading trip data: {str(e)}")

    nudges = compute_nudges(trip)
    
    return {
        "trip": trip.model_dump(),
        "cards": [card.model_dump() for card in nudges]
    }

@app.post("/chat", response_model=ChatResponse)
def chat_with_agent(request: ChatRequest):
    try:
        with open("data/trip.json", "r") as f:
            trip_data = json.load(f)
            trip = Trip(**trip_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading trip data: {str(e)}")

    # Get standard logic nudges
    nudges = compute_nudges(trip)
    
    # Generate conversational answer from LLM
    try:
        llm_response = generate_text(request.message)
    except Exception as e:
        llm_response = f"I am unable to answer right now: {str(e)}"
        
    # Optional recommendation card
    recommendation = Card(
        type="recommendation",
        title="Agent Suggestion",
        message="Based on your request, I can help rebook your arrangements.",
        actions=[{"label": "Rebook Options", "action_type": "view_rebooking"}]
    )
    
    nudges.append(recommendation)

    return ChatResponse(
        answer=llm_response,
        cards=nudges
    )
