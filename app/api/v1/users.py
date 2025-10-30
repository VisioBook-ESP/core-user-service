"""
User API endpoints. Provides CRUD operations for user resources.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user, require_admin
from app.models.user import User
from app.schemas.auth import TokenData
from app.schemas.user import UserCreate, UserOut, UserUpdate
from app.services import user_service

router = APIRouter(prefix="/api/v1/users", tags=["users"])


@router.get("/", response_model=list[UserOut])
def list_users(db: Session = Depends(get_db)) -> list[UserOut]:
    """Retrieve a list of users from database."""
    # Query all users from database
    users = db.query(User).all()
    
    # Convert database models to response schemas
    return [
        UserOut(
            id=str(user.id),  # Convert int to string for API compatibility
            email=user.email,
            username=user.username,
            role=user.role.value,
            first_name=user.profile.first_name if user.profile else None,
            last_name=user.profile.last_name if user.profile else None,
        )
        for user in users
    ]


@router.get("/me", response_model=UserOut)
def get_my_profile(
    current_user: TokenData = Depends(get_current_user),  # 🔒 Login required
    db: Session = Depends(get_db)
) -> UserOut:
    """Get the current user's profile from database."""
    if not current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user token",
        )
    
    # Convert string user_id back to integer for database query
    user_id = int(current_user.user_id)
    
    # Query user from database using integer ID
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User profile not found",
        )
    
    # Convert database model to response schema
    return UserOut(
        id=str(user.id),
        email=user.email,
        username=user.username,
        role=user.role.value,
        first_name=user.profile.first_name if user.profile else None,
        last_name=user.profile.last_name if user.profile else None,
    )


@router.get("/{user_id}", response_model=UserOut)
def get_user(
    user_id: int,
    db: Session = Depends(get_db)
) -> UserOut:
    """Retrieve a user by ID from database."""
    # Query user from database using integer ID
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    
    # Convert database model to response schema
    return UserOut(
        id=str(user.id),
        email=user.email,
        username=user.username,
        role=user.role.value,
        first_name=user.profile.first_name if user.profile else None,
        last_name=user.profile.last_name if user.profile else None,
    )


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
def delete_user(
    user_id: str,
    current_user: TokenData = Depends(require_admin)  # 🔒 Admin only
) -> None:
    """Delete a user by ID. (Admin only)"""
    ok = user_service.delete_user(user_id)
    if not ok:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
