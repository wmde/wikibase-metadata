"""Split quantity: external identifiers and URLs

Revision ID: ffb9e2b9a1a2
Revises: bcc81afe3bc3
Create Date: 2025-08-22 06:45:00.000000

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "ffb9e2b9a1a2"
down_revision: Union[str, None] = "07663ad9d60d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create new tables with the common observation columns
    op.create_table(
        "wikibase_external_identifier_observation",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("wikibase_id", sa.Integer(), nullable=False),
        sa.Column("anything", sa.Boolean(), nullable=False),
        sa.Column("date", sa.DateTime(timezone=True), nullable=False),
        sa.Column("total_external_identifier_properties", sa.Integer(), nullable=True),
        sa.Column("total_external_identifier_statements", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["wikibase_id"], ["wikibase.id"], name="observation_wikibase"
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "wikibase_url_observation",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("wikibase_id", sa.Integer(), nullable=False),
        sa.Column("anything", sa.Boolean(), nullable=False),
        sa.Column("date", sa.DateTime(timezone=True), nullable=False),
        sa.Column("total_url_properties", sa.Integer(), nullable=True),
        sa.Column("total_url_statements", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["wikibase_id"], ["wikibase.id"], name="observation_wikibase"
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    # Migrate existing data from quantity table if present
    conn = op.get_bind()
    try:
        res = conn.execute(
            sa.text(
                """
                SELECT id, wikibase_id, anything, date,
                       total_external_identifier_properties,
                       total_external_identifier_statements,
                       total_url_properties,
                       total_url_statements
                FROM wikibase_quantity_observation
                WHERE total_external_identifier_properties IS NOT NULL
                   OR total_external_identifier_statements IS NOT NULL
                   OR total_url_properties IS NOT NULL
                   OR total_url_statements IS NOT NULL
                """
            )
        )
        rows = res.fetchall()
    except Exception:
        rows = []

    if rows:
        # Insert into new tables
        for (
            _id,
            wikibase_id,
            anything,
            date,
            teip,
            teis,
            tup,
            tus,
        ) in rows:
            if teip is not None or teis is not None:
                conn.execute(
                    sa.text(
                        """
                        INSERT INTO wikibase_external_identifier_observation
                        (wikibase_id, anything, date, total_external_identifier_properties, total_external_identifier_statements)
                        VALUES (:wikibase_id, :anything, :date, :teip, :teis)
                        """
                    ),
                    {
                        "wikibase_id": wikibase_id,
                        "anything": anything,
                        "date": date,
                        "teip": teip,
                        "teis": teis,
                    },
                )
            if tup is not None or tus is not None:
                conn.execute(
                    sa.text(
                        """
                        INSERT INTO wikibase_url_observation
                        (wikibase_id, anything, date, total_url_properties, total_url_statements)
                        VALUES (:wikibase_id, :anything, :date, :tup, :tus)
                        """
                    ),
                    {
                        "wikibase_id": wikibase_id,
                        "anything": anything,
                        "date": date,
                        "tup": tup,
                        "tus": tus,
                    },
                )

    # Drop migrated columns from quantity table
    with op.batch_alter_table("wikibase_quantity_observation") as batch_op:
        for col in (
            "total_external_identifier_properties",
            "total_external_identifier_statements",
            "total_url_properties",
            "total_url_statements",
        ):
            try:
                batch_op.drop_column(col)
            except Exception:
                # Column may already be absent in some environments
                pass


def downgrade() -> None:
    # Add back columns to quantity table
    with op.batch_alter_table("wikibase_quantity_observation") as batch_op:
        batch_op.add_column(
            sa.Column(
                "total_external_identifier_properties", sa.Integer(), nullable=True
            )
        )
        batch_op.add_column(
            sa.Column(
                "total_external_identifier_statements", sa.Integer(), nullable=True
            )
        )
        batch_op.add_column(
            sa.Column("total_url_properties", sa.Integer(), nullable=True)
        )
        batch_op.add_column(
            sa.Column("total_url_statements", sa.Integer(), nullable=True)
        )

    # Move latest values per wikibase back into quantity table (best-effort)
    conn = op.get_bind()
    # External identifiers backfill
    conn.execute(
        sa.text(
            """
            UPDATE wikibase_quantity_observation AS q
            SET total_external_identifier_properties = (
                    SELECT e.total_external_identifier_properties
                    FROM wikibase_external_identifier_observation e
                    WHERE e.wikibase_id = q.wikibase_id
                    ORDER BY e.date DESC
                    LIMIT 1
                ),
                total_external_identifier_statements = (
                    SELECT e.total_external_identifier_statements
                    FROM wikibase_external_identifier_observation e
                    WHERE e.wikibase_id = q.wikibase_id
                    ORDER BY e.date DESC
                    LIMIT 1
                )
            WHERE q.anything = 1
            """
        )
    )
    # URL backfill
    conn.execute(
        sa.text(
            """
            UPDATE wikibase_quantity_observation AS q
            SET total_url_properties = (
                    SELECT u.total_url_properties
                    FROM wikibase_url_observation u
                    WHERE u.wikibase_id = q.wikibase_id
                    ORDER BY u.date DESC
                    LIMIT 1
                ),
                total_url_statements = (
                    SELECT u.total_url_statements
                    FROM wikibase_url_observation u
                    WHERE u.wikibase_id = q.wikibase_id
                    ORDER BY u.date DESC
                    LIMIT 1
                )
            WHERE q.anything = 1
            """
        )
    )

    # Drop new tables
    op.drop_table("wikibase_url_observation")
    op.drop_table("wikibase_external_identifier_observation")
