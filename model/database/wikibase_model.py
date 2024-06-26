"""Wikibase Table"""

from typing import List, Optional
from sqlalchemy import Integer, String, and_
from sqlalchemy.orm import Mapped, mapped_column, relationship

from model.database.base import ModelBase
from model.database.wikibase_observation import (
    WikibaseConnectivityObservationModel,
    WikibasePropertyPopularityObservationModel,
    WikibaseQuantityObservationModel,
    WikibaseSoftwareVersionObservationModel,
    WikibaseUserObservationModel,
)
from model.database.wikibase_url_model import WikibaseURLModel, WikibaseURLTypes


class WikibaseModel(ModelBase):
    """Wikibase Table"""

    __tablename__ = "wikibase"

    id: Mapped[int] = mapped_column("id", Integer, primary_key=True, autoincrement=True)
    """ID"""

    wikibase_name: Mapped[str] = mapped_column("wikibase_name", String, nullable=False)
    """Name"""

    organization: Mapped[Optional[str]] = mapped_column(
        "organization", String, nullable=True
    )
    """Organization"""

    country: Mapped[Optional[str]] = mapped_column("country", String, nullable=True)
    """Country"""

    region: Mapped[str] = mapped_column("region", String, nullable=False)
    """Region"""

    url: Mapped[WikibaseURLModel] = relationship(
        "WikibaseURLModel",
        primaryjoin=and_(
            id == WikibaseURLModel.wikibase_id,
            WikibaseURLTypes.base_url == WikibaseURLModel.url_type,
        ),
        lazy="selectin",
    )
    """Base URL"""

    action_query_url: Mapped[Optional[WikibaseURLModel]] = relationship(
        "WikibaseURLModel",
        primaryjoin=and_(
            id == WikibaseURLModel.wikibase_id,
            WikibaseURLTypes.action_query_url == WikibaseURLModel.url_type,
        ),
        lazy="selectin",
    )
    """Action Query API"""

    index_query_url: Mapped[Optional[WikibaseURLModel]] = relationship(
        "WikibaseURLModel",
        primaryjoin=and_(
            id == WikibaseURLModel.wikibase_id,
            WikibaseURLTypes.index_query_url == WikibaseURLModel.url_type,
        ),
        lazy="selectin",
    )
    """Index Query API"""

    sparql_query_url: Mapped[Optional[WikibaseURLModel]] = relationship(
        "WikibaseURLModel",
        primaryjoin=and_(
            id == WikibaseURLModel.wikibase_id,
            WikibaseURLTypes.sparql_query_url == WikibaseURLModel.url_type,
        ),
        lazy="selectin",
    )
    """SPARQL Query API"""

    sparql_endpoint_url: Mapped[Optional[WikibaseURLModel]] = relationship(
        "WikibaseURLModel",
        primaryjoin=and_(
            id == WikibaseURLModel.wikibase_id,
            WikibaseURLTypes.sparql_endpoint_url == WikibaseURLModel.url_type,
        ),
        lazy="selectin",
    )
    """SPARQL Endpoint"""

    special_version_url: Mapped[Optional[WikibaseURLModel]] = relationship(
        "WikibaseURLModel",
        primaryjoin=and_(
            id == WikibaseURLModel.wikibase_id,
            WikibaseURLTypes.special_version_url == WikibaseURLModel.url_type,
        ),
        lazy="selectin",
    )
    """Special:Version URL"""

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
