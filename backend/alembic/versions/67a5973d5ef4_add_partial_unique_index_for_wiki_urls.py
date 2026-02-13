"""add partial unique index for wiki urls

Revision ID: 67a5973d5ef4
Revises: 88914015098c
Create Date: 2026-02-13 09:18:35.896878

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '67a5973d5ef4'
down_revision: Union[str, Sequence[str], None] = '88914015098c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_index(
        "unique_wikibase_url",
        "wikibase_url",
        ["url"],
        unique=True,
        postgresql_where=sa.text(
            "url_type NOT IN ('ARTICLE_PATH', 'SCRIPT_PATH')"
        ),
    )


def downgrade():
    op.drop_index("unique_wikibase_url", table_name="wikibase_url")
