"""optional

Revision ID: a168eb215de7
Revises: 93d8f0a13a14
Create Date: 2024-06-26 16:46:02.943210

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "a168eb215de7"
down_revision: Union[str, None] = "93d8f0a13a14"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("wikibase") as batch_op:
        batch_op.alter_column("base_url", existing_type=sa.VARCHAR(), nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("wikibase") as batch_op:
        batch_op.alter_column("base_url", existing_type=sa.VARCHAR(), nullable=False)
    # ### end Alembic commands ###
