"""
Authentication schemas for request/response validation.
"""

from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
    """Schema for user login requests."""

    email: EmailStr
    password: str

    class Config:
        """Pydantic configuration."""

        json_schema_extra = {
            "example": {
                "email": "admin@visiobook.com",
                "password": "admin123"
            }
        }


class TokenResponse(BaseModel):
    """Schema for JWT token response."""

    access_token: str
    token_type: str = "bearer"
    expires_in: int  # Duration in seconds
    user_id: str
    role: str

    class Config:
        """Pydantic configuration."""

        json_schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
                "expires_in": 86400,
                "user_id": "user_001",
                "role": "admin"
            }
        }


class TokenData(BaseModel):
    """Schema for JWT token payload data."""

    user_id: str | None = None
    email: str | None = None
    role: str | None = None

    class Config:
        """Pydantic configuration."""

        json_schema_extra = {
            "example": {
                "user_id": "user_001",
                "email": "admin@visiobook.com",
                "role": "admin"
            }
        }