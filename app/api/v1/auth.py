"""
Authentication endpoints with database integration.
"""

from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.keys import get_jwks
from app.core.security import create_access_token, get_password_hash, verify_password
from app.models.user import Profile, User, UserRole
from app.schemas.auth import LoginRequest, TokenResponse
from app.schemas.user import UserCreate, UserOut

router = APIRouter(prefix="/api/v1/auth", tags=["Authentication"])


@router.post("/login", response_model=TokenResponse)
async def login(credentials: LoginRequest, db: Session = Depends(get_db)) -> TokenResponse:
    """
    Authenticate user against database and return JWT token.

    This authenticates against real users stored in the database.
    Password verification uses bcrypt hashing.
    """
    # Find user by email in database
    user = db.query(User).filter(User.email == credentials.email).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou mot de passe incorrect",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Verify password using bcrypt
    if not verify_password(credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou mot de passe incorrect",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create JWT token with user data
    token_data = {
        "sub": str(user.id),  # Subject (user ID)
        "email": user.email,
        "role": user.role.value,  # Convert enum to string
    }

    # Token expires in 24 hours
    access_token = create_access_token(data=token_data, expires_delta=timedelta(hours=24))

    return TokenResponse(
        access_token=access_token,
        expires_in=24 * 3600,  # 24 hours in seconds
        user_id=str(user.id),
        role=user.role.value,
    )


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def register(dto: UserCreate, db: Session = Depends(get_db)) -> UserOut:
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

    return UserOut.from_model(user)


@router.get("/.well-known/jwks.json")
async def jwks() -> dict[str, Any]:
    """Expose the public RSA key for JWT token verification."""
    return get_jwks()
