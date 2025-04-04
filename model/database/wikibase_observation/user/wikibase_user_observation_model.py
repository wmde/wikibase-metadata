"""Wikibase User Observation Table"""

from typing import Optional
from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from model.database.base import ModelBase
from model.database.wikibase_observation.wikibase_observation_model import (
    WikibaseObservationModel,
)
from model.database.wikibase_observation.user.wikibase_user_observation_group_model import (
    WikibaseUserObservationGroupModel,
)


class WikibaseUserObservationModel(ModelBase, WikibaseObservationModel):
    """Wikibase User Observation Table"""

    __tablename__ = "wikibase_user_observation"

    total_users: Mapped[Optional[int]] = mapped_column(
        "total_users", Integer, nullable=True
    )
    """Total Users"""

    user_group_observations: Mapped[list[WikibaseUserObservationGroupModel]] = (
        relationship(
            "WikibaseUserObservationGroupModel",
            back_populates="user_observation",
            lazy="selectin",
        )
    )
    """User Group Observations"""
