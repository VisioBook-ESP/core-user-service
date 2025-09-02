"""
User service handling CRUD operations on JSON file (mock repository).
"""

from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from app.schemas.user import UserCreate, UserOut, UserUpdate

# Path to the JSON data file
DATA_PATH: Path = Path(__file__).resolve().parents[1] / "data" / "users.json"


def _load_data() -> list[dict[str, Any]]:
    """Load user data from the JSON file."""
    if not DATA_PATH.exists():
        return []
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def _save_data(data: list[dict[str, Any]]) -> None:
    """Save user data back to the JSON file."""
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def list_users() -> list["UserOut"]:
    """Return all users."""
    return _load_data()


def get_user(user_id: str) -> dict[str, Any] | None:
    """Retrieve a single user by ID."""
    users = _load_data()
    return next((u for u in users if u["id"] == user_id), None)


def create_user(dto: "UserCreate") -> dict[str, Any]:
    """Create a new user and save it to JSON."""
    users = _load_data()
    new_user = dto.dict()
    new_user["id"] = str(uuid.uuid4())
    new_user["created_at"] = datetime.now(timezone.utc).isoformat()
    new_user["updated_at"] = new_user["created_at"]
    users.append(new_user)
    _save_data(users)
    return new_user


def update_user(user_id: str, dto: "UserUpdate") -> dict[str, Any] | None:
    """Update an existing user."""
    users = _load_data()
    for user in users:
        if user["id"] == user_id:
            update_data = dto.dict(exclude_unset=True)
            user.update(update_data)
            user["updated_at"] = datetime.now(timezone.utc).isoformat()
            _save_data(users)
            return user
    return None


def delete_user(user_id: str) -> bool:
    """Delete a user by ID."""
    users = _load_data()
    new_users = [u for u in users if u["id"] != user_id]
    if len(new_users) == len(users):
        return False
    _save_data(new_users)
    return True
