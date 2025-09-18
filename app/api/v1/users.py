"""
User API endpoints. Provides CRUD operations for user resources.
"""

from typing import List

from fastapi import APIRouter, HTTPException, status

from app.schemas.user import UserCreate, UserOut, UserUpdate
from app.services import user_service

router = APIRouter(prefix="/api/v1/users", tags=["users"])


@router.get("/", response_model=List[UserOut])
def list_users() -> List[UserOut]:
    """Retrieve a list of users."""
    return user_service.list_users()


@router.get("/{user_id}", response_model=UserOut)
def get_user(user_id: str) -> UserOut:
    """Retrieve a user by ID."""
    user = user_service.get_user(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user


@router.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_user(dto: UserCreate) -> UserOut:
    """Create a new user."""
    return user_service.create_user(dto)


@router.put("/{user_id}", response_model=UserOut)
def update_user(user_id: str, dto: UserUpdate) -> UserOut:
    """Update an existing user."""
    updated = user_service.update_user(user_id, dto)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return updated


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: str) -> None:
    """Delete a user by ID."""
    ok = user_service.delete_user(user_id)
    if not ok:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
