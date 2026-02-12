"""
Security utilities for password hashing and JWT tokens.
"""

from datetime import UTC, datetime, timedelta
from typing import Any

import bcrypt
import jwt

from app.core.keys import private_key, public_key
from app.core.settings import settings


def get_password_hash(password: str) -> str:
    """Hash a password for storing in the database."""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())


def create_access_token(data: dict[str, Any], expires_delta: timedelta | None = None) -> str:
    """Create a JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(UTC) + expires_delta
    else:
        expire = datetime.now(UTC) + timedelta(minutes=settings.access_token_expire_minutes)

    to_encode.update({"exp": expire, "iss": settings.jwt_issuer})
    encoded_jwt = jwt.encode(
        to_encode,
        private_key,
        algorithm=settings.jwt_algorithm,
        headers={"kid": settings.jwt_kid},
    )
    return encoded_jwt


def verify_token(token: str) -> dict[str, Any] | None:
    """Verify and decode a JWT token."""
    try:
        payload: dict[str, Any] = jwt.decode(
            token,
            public_key,
            algorithms=[settings.jwt_algorithm],
            issuer=settings.jwt_issuer,
        )
        return payload
    except jwt.PyJWTError:
        return None
