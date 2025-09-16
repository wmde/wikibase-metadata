"""add composite indexes for observation lookups

Revision ID: 4c8f9a2a1b2e
Revises: 825702b9d344
Create Date: 2025-09-11 13:05:00.000000

"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "4c8f9a2a1b2e"
down_revision: Union[str, None] = "825702b9d344"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    tables = [
        "wikibase_connectivity_observation",
        "wikibase_external_identifier_observation",
        "wikibase_property_usage_observation",
        "wikibase_quantity_observation",
        "wikibase_recent_changes_observation",
        "wikibase_software_version_observation",
        "wikibase_statistics_observation",
        "wikibase_time_to_first_value_observation",
        "wikibase_user_observation",
    ]

    for t in tables:
        op.create_index(
            f"ix_{t}_wikibase_id_date",
            t,
            ["wikibase_id", "date"],
            unique=False,
        )


def downgrade() -> None:
    tables = [
        "wikibase_connectivity_observation",
        "wikibase_external_identifier_observation",
        "wikibase_property_usage_observation",
        "wikibase_quantity_observation",
        "wikibase_recent_changes_observation",
        "wikibase_software_version_observation",
        "wikibase_statistics_observation",
        "wikibase_time_to_first_value_observation",
        "wikibase_user_observation",
    ]

    for t in tables:
        op.drop_index(f"ix_{t}_wikibase_id_date", table_name=t)
