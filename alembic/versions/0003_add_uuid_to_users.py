"""Add uuid column and remove folder_id from users table.

Revision ID: 0003
Revises: 0002
Create Date: 2026-03-26

"""

import uuid
from collections.abc import Sequence

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "0003"
down_revision: str | None = "0002"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

SCHEMA = "core_user_service"


def upgrade() -> None:
    # Add uuid column as nullable first
    op.add_column(
        "users",
        sa.Column("uuid", UUID(as_uuid=True), nullable=True),
        schema=SCHEMA,
    )

    # Backfill existing rows with generated UUIDs
    users_table = sa.table(
        "users",
        sa.column("id", sa.Integer),
        sa.column("uuid", UUID(as_uuid=True)),
        schema=SCHEMA,
    )
    conn = op.get_bind()
    rows = conn.execute(sa.select(users_table.c.id)).fetchall()
    for row in rows:
        conn.execute(
            users_table.update().where(users_table.c.id == row.id).values(uuid=uuid.uuid4())
        )

    # Make column non-nullable and add unique index
    op.alter_column("users", "uuid", nullable=False, schema=SCHEMA)
    op.create_index("ix_users_uuid", "users", ["uuid"], unique=True, schema=SCHEMA)

    # Remove folder_id column (no longer managed by this service)
    op.drop_column("users", "folder_id", schema=SCHEMA)


def downgrade() -> None:
    op.add_column("users", sa.Column("folder_id", sa.String(), nullable=True), schema=SCHEMA)
    op.drop_index("ix_users_uuid", table_name="users", schema=SCHEMA)
    op.drop_column("users", "uuid", schema=SCHEMA)
