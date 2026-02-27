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
   pytest
   ```
