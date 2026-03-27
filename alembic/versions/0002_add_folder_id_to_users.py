"""Add folder_id column to users table.

Revision ID: 0002
Revises: 0001
Create Date: 2026-03-13

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "0002"
down_revision: str | None = "0001"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

SCHEMA = "core_user_service"


def upgrade() -> None:
    op.add_column("users", sa.Column("folder_id", sa.String(), nullable=True), schema=SCHEMA)


def downgrade() -> None:
    op.drop_column("users", "folder_id", schema=SCHEMA)
