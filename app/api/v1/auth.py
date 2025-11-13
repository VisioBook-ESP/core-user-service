"""
Authentication endpoints with database integration.
"""

from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import create_access_token, verify_password
from app.models.user import User
from app.schemas.auth import LoginRequest, TokenResponse

router = APIRouter(prefix="/auth", tags=["Authentication"])


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
