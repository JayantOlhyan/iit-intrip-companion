from pydantic import BaseModel, Field
from typing import List, Dict, Any
from datetime import datetime

class Product(BaseModel):
    id: str
    type: str  # 'flight' or 'hotel'
    title: str
    start_time: datetime
    end_time: datetime
    meta: Dict[str, Any] = Field(default_factory=dict)

class Trip(BaseModel):
    id: str
    traveler_name: str
    products: List[Product]

class Card(BaseModel):
    type: str
    title: str
    message: str
    actions: List[Dict[str, Any]] = Field(default_factory=list)

class ChatRequest(BaseModel):
    trip_id: str
    message: str

class ChatResponse(BaseModel):
    answer: str
    cards: List[Card] = Field(default_factory=list)
