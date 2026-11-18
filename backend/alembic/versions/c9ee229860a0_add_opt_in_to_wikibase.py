"""add opt_in to Wikibase

Revision ID: c9ee229860a0
Revises: c2bbb7f8532f
Create Date: 2026-11-13 12:02:15.571544

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "c9ee229860a0"
down_revision: Union[str, Sequence[str], None] = "c2bbb7f8532f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column(
        "wikibase",
        sa.Column(
            "opt_in",
            sa.Boolean(),
            nullable=False,
            server_default=sa.false(),
        ),
    )


def downgrade():
    op.drop_column("wikibase", "opt_in")
