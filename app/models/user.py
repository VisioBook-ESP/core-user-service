"""
User and profile models.
"""

from __future__ import annotations

import enum

from sqlalchemy import Enum, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseModel


class UserRole(enum.Enum):
    """User role enumeration."""

    USER = "user"
    ADMIN = "admin"
    MODERATOR = "moderator"


class User(BaseModel):
    """
    User model representing a user account.

    Each user can have one profile with additional information.
    """

    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String, unique=True, nullable=False, index=True)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False, index=True)
    password: Mapped[str] = mapped_column(String, nullable=False)  # Hashed password
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), default=UserRole.USER, nullable=False)

    # Relations
    profile: Mapped[Profile | None] = relationship(
        "Profile", back_populates="user", uselist=False, cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<User(email='{self.email}', username='{self.username}')>"


class Profile(BaseModel):
    """
    User profile model with additional user information.

    Each profile belongs to exactly one user.
    """

    __tablename__ = "profiles"

    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), unique=True, nullable=False
    )
    first_name: Mapped[str | None] = mapped_column(String, nullable=True)
    last_name: Mapped[str | None] = mapped_column(String, nullable=True)
    avatar: Mapped[str | None] = mapped_column(String, nullable=True)  # URL to avatar image
    bio: Mapped[str | None] = mapped_column(String, nullable=True)

    # Relations
    user: Mapped[User] = relationship("User", back_populates="profile")

    def __repr__(self) -> str:
        return f"<Profile(user_id={self.user_id}, name='{self.first_name} {self.last_name}')>"

    @property
    def full_name(self) -> str:
        """Get the full name combining first and last names."""
        parts: list[str] = []
        if self.first_name:
            parts.append(self.first_name)
        if self.last_name:
            parts.append(self.last_name)
        return " ".join(parts) if parts else ""
