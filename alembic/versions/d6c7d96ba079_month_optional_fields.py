"""Month Optional Fields

Revision ID: d6c7d96ba079
Revises: 749172173f94
Create Date: 2024-11-18 13:18:58.190822

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "d6c7d96ba079"
down_revision: Union[str, None] = "749172173f94"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table(
        "wikibase_log_observation_month", recreate="always"
    ) as batch_op:
        batch_op.add_column(
            sa.Column("first", sa.Boolean(), nullable=True),
            insert_before="first_log_date",
        )
        batch_op.alter_column("log_count", existing_type=sa.INTEGER(), nullable=True)
        batch_op.alter_column("user_count", existing_type=sa.INTEGER(), nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("wikibase_log_observation_month") as batch_op:
        batch_op.alter_column("user_count", existing_type=sa.INTEGER(), nullable=False)
        batch_op.alter_column("log_count", existing_type=sa.INTEGER(), nullable=False)
        batch_op.drop_column("first")
    # ### end Alembic commands ###