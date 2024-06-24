"""Wikibase Connectivity Object / Relationship Count Table"""

from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column

from model.database.base import ModelBase
from model.database.wikibase_observation.connectivity.relationship_count_model import (
    WikibaseConnectivityObservationRelationshipCountModel,
)


class WikibaseConnectivityObservationObjectRelationshipCountModel(
    ModelBase, WikibaseConnectivityObservationRelationshipCountModel
):
    """Wikibase Connectivity Observation Object / Relationship Count Table"""

    __tablename__ = "wikibase_connectivity_observation_object_relationship_count"

    object_count: Mapped[int] = mapped_column("object_count", Integer, nullable=False)
    """Number of Objects with This Relationship Count"""
