"""lexemes

Revision ID: dca971dbdd41
Revises: 3078a807f9fa
Create Date: 2024-06-19 15:57:52.388232

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "dca971dbdd41"
down_revision: Union[str, None] = "3078a807f9fa"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "wikibase_quantity_observation",
        sa.Column("total_lexemes", sa.Integer(), nullable=True),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("wikibase_quantity_observation", "total_lexemes")
    # ### end Alembic commands ###
