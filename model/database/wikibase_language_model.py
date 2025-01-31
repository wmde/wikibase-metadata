"""Wikibase URL Table"""

from sqlalchemy import Boolean, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from model.database.base import ModelBase


class WikibaseLanguageModel(ModelBase):
    """Wikibase Language Table"""

    __tablename__ = "wikibase_language"

    __table_args__ = (
        UniqueConstraint("wikibase_id", "language", name="unique_wikibase_language"),
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

    language: Mapped[str] = mapped_column("language", String, nullable=False)
    """Language"""

    primary: Mapped[bool] = mapped_column("primary", Boolean, nullable=False)
    """Primary Language"""

    def __init__(self, language: str, primary: bool = False):
        self.language = language
        self.primary = primary
