"""set_test_true_for_localhost_wikibases

Revision ID: c2bbb7f8532f
Revises: 4fc740902451
Create Date: 2026-05-18 14:24:59.956844

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "c2bbb7f8532f"
down_revision: Union[str, Sequence[str], None] = "4fc740902451"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.execute("""
        UPDATE wikibase
        SET test = True
        WHERE id IN (
            SELECT wikibase_id FROM wikibase_url u
            WHERE u.url LIKE '%localhost%'
            AND u.url_type = 'BASE_URL'
        )
    """)


def downgrade() -> None:
    pass
