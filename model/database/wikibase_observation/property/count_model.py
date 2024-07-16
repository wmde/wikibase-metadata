"""Wikibase Property Popularity Count Table"""

from sqlalchemy import ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from model.database.base import ModelBase


class WikibasePropertyPopularityCountModel(ModelBase):
    """Wikibase Property Popularity Count Table"""

    __tablename__ = "wikibase_property_usage_count"

    __table_args__ = (
        UniqueConstraint(
            columns=["wikibase_property_usage_observation_id", "property_url"],
            name="unique_observation_property_url",
        ),
    )

    id: Mapped[int] = mapped_column("id", Integer, primary_key=True, autoincrement=True)
    """ID"""

    wikibase_property_popularity_observation_id: Mapped[int] = mapped_column(
        "wikibase_property_usage_observation_id",
        ForeignKey(column="wikibase_property_usage_observation.id", name="observation"),
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

    def __init__(self, property_url: str, usage_count: int):
        self.property_url = property_url
        self.usage_count = usage_count
