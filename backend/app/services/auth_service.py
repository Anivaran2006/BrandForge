from __future__ import annotations

import base64
import hashlib
import hmac
import json
import secrets
from datetime import datetime, timezone
from typing import Any, Dict
from uuid import uuid4

from app.core.config import USERS_FILE


class AuthService:
    def _load(self) -> Dict[str, Dict[str, Any]]:
        if not USERS_FILE.exists():
            return {}
        try:
            with USERS_FILE.open("r", encoding="utf-8") as file:
                data = json.load(file)
            return data if isinstance(data, dict) else {}
        except json.JSONDecodeError:
            return {}

    def _save(self, users: Dict[str, Dict[str, Any]]) -> None:
        temporary_file = USERS_FILE.with_suffix(".tmp")
        with temporary_file.open("w", encoding="utf-8") as file:
            json.dump(users, file, indent=2)
        temporary_file.replace(USERS_FILE)

    @staticmethod
    def _normalize_email(email: str) -> str:
        return email.strip().lower()

    @staticmethod
    def _hash_password(password: str, salt: bytes | None = None) -> str:
        salt = salt or secrets.token_bytes(16)
        digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 120_000)
        return f"{base64.urlsafe_b64encode(salt).decode()}${base64.urlsafe_b64encode(digest).decode()}"

    @classmethod
    def _verify_password(cls, password: str, stored: str) -> bool:
        try:
            salt_value, digest_value = stored.split("$", 1)
            salt = base64.urlsafe_b64decode(salt_value.encode())
            expected = cls._hash_password(password, salt).split("$", 1)[1]
            return hmac.compare_digest(expected, digest_value)
        except (ValueError, TypeError):
            return False

    def signup(self, name: str, email: str, password: str) -> Dict[str, Any]:
        email = self._normalize_email(email)
        users = self._load()
        if email in users:
            raise ValueError("An account with this email already exists")
        user = {
            "user_id": str(uuid4()),
            "name": name.strip(),
            "email": email,
            "password_hash": self._hash_password(password),
            "created_at": datetime.now(timezone.utc).isoformat(),
            "sessions": {},
        }
        users[email] = user
        self._save(users)
        return self._create_session(user, users)

    def login(self, email: str, password: str) -> Dict[str, Any]:
        users = self._load()
        user = users.get(self._normalize_email(email))
        if not user or not self._verify_password(password, user.get("password_hash", "")):
            raise ValueError("Invalid email or password")
        return self._create_session(user, users)

    def _create_session(self, user: Dict[str, Any], users: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
        token = secrets.token_urlsafe(32)
        user.setdefault("sessions", {})[token] = datetime.now(timezone.utc).isoformat()
        self._save(users)
        return {"access_token": token, "token_type": "bearer", "user": self.public_user(user)}

    def get_user_from_token(self, token: str | None) -> Dict[str, Any]:
        if not token:
            raise ValueError("Authentication required")
        users = self._load()
        for user in users.values():
            if token in user.get("sessions", {}):
                return self.public_user(user)
        raise ValueError("Invalid or expired session")

    @staticmethod
    def public_user(user: Dict[str, Any]) -> Dict[str, Any]:
        return {"user_id": user["user_id"], "name": user["name"], "email": user["email"]}
