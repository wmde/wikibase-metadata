"""Wikibase Property Popularity Observation Table"""

from typing import List
from sqlalchemy.orm import Mapped, relationship

from model.database.base import ModelBase
from model.database.wikibase_observation.property.count_model import (
    WikibasePropertyPopularityCountModel,
)
from model.database.wikibase_observation.wikibase_observation_model import (
    WikibaseObservationModel,
)


class WikibasePropertyPopularityObservationModel(ModelBase, WikibaseObservationModel):
    """Wikibase Property Popularity Observation Table"""

    __tablename__ = "wikibase_property_usage_observation"

    property_count_observations: Mapped[List[WikibasePropertyPopularityCountModel]] = (
        relationship(
            "WikibasePropertyPopularityCountModel",
            back_populates="wikibase_property_popularity_observation",
            lazy="selectin",
        )
    )
    """Property Count Observations"""
