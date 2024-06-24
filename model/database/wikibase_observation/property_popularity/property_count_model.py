"""Wikibase Property Popularity Count Table"""

from sqlalchemy import ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from model.database.base import ModelBase


class WikibasePropertyPopularityCountModel(ModelBase):
    """Wikibase Property Popularity Count Table"""

    __tablename__ = "wikibase_property_usage_count"

    __table_args__ = (
        UniqueConstraint(
            "wikibase_property_usage_observation_id",
            "property_url",
            name="unique_observation_property_url",
        ),
    )

    id: Mapped[int] = mapped_column("id", Integer, primary_key=True, autoincrement=True)
    """ID"""

    wikibase_property_popularity_observation_id = mapped_column(
        "wikibase_property_usage_observation_id",
        ForeignKey(
            "wikibase_property_usage_observation.id", None, False, "observation"
        ),
        nullable=False,
    )
    """Wikibase Property Popularity Observation ID"""

    wikibase_property_popularity_observation: Mapped[
        "WikibasePropertyPopularityObservationModel"
    ] = relationship(
        "WikibasePropertyPopularityObservationModel",
        back_populates="property_count_observations",
        lazy="selectin",
    )
    """Property Popularity Observation"""

    property_url: Mapped[str] = mapped_column("property_url", String, nullable=False)
    """Property URL"""

    usage_count: Mapped[int] = mapped_column("usage_count", Integer, nullable=False)
    """Number of Relationships with This Property"""
