"""
Authentication endpoints with database integration.
"""

import logging
from datetime import UTC, datetime, timedelta
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.core.keys import get_jwks
from app.core.security import (
    create_access_token,
    generate_refresh_token,
    get_password_hash,
    get_refresh_token_expiry,
    verify_password,
)
from app.models.refresh_token import RefreshToken
from app.models.user import Profile, User, UserRole
from app.schemas.auth import LoginRequest, RefreshRequest, TokenData, TokenResponse
from app.schemas.user import RegisterOut, RegisterRequest

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/auth", tags=["Authentication"])


def _create_tokens(user: User, db: Session) -> TokenResponse:
    """Create access and refresh tokens for a user."""
    token_data = {"sub": str(user.uuid)}
    access_token = create_access_token(data=token_data, expires_delta=timedelta(hours=1))

    refresh_token_str = generate_refresh_token()
    refresh_token = RefreshToken(
        token=refresh_token_str,
        user_id=user.id,
        expires_at=get_refresh_token_expiry(),
    )
    db.add(refresh_token)
    db.commit()

    return TokenResponse(access_token=access_token, refresh_token=refresh_token_str)


@router.post("/login", response_model=TokenResponse)
async def login(credentials: LoginRequest, db: Session = Depends(get_db)) -> TokenResponse:
    """
    Authenticate user and return access + refresh tokens.

    Access token: short-lived (1h). Refresh token: long-lived (7d).
    """
    user = db.query(User).filter(User.email == credentials.email).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou mot de passe incorrect",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not verify_password(credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou mot de passe incorrect",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return _create_tokens(user, db)


@router.post("/refresh", response_model=TokenResponse)
async def refresh(body: RefreshRequest, db: Session = Depends(get_db)) -> TokenResponse:
    """
    Exchange a valid refresh token for a new access token + refresh token.

    The old refresh token is revoked (rotation).
    """
    token_row = db.query(RefreshToken).filter(RefreshToken.token == body.refresh_token).first()

    if not token_row or token_row.revoked or token_row.expires_at < datetime.now(UTC):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token invalide ou expiré",
        )

    # Revoke the old refresh token
    token_row.revoked = True
    db.flush()

    user = db.query(User).filter(User.id == token_row.user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Utilisateur introuvable",
        )

    return _create_tokens(user, db)


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(
    body: RefreshRequest,
    db: Session = Depends(get_db),
    _current_user: TokenData = Depends(get_current_user),
) -> None:
    """Revoke the provided refresh token."""
    token_row = db.query(RefreshToken).filter(RefreshToken.token == body.refresh_token).first()

    if token_row and not token_row.revoked:
        token_row.revoked = True
        db.commit()


@router.post("/register", response_model=RegisterOut, status_code=status.HTTP_201_CREATED)
async def register(dto: RegisterRequest, db: Session = Depends(get_db)) -> RegisterOut:
    """Register a new user. Always creates with 'user' role."""
    existing_user = (
        db.query(User).filter((User.email == dto.email) | (User.username == dto.username)).first()
    )
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email or username already exists",
        )

    user = User(
        email=dto.email,
        username=dto.username,
        password=get_password_hash(dto.password),
        role=UserRole.USER,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    if dto.first_name or dto.last_name:
        profile = Profile(user_id=user.id, first_name=dto.first_name, last_name=dto.last_name)
        db.add(profile)
        db.commit()
        db.refresh(user)

    return RegisterOut.from_model(user)


@router.get("/.well-known/jwks.json")
async def jwks() -> dict[str, Any]:
    """Expose the public RSA key for JWT token verification."""
    return get_jwks()
