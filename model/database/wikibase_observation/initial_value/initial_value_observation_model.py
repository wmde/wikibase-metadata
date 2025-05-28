"""Wikibase Connectivity Observation Table"""

from datetime import datetime
from typing import Optional
from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from model.database.base import ModelBase
from model.database.wikibase_observation.initial_value.item_date_model import (
    WikibaseItemDateModel,
)
from model.database.wikibase_observation.wikibase_observation_model import (
    WikibaseObservationModel,
)


class WikibaseInitialValueObservationModel(ModelBase, WikibaseObservationModel):
    """Wikibase Initial Value Observation Table"""

    __tablename__ = "wikibase_initial_value_observation"

    initiation_date: Mapped[Optional[datetime]] = mapped_column(
        "initial_date", DateTime(timezone=True), nullable=True
    )

    item_date_models: Mapped[list[WikibaseItemDateModel]] = relationship(
        "WikibaseItemDateModel",
        back_populates="initial_value_observation",
        lazy="selectin",
    )
    """Item Date Records"""
