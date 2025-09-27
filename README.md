
# Stock Forecast Monorepo (Next.js + Flask + OpenBB + Prophet)

This repo contains:
- `frontend/` — Next.js 13 app (Tailwind CSS) to input a stock ticker and view a 30‑day forecast.
- `backend/` — Flask API using OpenBB SDK to fetch historical prices and Prophet to forecast.

## Quick start (local)

### Backend
```bash
cd backend
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
# serves on http://localhost:5000
```

### Frontend
```bash
cd frontend
npm install
echo "NEXT_PUBLIC_BACKEND_URL=http://localhost:5000" > .env.local
npm run dev
# open http://localhost:3000
```

## Deploy

### Backend on Render
- New Web Service → Root Directory: `backend/`
- Build Command: `pip install -r requirements.txt`
- Start Command: `gunicorn app:app --bind 0.0.0.0:$PORT`

### Frontend on Vercel
- Import project → Root Directory: `frontend/`
- Env var: `NEXT_PUBLIC_BACKEND_URL` = your Render URL (e.g. `https://your-app.onrender.com`)

## Notes
- OpenBB defaults to Yahoo Finance for equities (no API key required).
- Prophet forecasts are illustrative; do not use for investment decisions.
