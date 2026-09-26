import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

PROJECTS_FILE = DATA_DIR / "projects.json"
USERS_FILE = DATA_DIR / "users.json"

APP_TITLE = os.getenv("APP_TITLE", "BrandForge AI")
APP_ENV = os.getenv("APP_ENV", "development")
API_TIMEOUT_SECONDS = float(os.getenv("API_TIMEOUT_SECONDS", "20"))
CORS_ORIGINS = [
    origin.strip()
    for origin in os.getenv(
        "CORS_ORIGINS",
        "http://localhost:8001,http://127.0.0.1:8001,"
        "https://brand-forge-gilt.vercel.app",
    ).split(",")
    if origin.strip()
]
FRONTEND_DIR = BASE_DIR.parent / "frontend"
