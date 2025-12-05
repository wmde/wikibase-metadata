"""Log Types

Revision ID: 78bcf74f8d37
Revises: c63b980be98b
Create Date: 2025-12-04 02:05:46.592675

"""

from typing import Sequence, Union

from alembic import op
from alembic_postgresql_enum import TableReference
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "78bcf74f8d37"
down_revision: Union[str, Sequence[str], None] = "c63b980be98b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

old_log_type_values = [
    "ABUSE_FILTER_CREATE",
    "ABUSE_FILTER_MODIFIY",
    "ACHIEVEMENT_BADGE",
    "APPROVE",
    "COMMENTS_CREATE",
    "COMMENTS_DELETE",
    "CONSUMER_APPROVE",
    "CONSUMER_CREATE",
    "CONSUMER_DISABLE",
    "CONSUMER_PROPOSE",
    "CONSUMER_REJECT",
    "CONSUMER_UPDATE",
    "CONFIG_UPDATE",
    "CONTENT_MODEL_CREATE",
    "CONTENT_MODEL_CHANGE",
    "DATADUMP_DELETE",
    "DATADUMP_GENERATE",
    "EVENT_DELETE",
    "EXPORT_PDF",
    "FEEDBACK_CREATE",
    "FEEDBACK_FEATURE",
    "FEEDBACK_FLAG",
    "FEEDBACK_FLAG_INAPPROPRIATE",
    "FEEDBACK_HIDE",
    "FEEDBACK_NO_ACTION",
    "FEEDBACK_RESOLVE",
    "IMPORT",
    "IMPORT_HTML",
    "INTERWIKI_CREATE",
    "INTERWIKI_DELETE",
    "INTERWIKI_EDIT",
    "ITEM_CREATE",
    "ITEM_DELETE",
    "LOCK_FLOW_LOCK_TOPIC",
    "MEDIA_APPROVE",
    "MEDIA_OVERWRITE",
    "MEDIA_REVERT",
    "MEDIA_UPLOAD",
    "MOVE",
    "PAGE_CREATE",
    "PAGE_DELETE",
    "PAGE_TRANSLATE",
    "PAGE_TRANSLATE_DELETE_FOK",
    "PAGE_TRANSLATE_DELETE_LOK",
    "PAGE_TRANSLATE_MARK",
    "PAGE_TRANSLATE_UNMARK",
    "PAGE_UPDATE_LANGUAGE",
    "PATROL",
    "PATROL_AUTO",
    "PROFILE",
    "PROPERTY_CREATE",
    "PROPERTY_DELETE",
    "PROTECT",
    "REDIRECT_DELETE",
    "REDIRECT_MOVE",
    "REVISION_DELETE",
    "TABLE_CREATE",
    "TABLE_DELETE",
    "TAG_CREATE",
    "THANK",
    "UNAPPROVE",
    "UNDO_DELETE",
    "UNPROTECT",
    "USER_BLOCK",
    "USER_UNBLOCK",
    "USER_CREATE",
    "USER_DELETE",
    "USER_MERGE",
    "USER_RENAME",
    "USER_RIGHTS",
    "WIKI_FARM",
    "WIKI_GROUP_DELETE",
    "WIKI_NAMESPACES",
    "WIKI_RIGHTS",
    "WIKI_SETTINGS",
]
new_log_type_values = [*old_log_type_values, "PAGE_TRANSLATE_REVIEW", "UNCLASSIFIED"]


def upgrade() -> None:
    """Upgrade schema."""

    op.sync_enum_values(
        enum_schema="public",
        enum_name="wikibaselogtype",
        new_values=new_log_type_values,
        affected_columns=[
            TableReference(
                table_schema="public",
                table_name="wikibase_log_observation_month_type",
                column_name="log_type",
            )
        ],
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.sync_enum_values(
        enum_schema="public",
        enum_name="wikibaselogtype",
        new_values=old_log_type_values,
        affected_columns=[
            TableReference(
                table_schema="public",
                table_name="wikibase_log_observation_month_type",
                column_name="log_type",
            )
        ],
    )
