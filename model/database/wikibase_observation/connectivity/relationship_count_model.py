"""Wikibase Connectivity Relationship Count Table"""

from sqlalchemy import ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, declared_attr, mapped_column, relationship


class WikibaseConnectivityObservationRelationshipCountModel:
    """Wikibase Connectivity Observation Relationship Count Table"""

    __table_args__ = (
        UniqueConstraint(
            "wikibase_connectivity_observation_id",
            "relationship_count",
            name="unique_observation_relationship_count",
        ),
    )

    id: Mapped[int] = mapped_column("id", Integer, primary_key=True, autoincrement=True)
    """ID"""

    wikibase_connectivity_observation_id: Mapped[int] = mapped_column(
        "wikibase_connectivity_observation_id",
        ForeignKey(column="wikibase_connectivity_observation.id", name="observation"),
        nullable=False,
    )
    """Wikibase Connectivity Observation ID"""

    @declared_attr
    def connectivity_observation(
        self,
    ) -> Mapped["WikibaseConnectivityObservationModel"]: # type: ignore
        """Connectivity Observation"""
        return relationship("WikibaseConnectivityObservationModel", lazy="selectin")

    relationship_count: Mapped[int] = mapped_column(
        "relationship_count", Integer, nullable=False
    )
    """Number of Relationships"""
