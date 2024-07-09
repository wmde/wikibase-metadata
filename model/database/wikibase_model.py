"""Wikibase Table"""

# pylint: disable=too-many-instance-attributes,too-many-arguments

from typing import List, Optional
from sqlalchemy import Boolean, ForeignKey, Integer, String, and_
from sqlalchemy.orm import Mapped, mapped_column, relationship

from model.database.base import ModelBase
from model.database.wikibase_category_model import WikibaseCategoryModel
from model.database.wikibase_observation import (
    WikibaseConnectivityObservationModel,
    WikibaseLogObservationModel,
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

    category_id: Mapped[int] = mapped_column(
        "wikibase_category_id",
        ForeignKey("wikibase_category.id", None, False, "wikibase_category"),
        nullable=True,
    )
    """Wikibase Category ID"""

    category: Mapped[WikibaseCategoryModel] = relationship(
        "WikibaseCategoryModel", lazy="selectin", back_populates="wikibases"
    )
    """Wikibase Category"""

    checked: Mapped[bool] = mapped_column("valid", Boolean, nullable=False)
    """Checked"""

    url: Mapped[WikibaseURLModel] = relationship(
        "WikibaseURLModel",
        primaryjoin=and_(
            id == WikibaseURLModel.wikibase_id,
            WikibaseURLTypes.BASE_URL == WikibaseURLModel.url_type,
        ),
        lazy="selectin",
        overlaps=",".join(
            [
                "action_api_url",
                "index_api_url",
                "sparql_endpoint_url",
                "sparql_query_url",
                "special_version_url",
                "wikibase",
            ]
        ),
    )
    """Base URL"""

    action_api_url: Mapped[Optional[WikibaseURLModel]] = relationship(
        "WikibaseURLModel",
        primaryjoin=and_(
            id == WikibaseURLModel.wikibase_id,
            WikibaseURLTypes.ACTION_QUERY_URL == WikibaseURLModel.url_type,
        ),
        lazy="selectin",
        overlaps=",".join(
            [
                "index_api_url",
                "sparql_endpoint_url",
                "sparql_query_url",
                "special_version_url",
                "url",
                "wikibase",
            ]
        ),
    )
    """Action Query API"""

    index_api_url: Mapped[Optional[WikibaseURLModel]] = relationship(
        "WikibaseURLModel",
        primaryjoin=and_(
            id == WikibaseURLModel.wikibase_id,
            WikibaseURLTypes.INDEX_QUERY_URL == WikibaseURLModel.url_type,
        ),
        lazy="selectin",
        overlaps=",".join(
            [
                "action_api_url",
                "sparql_endpoint_url",
                "sparql_query_url",
                "special_version_url",
                "url",
                "wikibase",
            ]
        ),
    )
    """Index Query API"""

    sparql_query_url: Mapped[Optional[WikibaseURLModel]] = relationship(
        "WikibaseURLModel",
        primaryjoin=and_(
            id == WikibaseURLModel.wikibase_id,
            WikibaseURLTypes.SPARQL_QUERY_URL == WikibaseURLModel.url_type,
        ),
        lazy="selectin",
        overlaps=",".join(
            [
                "action_api_url",
                "index_api_url",
                "sparql_endpoint_url",
                "special_version_url",
                "url",
                "wikibase",
            ]
        ),
    )
    """SPARQL Query API"""

    sparql_endpoint_url: Mapped[Optional[WikibaseURLModel]] = relationship(
        "WikibaseURLModel",
        primaryjoin=and_(
            id == WikibaseURLModel.wikibase_id,
            WikibaseURLTypes.SPARQL_ENDPOINT_URL == WikibaseURLModel.url_type,
        ),
        lazy="selectin",
        overlaps=",".join(
            [
                "action_api_url",
                "index_api_url",
                "sparql_query_url",
                "special_version_url",
                "url",
                "wikibase",
            ]
        ),
    )
    """SPARQL Endpoint"""

    special_version_url: Mapped[Optional[WikibaseURLModel]] = relationship(
        "WikibaseURLModel",
        primaryjoin=and_(
            id == WikibaseURLModel.wikibase_id,
            WikibaseURLTypes.SPECIAL_VERSION_URL == WikibaseURLModel.url_type,
        ),
        lazy="selectin",
        overlaps=",".join(
            [
                "action_api_url",
                "index_api_url",
                "sparql_endpoint_url",
                "sparql_query_url",
                "url",
                "wikibase",
            ]
        ),
    )
    """Special:Version URL"""

    connectivity_observations: Mapped[List[WikibaseConnectivityObservationModel]] = (
        relationship(
            "WikibaseConnectivityObservationModel",
            back_populates="wikibase",
            lazy="selectin",
        )
    )
    """Connectivity Observations"""

    log_observations: Mapped[List[WikibaseLogObservationModel]] = relationship(
        "WikibaseLogObservationModel",
        back_populates="wikibase",
        lazy="selectin",
    )
    """Log Observations"""

    property_popularity_observations: Mapped[
        List[WikibasePropertyPopularityObservationModel]
    ] = relationship(
        "WikibasePropertyPopularityObservationModel",
        back_populates="wikibase",
        lazy="selectin",
    )
    """Property Popularity Observations"""

    quantity_observations: Mapped[List[WikibaseQuantityObservationModel]] = (
        relationship(
            "WikibaseQuantityObservationModel",
            back_populates="wikibase",
            lazy="selectin",
        )
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

    def __init__(
        self,
        wikibase_name: str,
        base_url: str,
        region: str,
        organization: Optional[str] = None,
        country: Optional[str] = None,
        sparql_query_url: Optional[str] = None,
        sparql_endpoint_url: Optional[str] = None,
    ):
        self.wikibase_name = wikibase_name
        self.organization = organization
        self.country = country
        self.region = region
        self.checked = False
        self.url = WikibaseURLModel(url=base_url, url_type=WikibaseURLTypes.BASE_URL)
        if sparql_endpoint_url is not None:
            self.sparql_endpoint_url = WikibaseURLModel(
                url=sparql_endpoint_url, url_type=WikibaseURLTypes.SPARQL_ENDPOINT_URL
            )
        if sparql_query_url is not None:
            self.sparql_query_url = WikibaseURLModel(
                url=sparql_query_url, url_type=WikibaseURLTypes.SPARQL_QUERY_URL
            )
