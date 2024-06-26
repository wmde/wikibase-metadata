"""Wikibase Table"""

from typing import List, Optional
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from model.database.base import ModelBase
from model.database.wikibase_observation import (
    WikibaseConnectivityObservationModel,
    WikibasePropertyPopularityObservationModel,
    WikibaseQuantityObservationModel,
    WikibaseSoftwareVersionObservationModel,
    WikibaseUserObservationModel,
)
from model.database.wikibase_url_model import WikibaseURLModel


class WikibaseModel(ModelBase):
    """Wikibase Table"""

    __tablename__ = "wikibase"

    id: Mapped[int] = mapped_column("id", Integer, primary_key=True, autoincrement=True)
    """ID"""

    url: Mapped[str] = mapped_column("base_url", String, nullable=False)
    """Base URL"""

    action_query_url: Mapped[Optional[str]] = mapped_column(
        "action_query_url", String, nullable=True
    )
    """Action Query API"""

    index_query_url: Mapped[Optional[str]] = mapped_column(
        "index_query_url", String, nullable=True
    )
    """Index Query API"""

    sparql_query_url: Mapped[Optional[str]] = mapped_column(
        "sparql_query_url", String, nullable=True
    )
    """SPARQL Query API"""

    sparql_endpoint_url: Mapped[Optional[str]] = mapped_column(
        "sparql_endpoint_url", String, nullable=True
    )
    """SPARQL Endpoint"""

    special_version_url: Mapped[Optional[str]] = mapped_column(
        "special_version_url", String, nullable=True
    )
    """Special:Version URL"""

    wikibase_urls: Mapped[List[WikibaseURLModel]] = relationship(
        "WikibaseURLModel", back_populates="wikibase", lazy="selectin"
    )
    """URLs"""

    connectivity_observations: Mapped[
        List[WikibaseConnectivityObservationModel]
    ] = relationship(
        "WikibaseConnectivityObservationModel",
        back_populates="wikibase",
        lazy="selectin",
    )
    """Connectivity Observations"""

    property_popularity_observations: Mapped[
        List[WikibasePropertyPopularityObservationModel]
    ] = relationship(
        "WikibasePropertyPopularityObservationModel",
        back_populates="wikibase",
        lazy="selectin",
    )
    """Property Popularity Observations"""

    quantity_observations: Mapped[
        List[WikibaseQuantityObservationModel]
    ] = relationship(
        "WikibaseQuantityObservationModel", back_populates="wikibase", lazy="selectin"
    )
    """Quantity Observations"""

    software_version_observations: Mapped[
        List[WikibaseSoftwareVersionObservationModel]
    ] = relationship(
        "WikibaseSoftwareVersionObservationModel",
        back_populates="wikibase",
        lazy="selectin",
    )
    """Quantity Observations"""

    user_observations: Mapped[List[WikibaseUserObservationModel]] = relationship(
        "WikibaseUserObservationModel", back_populates="wikibase", lazy="selectin"
    )
    """User Observations"""
