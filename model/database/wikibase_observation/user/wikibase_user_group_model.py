"""Wikibase User Group"""

from typing import List
from sqlalchemy import Boolean, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from model.database.base import ModelBase
from model.database.wikibase_observation.user.wikibase_user_observation_group_model import (
    WikibaseUserObservationGroupModel,
)


class WikibaseUserGroupModel(ModelBase):
    """Wikibase User Group"""

    __tablename__ = "wikibase_user_group"
    __table_args__ = (
        UniqueConstraint(columns=["group_name"], name="unique_group_name"),
    )

    id: Mapped[int] = mapped_column("id", Integer, primary_key=True, autoincrement=True)
    """ID"""

    group_name: Mapped[str] = mapped_column("group_name", String, nullable=False)

    wikibase_default_group: Mapped[bool] = mapped_column(
        "default", Boolean, nullable=False, default=False
    )
    """Wikibase Default?"""

    user_group_observations: Mapped[List[WikibaseUserObservationGroupModel]] = (
        relationship(
            "WikibaseUserObservationGroupModel",
            back_populates="user_group",
            lazy="selectin",
        )
    )
    """User Group Observations"""
