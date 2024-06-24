"""Wikibase User Observation Table"""

from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column

from model.database.base import ModelBase
from model.database.wikibase_observation.connectivity.relationship_count_model import (
    WikibaseConnectivityObservationRelationshipCountModel,
)


class WikibaseConnectivityObservationItemRelationshipCountModel(
    ModelBase, WikibaseConnectivityObservationRelationshipCountModel
):
    """Wikibase Connectivity Observation Item / Relationship Count Table"""

    __tablename__ = "wikibase_connectivity_observation_item_relationship_count"

    item_count: Mapped[int] = mapped_column("item_count", Integer, nullable=False)
    """Number of Items with This Relationship Count"""
