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

## Deploy the frontend on Vercel

Deploy the `frontend` folder as a static Vercel project:

1. Import this GitHub repository into Vercel.
2. Set **Root Directory** to `frontend`.
3. Leave the framework preset as **Other** and the build command empty.
4. Edit `frontend/config.js` and set `window.BRANDFORGE_API_URL` to the public URL of the deployed FastAPI backend, for example `https://brandforge-api.onrender.com`.
5. Commit that URL change and redeploy the frontend. Do not put credentials in this file.

The backend must allow the Vercel URL through its `CORS_ORIGINS` environment variable. For example:

```text
https://brandforge.vercel.app
```

Deploy the backend separately using the included Dockerfile and `render.yaml`, then copy its public URL into Vercel.
