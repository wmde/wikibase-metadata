"""Wikibase Software Table"""

from datetime import datetime
from typing import List, Optional
from sqlalchemy import Boolean, DateTime, Enum, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from model.database.base import ModelBase
from model.database.wikibase_software.software_tag_model import WikibaseSoftwareTagModel
from model.database.wikibase_software.software_tag_xref_model import (
    software_tag_xref_table,
)
from model.enum import WikibaseSoftwareType


class WikibaseSoftwareModel(ModelBase):
    """Wikibase Software Table"""

    __tablename__ = "wikibase_software"

    __table_args__ = (
        UniqueConstraint(
            "software_type", "software_name", name="unique_software_type_name"
        ),
    )

    id: Mapped[int] = mapped_column("id", Integer, primary_key=True, autoincrement=True)
    """ID"""

    software_type: Mapped[WikibaseSoftwareType] = mapped_column(
        "software_type", Enum(WikibaseSoftwareType), nullable=False
    )
    """Software Type"""

    software_name: Mapped[str] = mapped_column("software_name", String, nullable=False)
    """Software Name"""

    url: Mapped[Optional[str]] = mapped_column("url", String, nullable=True)
    """Reference URL"""

    data_fetched: Mapped[Optional[datetime]] = mapped_column(
        "fetched", DateTime(timezone=True), nullable=True
    )

    tags: Mapped[List[WikibaseSoftwareTagModel]] = relationship(
        secondary=software_tag_xref_table, lazy="selectin"
    )

    description: Mapped[Optional[str]] = mapped_column(
        "description", String, nullable=True
    )
    """Description"""

    latest_version: Mapped[Optional[str]] = mapped_column(
        "latest_version", String, nullable=True
    )
    """Latest Version"""

    quarterly_download_count: Mapped[Optional[int]] = mapped_column(
        "quarterly_download_count", Integer, nullable=True
    )
    """Quarterly Downloads"""

    public_wiki_count: Mapped[Optional[int]] = mapped_column(
        "public_wiki_count", Integer, nullable=True
    )
    """Public Wikis Using"""

    mediawiki_bundled: Mapped[Optional[bool]] = mapped_column(
        "mw_bundled", Boolean, nullable=True
    )
    """Bundled with Mediawiki"""

    wikibase_suite_bundled: Mapped[Optional[bool]] = mapped_column(
        "wbs_bundled", Boolean, nullable=True
    )
    """Bundled with Wikibase Suite"""

    archived: Mapped[Optional[bool]] = mapped_column("archived", Boolean, nullable=True)
    """Archived Extension"""

    def __init__(self, software_type: WikibaseSoftwareType, software_name: str):
        self.software_type = software_type
        self.software_name = software_name

    def __str__(self) -> str:
        return (
            "WikibaseSoftwareModel("
            + f"id={self.id}, "
            + f"software_type={self.software_type}, "
            + f"software_name={self.software_name})"
        )
