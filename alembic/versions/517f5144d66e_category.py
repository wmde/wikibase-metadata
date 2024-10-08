"""Category

Revision ID: 517f5144d66e
Revises: 83448d82b997
Create Date: 2024-07-09 11:15:48.016142

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "517f5144d66e"
down_revision: Union[str, None] = "83448d82b997"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "wikibase_category",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column(
            "category",
            sa.Enum(
                "CULTURAL_AND_HISTORICAL",
                "DIGITAL_COLLECTIONS_AND_ARCHIVES",
                "EDUCATIONAL_AND_REFERENCE_COLLECTIONS",
                "EXPERIMENTAL_AND_PROTOTYPE_PROJECTS",
                "FICTIONAL_AND_CREATIVE_WORKS",
                "LEGAL_AND_POLITICAL",
                "LINGUISTIC_AND_LITERARY",
                "MATHEMATICS_AND_SCIENCE",
                "SEMANTIC_AND_PROSOPOGRAPHIC_DATA",
                "SOCIAL_AND_ADVOCACY",
                "TECHNOLOGY_AND_OPEN_SOURCE",
                name="wikibasecategories",
            ),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("category", name="unique_category"),
    )
    with op.batch_alter_table("wikibase") as batch_op:
        batch_op.add_column(
            sa.Column("wikibase_category_id", sa.Integer(), nullable=True)
        )
        batch_op.create_foreign_key(
            "wikibase_category", "wikibase_category", ["wikibase_category_id"], ["id"]
        )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("wikibase") as batch_op:
        batch_op.drop_constraint("wikibase_category", type_="foreignkey")
        batch_op.drop_column("wikibase_category_id")
    op.drop_table("wikibase_category")
    # ### end Alembic commands ###
