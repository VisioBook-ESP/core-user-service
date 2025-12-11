"""
Database configuration and session management.
"""

from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.settings import settings
from app.models.base import Base

# Create database engine
engine = create_engine(
    settings.database_url,
    echo=settings.database_echo,  # Log SQL queries in development
    pool_pre_ping=True,  # Verify connections before use
    pool_recycle=300,  # Recycle connections every 5 minutes
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_tables() -> None:
    """Create all database tables. Use only in development."""
    Base.metadata.create_all(bind=engine)


def get_db() -> Generator[Session]:
    """
    Dependency to get database session.

    Usage in FastAPI endpoints:
    ```
    @app.get("/users")
    def get_users(db: Session = Depends(get_db)):
        # Use db session here
    ```
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# For direct database access (use sparingly)
def get_session() -> Session:
    """Get a database session for direct use (not in FastAPI endpoints)."""
    return SessionLocal()
