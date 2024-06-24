"""Wikibase Property Usage Observation Table"""

from typing import List
from sqlalchemy.orm import Mapped, relationship

from model.database.base import ModelBase
from model.database.wikibase_observation.property_usage.property_count_model import (
    WikibasePropertyUsageCountModel,
)
from model.database.wikibase_observation.wikibase_observation_model import (
    WikibaseObservationModel,
)


class WikibasePropertyUsageObservationModel(ModelBase, WikibaseObservationModel):
    """Wikibase Property Usage Observation Table"""

    __tablename__ = "wikibase_property_usage_observation"

    property_count_observations: Mapped[
        List[WikibasePropertyUsageCountModel]
    ] = relationship(
        "WikibasePropertyUsageCountModel",
        back_populates="property_usage_observation",
        lazy="selectin",
    )
    """Property Count Observations"""
