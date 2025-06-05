"""Wikibase URL Table"""

import re
from sqlalchemy import Enum, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from model.database.base import ModelBase
from model.enum import WikibaseURLType


class WikibaseURLModel(ModelBase):
    """Wikibase URL Table"""

    __tablename__ = "wikibase_url"

    __table_args__ = (
        UniqueConstraint("wikibase_id", "url_type", name="unique_wikibase_url_type"),
    )

    id: Mapped[int] = mapped_column("id", Integer, primary_key=True, autoincrement=True)
    """ID"""

    wikibase_id: Mapped[int] = mapped_column(
        "wikibase_id",
        ForeignKey(column="wikibase.id", name="observation_wikibase"),
        nullable=False,
    )
    """Wikibase ID"""

    wikibase: Mapped["WikibaseModel"] = relationship(  # type: ignore
        "WikibaseModel", lazy="selectin"
    )
    """Wikibase"""

    url_type: Mapped[WikibaseURLType] = mapped_column(
        "url_type", Enum(WikibaseURLType), nullable=False
    )
    """URL Type"""

    url: Mapped[str] = mapped_column("url", String, nullable=False)
    """URL"""


def join_url(*args: str) -> str:
    """Join URL"""

    if len(args) < 1:
        raise ValueError("Must Pass At Least One Arg")
    if len(args) == 1:
        return args[0]
    if len(args) > 1:
        return "/".join([re.sub(r"^/?(.*?)/?$", r"\1", arg) for arg in args])
