# iit-intrip-companion

Phase 1 bootstrap of the repo and environment for the trip companion service.

## Run Steps

1. **Activate the virtual environment**:
   ```bash
   source venv/bin/activate
   ```
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Environment Variables**:
   Ensure you have a `.env` file in the root with your `API_KEY` defined.
   ```
   API_KEY="your_api_key_here"
   ```
4. **Run the server**:
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```
5. **Run tests**:
   ```bash
   python -m pytest -q
   ```

## Test Scenarios

To test the dynamic nudge engine, modify `data/trip.json` to simulate these conditions and observe the different `cards` generated in the UI or via `/chat`:

1.  **Normal flow**: Flight departs in 6h, no delay. 
    *   *Expected Nudge*: "Check-in reminder".
2.  **Tight check-in window**: Departure in 1h 30m. 
    *   *Expected Nudge*: "Leave now / commute" + "Check-in urgency"
3.  **Moderate delay**: Delay 45m. 
    *   *Expected Nudge*: "Delay alert + options (Wait vs Rebook vs Notify Hotel)".
4.  **Severe delay**: Delay 180m. 
    *   *Expected Nudge*: "Misconnect risk" + "Reaccommodation guidance".
5.  **Late arrival affects hotel**: Arrival after hotel check-in end. 
    *   *Expected Nudge*: "Late check-in plan" / Notify hotel.
6.  **User intent-driven**: Keep the same trip, but ask a different question in the chat (e.g., "What is the baggage allowance?").
    *   *Expected Output*: Answer changes based on LLM processing the request, but standard trip condition nudges remain.
