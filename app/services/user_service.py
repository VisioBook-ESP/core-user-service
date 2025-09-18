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
    # Only for typing; avoid top-level import cycles at runtime
    from app.schemas.user import UserCreate, UserOut, UserRole, UserUpdate


# Internal JSON record shape stored in users.json
class UserRecord(TypedDict, total=False):
    id: str
    email: str
    username: str
    password: str
    role: str
    first_name: str
    last_name: str
    # created_at: str
    # updated_at: str
    # version: int


# Path to the JSON data file (app/data/users.json)
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


# ---------------------------- Mapping helpers --------------------------------


def _ensure_literal_role(value: str | None) -> "UserRole":
    """
    Coerce arbitrary string to allowed literal role ('admin'|'user'|'moderator'),
    defaulting to 'user' if missing/invalid.
    """
    raw = (value or "user").lower()
    if raw not in {"admin", "user", "moderator"}:
        raw = "user"
    return cast("UserRole", raw)


def _to_user_out(u: UserRecord) -> "UserOut":
    """
    Map a raw dict (from JSON file) to the public UserOut model.
    Import is deferred to avoid import cycles; never expose password.
    """
    # Import at runtime only when needed to avoid cycles
    from app.schemas.user import UserOut  # pylint: disable=import-outside-toplevel

    return UserOut(
        id=u["id"],
        email=u["email"],
        username=u["username"],
        role=_ensure_literal_role(u.get("role")),
        first_name=u["first_name"],
        last_name=u["last_name"],
    )


# ---------------------------- Read ops ---------------------------------------


def list_users() -> List["UserOut"]:
    """Return all users as Pydantic models."""
    return [_to_user_out(u) for u in _load_data()]


def get_user(user_id: str) -> Optional["UserOut"]:
    """Return a user by id or None if not found."""
    for u in _load_data():
        if u.get("id") == user_id:
            return _to_user_out(u)
    return None


# ---------------------------- Write ops --------------------------------------


def create_user(dto: "UserCreate") -> "UserOut":
    """
    Create and persist a new user in the JSON file.
    Note: password is kept as-is for mock purposes only.
    """
    items = _load_data()
    record: UserRecord = {
        "id": f"u_{uuid.uuid4().hex[:8]}",
        "email": dto.email,
        "username": dto.username,
        "password": dto.password,  # stored in clear only for the mock
        "role": dto.role or "user",  # default to 'user' if omitted
        "first_name": dto.first_name,
        "last_name": dto.last_name,
        # "created_at": _now_iso(),
        # "updated_at": _now_iso(),
        # "version": 1,
    }
    items.append(record)
    _save_data(items)
    return _to_user_out(record)


def update_user(user_id: str, dto: "UserUpdate") -> Optional["UserOut"]:
    """Update an existing user, returns updated model or None if not found."""
    items = _load_data()
    for u in items:
        if u.get("id") == user_id:
            # Only update provided fields
            if dto.email is not None:
                u["email"] = dto.email
            if dto.username is not None:
                u["username"] = dto.username
            if dto.password is not None:
                u["password"] = dto.password
            if dto.role is not None:
                u["role"] = dto.role
            if dto.first_name is not None:
                u["first_name"] = dto.first_name
            if dto.last_name is not None:
                u["last_name"] = dto.last_name

            # u["updated_at"] = _now_iso()
            # u["version"] = int(u.get("version", 1)) + 1
            _save_data(items)
            return _to_user_out(u)
    return None


def delete_user(user_id: str) -> bool:
    """Delete a user by id. Returns True if something was deleted."""
    items = _load_data()
    remaining = [u for u in items if u.get("id") != user_id]
    if len(remaining) == len(items):
        return False
    _save_data(remaining)
    return True
