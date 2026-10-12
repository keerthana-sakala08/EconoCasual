# EconoCausal — Week 1 Starter Project

A beginner-friendly starter for **Dynamic Pricing via Double Machine Learning**.
Week 1 scope: project setup, dashboard shell, CSV upload, basic dataset summary, and frontend/backend connection.

## Folder structure
- `frontend/` — React + Vite dashboard
- `backend/` — Flask API for CSV upload and basic analysis
- `sample_data/` — sample discount/sales dataset

## Requirements
- Node.js LTS (includes npm)
- Python 3.10+ recommended

## Run the backend (Terminal 1)
```powershell
cd backend
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```
Backend runs at `http://127.0.0.1:5000`.

If PowerShell blocks activation, run this once for the current terminal:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```
You can also skip activation and use `py -m pip install -r requirements.txt`, then `py app.py`.

## Run the frontend (Terminal 2)
```powershell
cd frontend
npm install
npm run dev
```
Open the local URL printed by Vite, usually `http://localhost:5173`.

## Upload a CSV
Use the included `sample_data/pricing_data.csv`. The CSV should have column headers. The app displays row/column counts, column names, and numeric summaries.

## Important
This is a Week 1 foundation, **not yet a completed causal-inference system**. It does not estimate causal effects with Double Machine Learning yet. That will be added after the data pipeline is verified.
