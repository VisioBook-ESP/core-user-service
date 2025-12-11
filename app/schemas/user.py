"""
Pydantic schemas for the User entity.
All required fields are truly required for creation.
Role defaults to 'user' if omitted.
"""

from typing import Annotated, Literal

from pydantic import BaseModel, EmailStr, Field

# Allowed roles for users
UserRole = Literal["admin", "user", "moderator"]


class UserBase(BaseModel):
    """Base attributes shared by in/out models (except password)."""

    email: EmailStr  # required
    username: Annotated[str, Field(min_length=3, max_length=50)]  # required
    role: UserRole = "user"  # optional, default -> "user"


class UserCreate(UserBase):
    """Payload required to create a user."""

    password: Annotated[str, Field(min_length=6)]  # required (no default)
    # Profile fields (optional)
    first_name: Annotated[str, Field(min_length=1, max_length=50)] | None = None
    last_name: Annotated[str, Field(min_length=1, max_length=50)] | None = None


class UserUpdate(BaseModel):
    """Partial update; all fields optional."""

    email: EmailStr | None = None
    username: Annotated[str, Field(min_length=3, max_length=50)] | None = None
    password: Annotated[str, Field(min_length=6)] | None = None
    role: UserRole | None = None
    first_name: Annotated[str, Field(min_length=1, max_length=50)] | None = None
    last_name: Annotated[str, Field(min_length=1, max_length=50)] | None = None


class UserOut(BaseModel):
    """Response model for user data (never includes password)."""

    id: str
    email: EmailStr
    username: str
    role: UserRole
    # Profile fields (optional)
    first_name: str | None = None
    last_name: str | None = None
