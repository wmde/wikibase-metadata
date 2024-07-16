"""Wikibase URL Table"""

from sqlalchemy import Enum, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from model.database.base import ModelBase
from model.enum import WikibaseURLTypes


class WikibaseURLModel(ModelBase):
    """Wikibase URL Table"""

    __tablename__ = "wikibase_url"

    __table_args__ = (
        UniqueConstraint(
            "wikibase_id",
            "url_type",
            name="unique_wikibase_url_type",
        ),
    )

    id: Mapped[int] = mapped_column("id", Integer, primary_key=True, autoincrement=True)
    """ID"""

    wikibase_id: Mapped[int] = mapped_column(
        "wikibase_id",
        ForeignKey(column="wikibase.id", name="observation_wikibase"),
        nullable=False,
    )
    """Wikibase ID"""

    wikibase: Mapped["WikibaseModel"] = relationship("WikibaseModel", lazy="selectin")
    """Wikibase"""

    url_type: Mapped[WikibaseURLTypes] = mapped_column(
        "url_type", Enum(WikibaseURLTypes), nullable=False
    )
    """URL Type"""

    url: Mapped[str] = mapped_column("url", String, nullable=False)
    """Base URL"""
