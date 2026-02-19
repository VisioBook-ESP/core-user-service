"""
User API endpoints. Provides CRUD operations for user resources.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user, require_admin
from app.core.security import get_password_hash
from app.models.user import Profile, User, UserRole
from app.schemas.auth import TokenData
from app.schemas.user import UserCreate, UserOut, UserUpdate

router = APIRouter(prefix="/api/v1/users", tags=["users"])


@router.get("", response_model=list[UserOut])
def list_users(
    _current_user: TokenData = Depends(require_admin), db: Session = Depends(get_db)
) -> list[UserOut]:
    """Retrieve a list of users from database. (Admin only)"""
    # Query all users from database
    users = db.query(User).all()

    return [UserOut.from_model(user) for user in users]


@router.get("/me", response_model=UserOut)
def get_my_profile(
    current_user: TokenData = Depends(get_current_user),  # 🔒 Login required
    db: Session = Depends(get_db),
) -> UserOut:
    """Get the current user's profile from database."""
    if not current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user token",
        )

    # Convert string user_id back to integer for database query
    try:
        user_id = int(current_user.user_id)
    except (ValueError, TypeError) as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user token format",
        ) from exc

    # Query user from database using integer ID
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User profile not found",
        )

    return UserOut.from_model(user)


@router.put("/me", response_model=UserOut)
def update_my_profile(
    dto: UserUpdate,
    current_user: TokenData = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> UserOut:
    """Update the current user's own profile."""
    if not current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user token",
        )

    try:
        user_id = int(current_user.user_id)
    except (ValueError, TypeError) as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user token format",
        ) from exc

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    # Users cannot change their own role
    if dto.role is not None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot change your own role",
        )

    if dto.email is not None:
        user.email = dto.email
    if dto.username is not None:
        user.username = dto.username
    if dto.password is not None:
        user.password = get_password_hash(dto.password)

    if dto.first_name is not None or dto.last_name is not None:
        if not user.profile:
            user.profile = Profile(user_id=user.id)
            db.add(user.profile)
        if dto.first_name is not None:
            user.profile.first_name = dto.first_name
        if dto.last_name is not None:
            user.profile.last_name = dto.last_name

    db.commit()
    db.refresh(user)

    return UserOut.from_model(user)


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
def delete_my_account(
    current_user: TokenData = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> None:
    """Delete the current user's own account."""
    if not current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user token",
        )

    try:
        user_id = int(current_user.user_id)
    except (ValueError, TypeError) as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user token format",
        ) from exc

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    db.delete(user)
    db.commit()


@router.get("/{user_id}", response_model=UserOut)
def get_user(
    user_id: int,
    current_user: TokenData = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> UserOut:
    """Retrieve a user by ID from database. Can only view own profile or must be admin."""
    # Check authorization: must be viewing own profile OR be an admin
    if str(user_id) != current_user.user_id and "admin" not in current_user.roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view this user",
        )

    # Query user from database using integer ID
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return UserOut.from_model(user)


@router.post("", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_user(
    dto: UserCreate,
    _current_user: TokenData = Depends(require_admin),
    db: Session = Depends(get_db),
) -> UserOut:
    """Create a new user. (Admin only)"""
    # Check if user already exists
    existing_user = (
        db.query(User).filter((User.email == dto.email) | (User.username == dto.username)).first()
    )

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email or username already exists",
        )

    # Create new user with forced USER role (ignore dto.role for security)
    user = User(
        email=dto.email,
        username=dto.username,
        password=get_password_hash(dto.password),
        role=UserRole.USER,  # Always create as USER, not dto.role
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    # Create profile if first_name or last_name provided
    if dto.first_name or dto.last_name:
        profile = Profile(
            user_id=user.id,
            first_name=dto.first_name,
            last_name=dto.last_name,
        )
        db.add(profile)
        db.commit()
        db.refresh(user)  # Refresh to include profile

    return UserOut.from_model(user)


@router.put("/{user_id}", response_model=UserOut)
def update_user(
    user_id: int,
    dto: UserUpdate,
    current_user: TokenData = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> UserOut:
    """Update an existing user. Can only update own profile or must be admin."""
    # Check authorization: must be updating own profile OR be an admin
    is_own_profile = str(user_id) == current_user.user_id
    is_admin = "admin" in current_user.roles

    if not is_own_profile and not is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this user",
        )

    # Prevent users from changing their own role (only admins can change roles)
    if is_own_profile and not is_admin and dto.role is not None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot change your own role",
        )

    # Find user in database
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    # Update fields that are provided
    if dto.email is not None:
        user.email = dto.email
    if dto.username is not None:
        user.username = dto.username
    if dto.password is not None:
        user.password = get_password_hash(dto.password)
    if dto.role is not None:
        user.role = UserRole(dto.role)

    # Update profile fields if they exist
    if dto.first_name is not None or dto.last_name is not None:
        if not user.profile:
            user.profile = Profile(user_id=user.id)
            db.add(user.profile)

        if dto.first_name is not None:
            user.profile.first_name = dto.first_name
        if dto.last_name is not None:
            user.profile.last_name = dto.last_name

    db.commit()
    db.refresh(user)

    return UserOut.from_model(user)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    _current_user: TokenData = Depends(require_admin),  # 🔒 Admin only
    db: Session = Depends(get_db),
) -> None:
    """Delete a user by ID. (Admin only)"""
    # Find user in database
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    # Delete user (cascade will delete profile automatically)
    db.delete(user)
    db.commit()
