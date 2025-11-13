"""
New SQLAlchemy-based user service.
This will replace the JSON-based user_service.py
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.security import get_password_hash, verify_password
from app.models.user import Profile, User

if TYPE_CHECKING:
    from app.schemas.user import UserCreate, UserOut, UserUpdate


class DatabaseUserService:
    """
    SQLAlchemy-based user service.

    Handles CRUD operations for users and profiles using a database.
    """

    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user_data: UserCreate) -> UserOut:
        """Create a new user with optional profile data."""
        try:
            # Hash password
            hashed_password = get_password_hash(user_data.password)

            # Create user
            db_user = User(
                email=user_data.email,
                username=user_data.username,
                password=hashed_password,
                role=user_data.role or "user",  # Default role
            )

            self.db.add(db_user)
            self.db.flush()  # Get user ID without committing

            # Create profile if data provided
            if user_data.first_name or user_data.last_name:
                db_profile = Profile(
                    user_id=db_user.id,
                    first_name=user_data.first_name,
                    last_name=user_data.last_name,
                )
                self.db.add(db_profile)

            self.db.commit()
            self.db.refresh(db_user)

            return self._to_user_out(db_user)

        except IntegrityError as e:
            self.db.rollback()
            error_message = str(e.orig).lower()
            if "email" in error_message:
                raise HTTPException(status_code=400, detail="Email already exists") from e
            if "username" in error_message:
                raise HTTPException(status_code=400, detail="Username already exists") from e
            raise HTTPException(status_code=400, detail="User creation failed") from e

    def get_user(self, user_id: str) -> UserOut | None:
        """Get a user by ID."""
        db_user = self.db.query(User).filter(User.id == user_id).first()
        if not db_user:
            return None
        return self._to_user_out(db_user)

    def get_user_by_email(self, email: str) -> UserOut | None:
        """Get a user by email."""
        db_user = self.db.query(User).filter(User.email == email).first()
        if not db_user:
            return None
        return self._to_user_out(db_user)

    def get_user_by_username(self, username: str) -> UserOut | None:
        """Get a user by username."""
        db_user = self.db.query(User).filter(User.username == username).first()
        if not db_user:
            return None
        return self._to_user_out(db_user)

    def list_users(self) -> list[UserOut]:
        """Get all users."""
        db_users = self.db.query(User).all()
        return [self._to_user_out(user) for user in db_users]

    def update_user(self, user_id: str, user_data: UserUpdate) -> UserOut | None:
        """Update an existing user."""
        db_user = self.db.query(User).filter(User.id == user_id).first()
        if not db_user:
            return None

        try:
            # Update user fields
            update_data = user_data.model_dump(exclude_unset=True)

            # Handle password separately (needs hashing)
            if "password" in update_data:
                update_data["password"] = get_password_hash(update_data["password"])

            # Update user model
            for field, value in update_data.items():
                if hasattr(db_user, field) and field not in ["first_name", "last_name"]:
                    setattr(db_user, field, value)

            # Update profile if profile data provided
            profile_fields = {"first_name", "last_name"}
            profile_data = {k: v for k, v in update_data.items() if k in profile_fields}

            if profile_data:
                if not db_user.profile:
                    # Create profile if it doesn't exist
                    db_profile = Profile(user_id=db_user.id, **profile_data)
                    self.db.add(db_profile)
                else:
                    # Update existing profile
                    for field, value in profile_data.items():
                        setattr(db_user.profile, field, value)

            # Increment version for optimistic locking
            db_user.version += 1

            self.db.commit()
            self.db.refresh(db_user)

            return self._to_user_out(db_user)

        except IntegrityError as e:
            self.db.rollback()
            error_message = str(e.orig).lower()
            if "email" in error_message:
                raise HTTPException(status_code=400, detail="Email already exists") from e
            if "username" in error_message:
                raise HTTPException(status_code=400, detail="Username already exists") from e
            raise HTTPException(status_code=400, detail="User update failed") from e

    def delete_user(self, user_id: str) -> bool:
        """Delete a user by ID."""
        db_user = self.db.query(User).filter(User.id == user_id).first()
        if not db_user:
            return False

        self.db.delete(db_user)  # Cascade will delete profile
        self.db.commit()
        return True

    def authenticate_user(self, email: str, password: str) -> UserOut | None:
        """Authenticate a user by email and password."""
        db_user = self.db.query(User).filter(User.email == email).first()
        if not db_user:
            return None

        if not verify_password(password, db_user.password):
            return None

        return self._to_user_out(db_user)

    def _to_user_out(self, db_user: User) -> UserOut:
        """Convert a database User model to UserOut schema."""
        # Import at runtime to avoid cycles
        from app.schemas.user import UserOut  # pylint: disable=import-outside-toplevel

        return UserOut(
            id=str(db_user.id),
            email=db_user.email,
            username=db_user.username,
            role=db_user.role.value,  # Convert enum to string
            first_name=db_user.profile.first_name if db_user.profile else None,
            last_name=db_user.profile.last_name if db_user.profile else None,
        )
