"""
Pydantic schemas for the User entity.
All required fields are truly required for creation.
Role defaults to 'user' if omitted.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Annotated, Literal

from pydantic import BaseModel, EmailStr, Field

if TYPE_CHECKING:
    from app.models.user import User

# Allowed roles for users
UserRole = Literal["admin", "user"]


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

    @classmethod
    def from_model(cls, user: User) -> UserOut:
        """Build a UserOut from a SQLAlchemy User model."""
        return cls(
            id=str(user.id),
            email=user.email,
            username=user.username,
            role=user.role.value,
            first_name=user.profile.first_name if user.profile else None,
            last_name=user.profile.last_name if user.profile else None,
        )
