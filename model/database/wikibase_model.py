"""Wikibase Table"""

from typing import Optional
from sqlalchemy import Boolean, ForeignKey, Integer, String, and_, not_
from sqlalchemy.orm import Mapped, mapped_column, relationship

from model.database.base import ModelBase
from model.database.wikibase_category_model import WikibaseCategoryModel
from model.database.wikibase_language_model import WikibaseLanguageModel
from model.database.wikibase_observation import (
    WikibaseConnectivityObservationModel,
    WikibaseLogMonthObservationModel,
    WikibasePropertyPopularityObservationModel,
    WikibaseQuantityObservationModel,
    WikibaseSoftwareVersionObservationModel,
    WikibaseStatisticsObservationModel,
    WikibaseUserObservationModel,
)
from model.database.wikibase_url_model import WikibaseURLModel
from model.enum import WikibaseURLType


# pylint: disable-next=too-many-instance-attributes
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

    description: Mapped[Optional[str]] = mapped_column(
        "description", String, nullable=True
    )
    """Description"""

    country: Mapped[Optional[str]] = mapped_column("country", String, nullable=True)
    """Country"""

    region: Mapped[Optional[str]] = mapped_column("region", String, nullable=True)
    """Region"""

    category_id: Mapped[Optional[int]] = mapped_column(
        "wikibase_category_id",
        ForeignKey(column="wikibase_category.id", name="wikibase_category"),
        nullable=True,
    )
    """Wikibase Category ID"""

    category: Mapped[Optional[WikibaseCategoryModel]] = relationship(
        "WikibaseCategoryModel", lazy="selectin", back_populates="wikibases"
    )
    """Wikibase Category"""

    checked: Mapped[bool] = mapped_column("valid", Boolean, nullable=False)
    """Checked"""

    test: Mapped[bool] = mapped_column("test", Boolean, nullable=False)
    """Test Wikibase?"""

    languages: Mapped[list[WikibaseLanguageModel]] = relationship(
        "WikibaseLanguageModel", back_populates="wikibase", lazy="select"
    )
    """Languages"""

    primary_language: Mapped[Optional[WikibaseLanguageModel]] = relationship(
        "WikibaseLanguageModel",
        primaryjoin=and_(
            id == WikibaseLanguageModel.wikibase_id, WikibaseLanguageModel.primary
        ),
        lazy="selectin",
    )

    additional_languages: Mapped[list[WikibaseLanguageModel]] = relationship(
        "WikibaseLanguageModel",
        primaryjoin=and_(
            id == WikibaseLanguageModel.wikibase_id, not_(WikibaseLanguageModel.primary)
        ),
        lazy="selectin",
    )

    url: Mapped[WikibaseURLModel] = relationship(
        "WikibaseURLModel",
        primaryjoin=and_(
            id == WikibaseURLModel.wikibase_id,
            WikibaseURLType.BASE_URL == WikibaseURLModel.url_type,
        ),
        lazy="selectin",
        overlaps=",".join(
            [
                "action_api_url",
                "index_api_url",
                "sparql_endpoint_url",
                "sparql_query_url",
                "special_statistics_url",
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
            WikibaseURLType.ACTION_QUERY_URL == WikibaseURLModel.url_type,
        ),
        lazy="selectin",
        overlaps=",".join(
            [
                "index_api_url",
                "sparql_endpoint_url",
                "sparql_query_url",
                "special_statistics_url",
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
            WikibaseURLType.INDEX_QUERY_URL == WikibaseURLModel.url_type,
        ),
        lazy="selectin",
        overlaps=",".join(
            [
                "action_api_url",
                "sparql_endpoint_url",
                "sparql_query_url",
                "special_statistics_url",
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
            WikibaseURLType.SPARQL_QUERY_URL == WikibaseURLModel.url_type,
        ),
        lazy="selectin",
        overlaps=",".join(
            [
                "action_api_url",
                "index_api_url",
                "sparql_endpoint_url",
                "special_statistics_url",
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
            WikibaseURLType.SPARQL_ENDPOINT_URL == WikibaseURLModel.url_type,
        ),
        lazy="selectin",
        overlaps=",".join(
            [
                "action_api_url",
                "index_api_url",
                "sparql_query_url",
                "special_statistics_url",
                "special_version_url",
                "url",
                "wikibase",
            ]
        ),
    )
    """SPARQL Endpoint"""

    special_statistics_url: Mapped[Optional[WikibaseURLModel]] = relationship(
        "WikibaseURLModel",
        primaryjoin=and_(
            id == WikibaseURLModel.wikibase_id,
            WikibaseURLType.SPECIAL_STATISTICS_URL == WikibaseURLModel.url_type,
        ),
        lazy="selectin",
        overlaps=",".join(
            [
                "action_api_url",
                "index_api_url",
                "sparql_endpoint_url",
                "sparql_query_url",
                "special_version_url",
                "url",
                "wikibase",
            ]
        ),
    )
    """Special:Statistics URL"""

    special_version_url: Mapped[Optional[WikibaseURLModel]] = relationship(
        "WikibaseURLModel",
        primaryjoin=and_(
            id == WikibaseURLModel.wikibase_id,
            WikibaseURLType.SPECIAL_VERSION_URL == WikibaseURLModel.url_type,
        ),
        lazy="selectin",
        overlaps=",".join(
            [
                "action_api_url",
                "index_api_url",
                "sparql_endpoint_url",
                "sparql_query_url",
                "special_statistics_url",
                "url",
                "wikibase",
            ]
        ),
    )
    """Special:Version URL"""

    connectivity_observations: Mapped[list[WikibaseConnectivityObservationModel]] = (
        relationship(
            "WikibaseConnectivityObservationModel",
            back_populates="wikibase",
            lazy="select",
        )
    )
    """Connectivity Observations"""

    log_month_observations: Mapped[list[WikibaseLogMonthObservationModel]] = (
        relationship(
            "WikibaseLogMonthObservationModel", back_populates="wikibase", lazy="select"
        )
    )
    """Log Month Observations"""

    property_popularity_observations: Mapped[
        list[WikibasePropertyPopularityObservationModel]
    ] = relationship(
        "WikibasePropertyPopularityObservationModel",
        back_populates="wikibase",
        lazy="select",
    )
    """Property Popularity Observations"""

    quantity_observations: Mapped[list[WikibaseQuantityObservationModel]] = (
        relationship(
            "WikibaseQuantityObservationModel", back_populates="wikibase", lazy="select"
        )
    )
    """Quantity Observations"""

    software_version_observations: Mapped[
        list[WikibaseSoftwareVersionObservationModel]
    ] = relationship(
        "WikibaseSoftwareVersionObservationModel",
        back_populates="wikibase",
        lazy="select",
    )
    """Software Version Observations"""

    statistics_observations: Mapped[list[WikibaseStatisticsObservationModel]] = (
        relationship(
            "WikibaseStatisticsObservationModel",
            back_populates="wikibase",
            lazy="select",
        )
    )
    """Statistics Observations"""

    user_observations: Mapped[list[WikibaseUserObservationModel]] = relationship(
        "WikibaseUserObservationModel", back_populates="wikibase", lazy="select"
    )
    """User Observations"""

    # pylint: disable-next=too-many-arguments,too-many-positional-arguments
    def __init__(
        self,
        wikibase_name: str,
        base_url: str,
        description: Optional[str] = None,
        organization: Optional[str] = None,
        country: Optional[str] = None,
        region: Optional[str] = None,
        primary_language: Optional[str] = None,
        additional_languages: Optional[list[str]] = None,
        action_api_url: Optional[str] = None,
        index_api_url: Optional[str] = None,
        sparql_query_url: Optional[str] = None,
        sparql_endpoint_url: Optional[str] = None,
        special_statistics_url: Optional[str] = None,
        special_version_url: Optional[str] = None,
    ):
        self.wikibase_name = wikibase_name
        self.description = description
        self.organization = organization
        self.country = country
        self.region = region
        self.checked = False
        self.test = False
        if primary_language is not None:
            self.languages.append(
                WikibaseLanguageModel(language=primary_language, primary=True)
            )
        if additional_languages is not None:
            self.languages.extend(
                [WikibaseLanguageModel(language=l) for l in additional_languages]
            )

        self.url = WikibaseURLModel(url=base_url, url_type=WikibaseURLType.BASE_URL)
        if action_api_url is not None:
            self.action_api_url = WikibaseURLModel(
                url=action_api_url, url_type=WikibaseURLType.ACTION_QUERY_URL
            )
        if index_api_url is not None:
            self.index_api_url = WikibaseURLModel(
                url=index_api_url, url_type=WikibaseURLType.INDEX_QUERY_URL
            )
        if sparql_endpoint_url is not None:
            self.sparql_endpoint_url = WikibaseURLModel(
                url=sparql_endpoint_url, url_type=WikibaseURLType.SPARQL_ENDPOINT_URL
            )
        if sparql_query_url is not None:
            self.sparql_query_url = WikibaseURLModel(
                url=sparql_query_url, url_type=WikibaseURLType.SPARQL_QUERY_URL
            )
        if special_statistics_url is not None:
            self.special_statistics_url = WikibaseURLModel(
                url=special_statistics_url,
                url_type=WikibaseURLType.SPECIAL_STATISTICS_URL,
            )
        if special_version_url is not None:
            self.special_version_url = WikibaseURLModel(
                url=special_version_url, url_type=WikibaseURLType.SPECIAL_VERSION_URL
            )
