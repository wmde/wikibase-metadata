"""make url unique

Revision ID: 2f06bfe50128
Revises: 88914015098c
Create Date: 2026-02-10 19:08:41.971923

"""
from typing import Sequence, Union
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '2f06bfe50128'
down_revision: Union[str, Sequence[str], None] = '88914015098c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("""
        DELETE FROM wikibase_url a
        USING wikibase_url b
        WHERE a.url = b.url
          AND a.id > b.id;
    """)

    op.create_unique_constraint('unique_wikibase_url', 'wikibase_url', ['url'])

def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint('unique_wikibase_url', 'wikibase_url', type_='unique')
