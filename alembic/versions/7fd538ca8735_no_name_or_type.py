"""No Name or Type

Revision ID: 7fd538ca8735
Revises: bf635fa3a7ce
Create Date: 2024-10-17 00:13:58.311963

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "7fd538ca8735"
down_revision: Union[str, None] = "bf635fa3a7ce"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("wikibase_software_version") as batch_op:
        batch_op.drop_constraint(
            "unique_observation_software_type_name", type_="unique"
        )
        batch_op.create_unique_constraint(
            "unique_observation_software_id",
            ["wikibase_software_version_observation_id", "wikibase_software_id"],
        )
        batch_op.drop_column("software_type")
        batch_op.drop_column("software_name")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("wikibase_software_version") as batch_op:
        batch_op.add_column(sa.Column("software_name", sa.VARCHAR(), nullable=False))
        batch_op.add_column(
            sa.Column("software_type", sa.VARCHAR(length=9), nullable=False)
        )
        batch_op.drop_constraint("unique_observation_software_id", type_="unique")
        batch_op.create_unique_constraint(
            "unique_observation_software_type_name",
            [
                "wikibase_software_version_observation_id",
                "software_type",
                "software_name",
            ],
        )
    # ### end Alembic commands ###