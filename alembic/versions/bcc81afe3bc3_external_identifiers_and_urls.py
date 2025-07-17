"""external identifiers and urls

Revision ID: bcc81afe3bc3
Revises: 215716d3ef0e
Create Date: 2025-07-01 16:26:53.381242

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "bcc81afe3bc3"
down_revision: Union[str, None] = "215716d3ef0e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table("wikibase_quantity_observation") as batch_op:
        batch_op.add_column(
            sa.Column(
                "total_external_identifier_properties", sa.Integer(), nullable=True
            ),
        )
        batch_op.add_column(
            sa.Column(
                "total_external_identifier_statements", sa.Integer(), nullable=True
            ),
        )
        batch_op.add_column(
            sa.Column("total_url_properties", sa.Integer(), nullable=True),
        )
        batch_op.add_column(
            sa.Column("total_url_statements", sa.Integer(), nullable=True),
        )


def downgrade() -> None:
    with op.batch_alter_table("wikibase_quantity_observation") as batch_op:
        batch_op.drop_column("total_url_statements")
        batch_op.drop_column("total_url_properties")
        batch_op.drop_column("total_external_identifier_statements")
        batch_op.drop_column("total_external_identifier_properties")
