"""Wikibase Category Table"""

from sqlalchemy import Enum, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from model.database.base import ModelBase
from model.enum import WikibaseCategory


class WikibaseCategoryModel(ModelBase):
    """Wikibase Category Table"""

    __tablename__ = "wikibase_category"

    __table_args__ = (UniqueConstraint("category", name="unique_category"),)

    id: Mapped[int] = mapped_column("id", Integer, primary_key=True, autoincrement=True)
    """ID"""

    wikibases: Mapped[list["WikibaseModel"]] = relationship(
        "WikibaseModel", lazy="selectin", back_populates="category"
    )
    """Wikibases"""

    category: Mapped[WikibaseCategory] = mapped_column(
        "category", Enum(WikibaseCategory), nullable=False
    )
    """Category"""

    def __str__(self):
        return f"WikibaseCategoryModel(id={self.id}, category={self.category})"
