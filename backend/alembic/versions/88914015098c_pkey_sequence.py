"""pkey sequence

Revision ID: 88914015098c
Revises: 78bcf74f8d37
Create Date: 2025-12-07 17:26:53.796547

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "88914015098c"
down_revision: Union[str, Sequence[str], None] = "78bcf74f8d37"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


id_tables = [
    "wikibase",
    "wikibase_category",
    "wikibase_connectivity_observation",
    "wikibase_connectivity_observation_item_relationship_count",
    "wikibase_connectivity_observation_object_relationship_count",
    "wikibase_external_identifier_observation",
    "wikibase_item_date",
    "wikibase_language",
    "wikibase_log_observation_month",
    "wikibase_log_observation_month_type",
    "wikibase_log_observation_month_user",
    "wikibase_property_usage_count",
    "wikibase_property_usage_observation",
    "wikibase_quantity_observation",
    "wikibase_recent_changes_observation",
    "wikibase_software",
    "wikibase_software_tag",
    "wikibase_software_version",
    "wikibase_software_version_observation",
    "wikibase_statistics_observation",
    "wikibase_time_to_first_value_observation",
    "wikibase_url",
    "wikibase_user_group",
    "wikibase_user_observation",
    "wikibase_user_observation_group",
]


def upgrade() -> None:
    """Upgrade schema."""
    for table in id_tables:
        op.execute(
            sa.text(
                f"SELECT pg_catalog.setval(pg_get_serial_sequence('{table}', 'id'), MAX(id)) FROM {table};"
            )
        )


def downgrade() -> None:
    """Downgrade schema."""
    pass
