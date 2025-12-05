"""bigint

Revision ID: c63b980be98b
Revises: b60498d6c3b1
Create Date: 2025-11-21 14:36:01.251256

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "c63b980be98b"
down_revision: Union[str, Sequence[str], None] = "b60498d6c3b1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    with op.batch_alter_table("wikibase_quantity_observation") as batch_op:

        batch_op.alter_column(
            "total_items", existing_type=sa.Integer, type_=sa.BigInteger
        )
        batch_op.alter_column(
            "total_lexemes", existing_type=sa.Integer, type_=sa.BigInteger
        )
        batch_op.alter_column(
            "total_properties", existing_type=sa.Integer, type_=sa.BigInteger
        )
        batch_op.alter_column(
            "total_triples", existing_type=sa.Integer, type_=sa.BigInteger
        )


def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table("wikibase_quantity_observation") as batch_op:

        batch_op.alter_column(
            "total_items", existing_type=sa.BigInteger, type_=sa.Integer
        )
        batch_op.alter_column(
            "total_lexemes", existing_type=sa.BigInteger, type_=sa.Integer
        )
        batch_op.alter_column(
            "total_properties", existing_type=sa.BigInteger, type_=sa.Integer
        )
        batch_op.alter_column(
            "total_triples", existing_type=sa.BigInteger, type_=sa.Integer
        )
