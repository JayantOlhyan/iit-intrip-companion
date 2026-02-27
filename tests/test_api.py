from fastapi.testclient import TestClient
from app.main import app
import json

client = TestClient(app)

def test_status_endpoint():
    response = client.get("/status?trip_id=demo")
    assert response.status_code == 200
    
    data = response.json()
    assert "trip" in data
    assert "cards" in data
    assert len(data["cards"]) >= 1

def test_chat_endpoint():
    request_data = {
        "trip_id": "demo",
        "message": "Hello"
    }
    response = client.post("/chat", json=request_data)
    assert response.status_code == 200
    
    data = response.json()
    assert "answer" in data
    assert "cards" in data
    assert len(data["cards"]) >= 1
