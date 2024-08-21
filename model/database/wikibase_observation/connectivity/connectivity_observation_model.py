"""Wikibase Connectivity Observation Table"""

from typing import List, Optional
from sqlalchemy import Double, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from model.database.base import ModelBase
from model.database.wikibase_observation.connectivity.item_relationship_count_model import (
    WikibaseConnectivityObservationItemRelationshipCountModel,
)
from model.database.wikibase_observation.connectivity.object_relationship_count_model import (
    WikibaseConnectivityObservationObjectRelationshipCountModel,
)
from model.database.wikibase_observation.wikibase_observation_model import (
    WikibaseObservationModel,
)


class WikibaseConnectivityObservationModel(ModelBase, WikibaseObservationModel):
    """Wikibase Connectivity Observation Table"""

    __tablename__ = "wikibase_connectivity_observation"

    returned_links: Mapped[Optional[int]] = mapped_column(
        "link_count", Integer, nullable=True
    )
    """number of non-unique item -> item links returned"""

    connectivity: Mapped[Optional[float]] = mapped_column(
        "connectivity", Double, nullable=True
    )
    """number of unique item -> item connections (regardless of steps) / number of items squared"""

    average_connected_distance: Mapped[Optional[float]] = mapped_column(
        "average_connected_distance", Double, nullable=True
    )
    """Average steps for item -> item connections, ignoring disconnected items"""

    item_relationship_count_observations: Mapped[
        List[WikibaseConnectivityObservationItemRelationshipCountModel]
    ] = relationship(
        "WikibaseConnectivityObservationItemRelationshipCountModel",
        back_populates="connectivity_observation",
        lazy="selectin",
    )
    """Item / Relationship Count Observations"""

    object_relationship_count_observations: Mapped[
        List[WikibaseConnectivityObservationObjectRelationshipCountModel]
    ] = relationship(
        "WikibaseConnectivityObservationObjectRelationshipCountModel",
        back_populates="connectivity_observation",
        lazy="selectin",
    )
    """Object / Relationship Count Observations"""
