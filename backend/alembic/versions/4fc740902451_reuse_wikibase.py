"""Reuse Wikibase

Revision ID: 4fc740902451
Revises: 67a5973d5ef4
Create Date: 2026-05-07 06:01:24.241374

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "4fc740902451"
down_revision: Union[str, Sequence[str], None] = "67a5973d5ef4"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    with op.batch_alter_table("wikibase") as batch_op:
        batch_op.add_column(sa.Column("reuse", sa.Boolean(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table("wikibase") as batch_op:
        batch_op.drop_column("reuse")
