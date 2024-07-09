"""Wikibase URL Table"""

import enum
from typing import List
from sqlalchemy import Enum, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from model.database.base import ModelBase


class WikibaseCategory(enum.Enum):
    """Wikibase Categories"""

    CULTURAL_AND_HISTORICAL = 1
    DIGITAL_COLLECTIONS_AND_ARCHIVES = 2
    EDUCATIONAL_AND_REFERENCE_COLLECTIONS = 3
    EXPERIMENTAL_AND_PROTOTYPE_PROJECTS = 4
    FICTIONAL_AND_CREATIVE_WORKS = 5
    LEGAL_AND_POLITICAL = 6
    LINGUISTIC_AND_LITERARY = 7
    MATHEMATICS_AND_SCIENCE = 8
    SEMANTIC_AND_PROSOPOGRAPHIC_DATA = 9
    SOCIAL_AND_ADVOCACY = 10
    TECHNOLOGY_AND_OPEN_SOURCE = 11


def wikibase_category_name(category: WikibaseCategory) -> str:
    return category.name.replace("_", " ").title().replace("And", "and")


class WikibaseCategoryModel(ModelBase):
    """Wikibase Category Table"""

    __tablename__ = "wikibase_category"

    __table_args__ = (
        UniqueConstraint(
            "category",
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
