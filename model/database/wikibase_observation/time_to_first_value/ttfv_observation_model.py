"""Wikibase Time to First Value Observation Table"""

from datetime import datetime, timezone
from typing import Optional
from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from model.database.base import ModelBase
from model.database.wikibase_observation.time_to_first_value.item_date_model import (
    WikibaseItemDateModel,
)
from model.database.wikibase_observation.wikibase_observation_model import (
    WikibaseObservationModel,
)


class WikibaseTimeToFirstValueObservationModel(ModelBase, WikibaseObservationModel):
    """Wikibase Time to First Value Observation Table"""

    __tablename__ = "wikibase_time_to_first_value_observation"

    initiation_date: Mapped[Optional[datetime]] = mapped_column(
        "initial_date", DateTime(timezone=True), nullable=True
    )

    item_date_models: Mapped[list[WikibaseItemDateModel]] = relationship(
        "WikibaseItemDateModel",
        # back_populates="initial_value_observation",
        lazy="selectin",
    )
    """Item Date Records"""

    def __init__(self, wikibase_id: int):
        self.wikibase_id = wikibase_id
        self.observation_date = datetime.now(timezone.utc)
        self.item_date_models = []
