"""
Pydantic schemas for the User entity.
"""

from typing import Annotated, Literal

from pydantic import BaseModel, EmailStr, Field

# Allowed roles for users
UserRole = Literal["admin", "user", "moderator"]


class UserBase(BaseModel):
    """Base schema shared by all user models."""

    email: EmailStr
    username: Annotated[str, Field(min_length=3, max_length=50)]
    role: UserRole = "user"
    first_name: Annotated[str, Field(min_length=1, max_length=50)]
    last_name: Annotated[str, Field(min_length=1, max_length=50)]


class UserCreate(UserBase):
    """Schema for creating a new user (requires password)."""

    password: Annotated[str, Field(min_length=6)]


class UserUpdate(BaseModel):
    """Schema for updating an existing user (all fields optional)."""

    email: EmailStr | None = None
    username: Annotated[str, Field(min_length=3, max_length=50)] | None = None
    password: Annotated[str, Field(min_length=6)] | None = None
    role: UserRole | None = None
    first_name: Annotated[str, Field(min_length=1, max_length=50)] | None = None
    last_name: Annotated[str, Field(min_length=1, max_length=50)] | None = None


class UserOut(UserBase):
    """Schema for returning user data (without password)."""

    id: str
