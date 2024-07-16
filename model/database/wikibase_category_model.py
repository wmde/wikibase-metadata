"""Wikibase Category Table"""

from typing import List
from sqlalchemy import Enum, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from model.database.base import ModelBase
from model.enum import WikibaseCategory


class WikibaseCategoryModel(ModelBase):
    """Wikibase Category Table"""

    __tablename__ = "wikibase_category"

    __table_args__ = (
        UniqueConstraint(
            columns=["category"],
            name="unique_category",
        ),
    )

    id: Mapped[int] = mapped_column("id", Integer, primary_key=True, autoincrement=True)
    """ID"""

    wikibases: Mapped[List["WikibaseModel"]] = relationship(
        "WikibaseModel", lazy="selectin", back_populates="category"
    )
    """Wikibases"""

    category: Mapped[WikibaseCategory] = mapped_column(
        "category", Enum(WikibaseCategory), nullable=False
    )
    """Category"""
