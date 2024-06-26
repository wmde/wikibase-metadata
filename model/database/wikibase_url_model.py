"""Wikibase URL Table"""

import enum
from sqlalchemy import Enum, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from model.database.base import ModelBase


class WikibaseURLTypes(enum.Enum):
    base_url = 1
    action_query_url = 2
    index_query_url = 3
    sparql_endpoint_url = 4
    sparql_query_url = 5
    special_version = 6
    special_base = 7


class WikibaseURLModel(ModelBase):
    """Wikibase URL Table"""

    __tablename__ = "wikibase_url"

    id: Mapped[int] = mapped_column("id", Integer, primary_key=True, autoincrement=True)
    """ID"""

    wikibase_id: Mapped[int] = mapped_column(
        "wikibase_id",
        ForeignKey("wikibase.id", None, False, "observation_wikibase"),
        nullable=False,
    )
    """Wikibase ID"""

    wikibase: Mapped["WikibaseModel"] = relationship(
        "WikibaseModel", back_populates="wikibase_urls", lazy="selectin"
    )
    """Wikibase"""

    url_type: Mapped[WikibaseURLTypes] = mapped_column(
        "url_type", Enum(WikibaseURLTypes), nullable=False
    )
    """URL Type"""

    url: Mapped[str] = mapped_column("url", String, nullable=False)
    """Base URL"""
