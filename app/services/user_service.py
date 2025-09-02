"""
User service handling CRUD operations on a JSON file (mock repository).
All read operations return Pydantic models (UserOut).
"""

from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import TYPE_CHECKING, Any, List, Optional, TypedDict, cast

if TYPE_CHECKING:
    from app.schemas.user import UserOut  # local import to avoid cyclic types
    from app.schemas.user import UserCreate, UserUpdate


# Internal JSON record shape
class UserRecord(TypedDict, total=False):
    id: str
    email: str
    username: str
    # password: str
    # role: str
    first_name: str
    last_name: str
    # created_at: str
    # updated_at: str


# version: int


# Path to the JSON data file
DATA_PATH: Path = Path(__file__).resolve().parents[1] / "data" / "users.json"


# ---------------------------- IO helpers -------------------------------------


def _now_iso() -> str:
    """Return current UTC time as ISO-8601 string."""
    return datetime.now(timezone.utc).isoformat()


def _load_data() -> List[UserRecord]:
    """
    Load user data from the JSON file.

    Returns:
        A list of UserRecord objects (empty list if file missing/empty).
    """
    if not DATA_PATH.exists():
        return []
    text = DATA_PATH.read_text(encoding="utf-8").strip()
    if not text:
        return []
    data: Any = json.loads(text)
    if not isinstance(data, list):
        raise RuntimeError(f"{DATA_PATH} must contain a JSON array")
    return cast(List[UserRecord], data)


def _save_data(data: List[UserRecord]) -> None:
    """Persist the full users array atomically."""
    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    tmp = DATA_PATH.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    tmp.replace(DATA_PATH)


# ---------------------------- Read ops ---------------------------------------


def list_users() -> List["UserOut"]:
    """Return all users as Pydantic models."""

    return [UserOut(**u) for u in _load_data()]


def get_user(user_id: str) -> Optional["UserOut"]:
    """Return a user by id or None if not found."""

    for u in _load_data():
        if u.get("id") == user_id:
            return UserOut(**u)
    return None


# ---------------------------- Write ops --------------------------------------


def create_user(dto: "UserCreate") -> "UserOut":
    """
    Create and persist a new user in the JSON file.
    Note: password is kept as-is for mock purposes only.
    """
    from app.schemas.user import UserOut

    items = _load_data()
    record: UserRecord = {
        "id": f"u_{uuid.uuid4().hex[:8]}",
        "email": dto.email,
        "username": dto.username,
        # "password": dto.password,
        # "role": dto.role,
        "first_name": dto.first_name,
        "last_name": dto.last_name,
        # "created_at": _now_iso(),
        # "updated_at": _now_iso(),
        # "version": 1,
    }
    items.append(record)
    _save_data(items)
    return UserOut(**record)


def update_user(user_id: str, dto: "UserUpdate") -> Optional["UserOut"]:
    """Update an existing user, returns updated model or None if not found."""
    from app.schemas.user import UserOut

    items = _load_data()
    for u in items:
        if u.get("id") == user_id:
            # Only update provided fields
            if dto.email is not None:
                u["email"] = dto.email
            if dto.username is not None:
                u["username"] = dto.username
                # if dto.password is not None:
                #     u["password"] = dto.password
                # if dto.role is not None:
                #     u["role"] = dto.role
            if dto.first_name is not None:
                u["first_name"] = dto.first_name
            if dto.last_name is not None:
                u["last_name"] = dto.last_name

            #  u["updated_at"] = _now_iso()
            # u["version"] = int(u.get("version", 1)) + 1
            _save_data(items)
            return UserOut(**u)
    return None


def delete_user(user_id: str) -> bool:
    """Delete a user by id. Returns True if something was deleted."""
    items = _load_data()
    remaining = [u for u in items if u.get("id") != user_id]
    if len(remaining) == len(items):
        return False
    _save_data(remaining)
    return True
