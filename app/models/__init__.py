"""
Models package initialization.
Imports all models for SQLAlchemy to register them.
"""

from .base import BaseModel
from .user import Profile, User, UserRole

__all__ = ["BaseModel", "User", "Profile", "UserRole"]
