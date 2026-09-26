from fastapi import APIRouter, Header, HTTPException, status

from app.schemas.auth_schemas import LoginRequest, SignupRequest
from app.services.auth_service import AuthService

router = APIRouter()
service = AuthService()


@router.post("/api/auth/signup", status_code=status.HTTP_201_CREATED)
def signup(payload: SignupRequest):
    try:
        return service.signup(payload.name, payload.email, payload.password)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc


@router.post("/api/auth/login")
def login(payload: LoginRequest):
    try:
        return service.login(payload.email, payload.password)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc)) from exc


@router.get("/api/auth/me")
def me(authorization: str | None = Header(default=None)):
    token = authorization.removeprefix("Bearer ").strip() if authorization else None
    try:
        return {"user": service.get_user_from_token(token)}
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc)) from exc
