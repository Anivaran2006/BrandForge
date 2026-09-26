# BrandForge AI

BrandForge AI turns a rough idea into positioning, brand definition, expression, challenge insights, a final brand system, and a practical launch plan.

## Run locally

### Backend and frontend together

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r backend\requirements.txt
uvicorn app.main:app --app-dir backend --reload
```

Open `http://127.0.0.1:8000/`.

### Run the test suite

```powershell
pytest backend\tests
```

## Deploy with Docker

```powershell
docker build -t brandforge-ai .
docker run --rm -p 8000:8000 -v brandforge-data:/app/backend/data brandforge-ai
```

The application serves the frontend and API from the same origin. Set `CORS_ORIGINS` only when a separate frontend origin is required.

## Deploy on Render

The included `render.yaml` uses the Dockerfile, exposes `/api/health` as the health check, and persists project data on a one-gigabyte disk. Set `CORS_ORIGINS` to a comma-separated list of trusted origins if needed.
