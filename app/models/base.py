"""
Base model with common fields for all database models.
"""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, Integer, MetaData, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

SCHEMA_NAME = "core_user_service"


class Base(DeclarativeBase):
    """Base class for all database models."""

    metadata = MetaData(schema=SCHEMA_NAME)


class BaseModel(Base):
    """
    Abstract base class for all database models.

    Provides common fields:
    - id: Integer primary key (auto-increment)
    - created_at: Timestamp when record was created
    - updated_at: Timestamp when record was last updated
    - version: Version number for optimistic locking
    """

    __abstract__ = True

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    created_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), server_default=text("CURRENT_TIMESTAMP")
    )
    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), onupdate=text("CURRENT_TIMESTAMP")
    )
    version: Mapped[int] = mapped_column(Integer, default=1)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}(id={self.id})>"
