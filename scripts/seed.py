"""Seed the database with an initial admin user."""

import logging
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.core.database import get_session
from app.core.security import get_password_hash
from app.models.user import User, UserRole

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def seed() -> None:
    """Create admin user if it does not already exist."""
    db = get_session()
    try:
        existing = db.query(User).filter(User.email == "admin@mail.com").first()
        if existing:
            logger.info("Admin user already exists, skipping seed.")
            return

        admin = User(
            email="admin@mail.com",
            username="admin",
            password=get_password_hash("Admin123456"),
            role=UserRole.ADMIN,
        )
        db.add(admin)
        db.commit()
        logger.info("Admin user created (admin@mail.com).")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
