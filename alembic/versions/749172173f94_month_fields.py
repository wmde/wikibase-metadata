"""Month Fields

Revision ID: 749172173f94
Revises: ced691eaf66e
Create Date: 2024-11-18 10:59:19.124446

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "749172173f94"
down_revision: Union[str, None] = "ced691eaf66e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###

    with op.batch_alter_table(
        "wikibase_log_observation_month", recreate="always"
    ) as batch_op:
        batch_op.add_column(
            sa.Column("wikibase_id", sa.Integer(), nullable=True),
            insert_before="first_log_date",
        )
        batch_op.add_column(
            sa.Column("anything", sa.Boolean(), nullable=True),
            insert_before="first_log_date",
        )
        batch_op.add_column(
            sa.Column("date", sa.DateTime(timezone=True), nullable=True),
            insert_before="first_log_date",
        )
        batch_op.add_column(
            sa.Column(
                "last_log_user_type",
                sa.Enum("BOT", "MISSING", "USER", "NONE", name="wikibaseusertype"),
                nullable=True,
            ),
            insert_after="last_log_date",
        )
        batch_op.create_foreign_key(
            "observation_wikibase", "wikibase", ["wikibase_id"], ["id"]
        )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("wikibase_log_observation_month") as batch_op:
        batch_op.drop_constraint("observation_wikibase", type_="foreignkey")
        batch_op.drop_column("last_log_user_type")
        batch_op.drop_column("date")
        batch_op.drop_column("anything")
        batch_op.drop_column("wikibase_id")
    # ### end Alembic commands ###
