"""add date_added to wikibase

Revision ID: d27b1993ba79
Revises: c2bbb7f8532f
Create Date: 2026-11-12 10:24:53.385916

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "d27b1993ba79"
down_revision: Union[str, Sequence[str], None] = "c2bbb7f8532f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column(
        "wikibase",
        sa.Column(
            "date_added",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
    )


def downgrade():
    op.drop_column("wikibase", "date_added")
