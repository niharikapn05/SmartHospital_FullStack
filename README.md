# Smart Hospital Appointment & Patient Queue System — Full Stack

## Included
- `backend/` — your original Python hospital project plus a FastAPI REST layer (`api.py`)
- `frontend/` — React + TypeScript + Vite dashboard
- The frontend uses the same Patient, Doctor, Appointment, Priority Queue, cancellation, rescheduling, search, and daily report concepts from the backend.

## Important
The original backend was a command-line program and did not expose HTTP endpoints. `api.py` is the bridge that makes the existing `Hospital` class available to the React frontend. Data is stored in memory, so restarting the API resets data.

## Backend
```powershell
cd backend
python -m pip install -r requirements.txt
python -m uvicorn api:app --reload
```
API: http://127.0.0.1:8000
Swagger: http://127.0.0.1:8000/docs

## Frontend
Open a second terminal:
```powershell
cd frontend
npm install
npm run dev
```
Open the URL printed by Vite, normally http://localhost:5173

## Existing CLI
Your original CLI is still available:
```powershell
cd backend
python main.py
```
