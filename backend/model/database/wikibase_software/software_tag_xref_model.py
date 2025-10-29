"""Software/Tag XRef Table"""

from sqlalchemy import Column, ForeignKey, Table

from model.database.base import ModelBase


software_tag_xref_table = Table(
    "wikibase_software_tag_xref",
    ModelBase.metadata,
    Column(
        "wikibase_software_id",
        ForeignKey("wikibase_software.id", None, False, "foreign_wikibase_software_id"),
        primary_key=True,
    ),
    Column(
        "wikibase_software_tag_id",
        ForeignKey(
            "wikibase_software_tag.id", None, False, "foreign_wikibase_software_tag_id"
        ),
        primary_key=True,
    ),
)
"""Software/Tag XRef Table"""
