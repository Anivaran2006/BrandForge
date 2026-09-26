from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.api.routes.health import router as health_router
from app.api.routes.auth import router as auth_router
from app.api.routes.projects import router as projects_router
from app.core.config import APP_TITLE, APP_ENV, CORS_ORIGINS, FRONTEND_DIR

app = FastAPI(title=APP_TITLE, version='0.1.0', description='BrandForge AI workflow backend')

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=False,
    allow_methods=['GET', 'POST', 'PUT'],
    allow_headers=['Content-Type', 'Authorization'],
)

app.include_router(health_router)
app.include_router(auth_router)
app.include_router(projects_router)


@app.get('/')
def root():
    frontend_index = FRONTEND_DIR / 'index.html'
    if frontend_index.exists():
        return FileResponse(frontend_index)
    return {'message': APP_TITLE, 'environment': APP_ENV}


if FRONTEND_DIR.exists():
    app.mount('/', StaticFiles(directory=FRONTEND_DIR), name='frontend')
