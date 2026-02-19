"""
Authentication schemas for request/response validation.
"""

from pydantic import BaseModel, ConfigDict, EmailStr


class LoginRequest(BaseModel):
    """Schema for user login requests."""

    model_config = ConfigDict(
        json_schema_extra={"example": {"email": "admin@visiobook.com", "password": "admin123"}}
    )

    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    """Schema for JWT token response."""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...",
            }
        }
    )

    access_token: str


class TokenData(BaseModel):
    """Schema for JWT token payload data."""

    model_config = ConfigDict(
        json_schema_extra={"example": {"user_id": "1", "roles": ["admin", "user"]}}
    )

    user_id: str | None = None
    roles: list[str] = []
