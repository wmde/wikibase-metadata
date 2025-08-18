"""Wikibase Table"""

from typing import Optional
from sqlalchemy import Boolean, Enum, ForeignKey, Integer, String, and_, not_
from sqlalchemy.orm import Mapped, mapped_column, relationship

from model.database.base import ModelBase
from model.database.wikibase_category_model import WikibaseCategoryModel
from model.database.wikibase_language_model import WikibaseLanguageModel
from model.database.wikibase_observation import (
    WikibaseConnectivityObservationModel,
    WikibaseLogMonthObservationModel,
    WikibasePropertyPopularityObservationModel,
    WikibaseQuantityObservationModel,
    WikibaseRecentChangesObservationModel,
    WikibaseSoftwareVersionObservationModel,
    WikibaseStatisticsObservationModel,
    WikibaseTimeToFirstValueObservationModel,
    WikibaseUserObservationModel,
)
from model.database.wikibase_url_model import WikibaseURLModel, join_url
from model.enum import WikibaseType, WikibaseURLType


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

    # LOCATION
    country: Mapped[Optional[str]] = mapped_column("country", String, nullable=True)
    """Country"""

    region: Mapped[Optional[str]] = mapped_column("region", String, nullable=True)
    """Region"""

    # CATEGORY
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

    wikibase_type: Mapped[Optional[WikibaseType]] = mapped_column(
        "wb_type", Enum(WikibaseType), nullable=True
    )
    """Suite, Cloud, Etc"""

    checked: Mapped[bool] = mapped_column("valid", Boolean, nullable=False)
    """Checked"""

    test: Mapped[bool] = mapped_column("test", Boolean, nullable=False)
    """Test Wikibase?"""

    # LANGUAGES
    languages: Mapped[list[WikibaseLanguageModel]] = relationship(
        "WikibaseLanguageModel",
        back_populates="wikibase",
        lazy="selectin",
        overlaps="primary_language,additional_languages,wikibase",
        cascade="delete,delete-orphan,merge,save-update",
    )
    """Languages"""

    primary_language: Mapped[Optional[WikibaseLanguageModel]] = relationship(
        "WikibaseLanguageModel",
        primaryjoin=and_(
            id == WikibaseLanguageModel.wikibase_id, WikibaseLanguageModel.primary
        ),
        lazy="selectin",
        overlaps="languages,additional_languages,wikibase",
    )

    additional_languages: Mapped[list[WikibaseLanguageModel]] = relationship(
        "WikibaseLanguageModel",
        primaryjoin=and_(
            id == WikibaseLanguageModel.wikibase_id, not_(WikibaseLanguageModel.primary)
        ),
        lazy="selectin",
        overlaps="languages,primary_language,wikibase",
    )

    # URLS
    url: Mapped[WikibaseURLModel] = relationship(
        "WikibaseURLModel",
        primaryjoin=and_(
            id == WikibaseURLModel.wikibase_id,
            WikibaseURLType.BASE_URL == WikibaseURLModel.url_type,
        ),
        lazy="selectin",
        overlaps=",".join(
            [
                "article_path",
                "script_path",
                "sparql_endpoint_url",
                "sparql_frontend_url",
                "wikibase",
            ]
        ),
        cascade="all, delete-orphan",
    )
    """Base URL"""

    article_path: Mapped[Optional[WikibaseURLModel]] = relationship(
        "WikibaseURLModel",
        primaryjoin=and_(
            id == WikibaseURLModel.wikibase_id,
            WikibaseURLType.ARTICLE_PATH == WikibaseURLModel.url_type,
        ),
        lazy="selectin",
        overlaps=",".join(
            [
                "script_path",
                "sparql_endpoint_url",
                "sparql_frontend_url",
                "url",
                "wikibase",
            ]
        ),
        cascade="all, delete-orphan",
    )
    """Article Path - `/wiki`"""

    def special_statistics_url(self) -> Optional[str]:
        """Special:Statistics url - `/wiki/Special:Statistics`"""
        if self.article_path is None:
            return None
        return join_url(self.url.url, self.article_path.url, "Special:Statistics")

    def special_version_url(self) -> Optional[str]:
        """Special:Version url - `/wiki/Special:Version`"""
        if self.article_path is None:
            return None
        return join_url(self.url.url, self.article_path.url, "Special:Version")

    script_path: Mapped[Optional[WikibaseURLModel]] = relationship(
        "WikibaseURLModel",
        primaryjoin=and_(
            id == WikibaseURLModel.wikibase_id,
            WikibaseURLType.SCRIPT_PATH == WikibaseURLModel.url_type,
        ),
        lazy="selectin",
        overlaps=",".join(
            [
                "article_path",
                "sparql_endpoint_url",
                "sparql_frontend_url",
                "url",
                "wikibase",
            ]
        ),
        cascade="all, delete-orphan",
    )
    """Script Path - `/w`"""

    def action_api_url(self) -> Optional[str]:
        """Action API URL - `/w/api.php`"""

        if self.script_path is None:
            return None
        return join_url(self.url.url, self.script_path.url, "api.php")

    def index_api_url(self) -> Optional[str]:
        """Index API URL - `/w/index.php`"""

        if self.script_path is None:
            return None
        return join_url(self.url.url, self.script_path.url, "index.php")

    sparql_endpoint_url: Mapped[Optional[WikibaseURLModel]] = relationship(
        "WikibaseURLModel",
        primaryjoin=and_(
            id == WikibaseURLModel.wikibase_id,
            WikibaseURLType.SPARQL_ENDPOINT_URL == WikibaseURLModel.url_type,
        ),
        lazy="selectin",
        overlaps=",".join(
            ["article_path", "script_path", "sparql_frontend_url", "url", "wikibase"]
        ),
        cascade="all, delete-orphan",
    )
    """SPARQL Endpoint"""

    sparql_frontend_url: Mapped[Optional[WikibaseURLModel]] = relationship(
        "WikibaseURLModel",
        primaryjoin=and_(
            id == WikibaseURLModel.wikibase_id,
            WikibaseURLType.SPARQL_FRONTEND_URL == WikibaseURLModel.url_type,
        ),
        lazy="selectin",
        overlaps=",".join(
            ["article_path", "script_path", "sparql_endpoint_url", "url", "wikibase"]
        ),
        cascade="all, delete-orphan",
    )
    """SPARQL Frontend"""

    # OBSERVATIONS
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

    recent_changes_observations: Mapped[list[WikibaseRecentChangesObservationModel]] = (
        relationship(
            "WikibaseRecentChangesObservationModel",
            back_populates="wikibase",
            lazy="select",
        )
    )
    """Recent Changes Observations"""

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

    time_to_first_value_observations: Mapped[
        list[WikibaseTimeToFirstValueObservationModel]
    ] = relationship(
        "WikibaseTimeToFirstValueObservationModel",
        back_populates="wikibase",
        lazy="select",
    )
    """Time to First Value Observations"""

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
        article_path: Optional[str] = None,
        script_path: Optional[str] = None,
        sparql_endpoint_url: Optional[str] = None,
        sparql_frontend_url: Optional[str] = None,
    ):
        self.wikibase_name = wikibase_name
        self.description = description
        self.organization = organization
        self.country = country
        self.region = region
        self.checked = False
        self.test = False

        self.url = WikibaseURLModel(url=base_url, url_type=WikibaseURLType.BASE_URL)

        if primary_language is not None:
            self.set_primary_language(primary_language)

        if additional_languages is not None and len(additional_languages) > 0:
            self.set_additional_languages(additional_languages)

        if article_path is not None:
            self.set_article_path(article_path)

        if script_path is not None:
            self.set_script_path(script_path)

        if sparql_endpoint_url is not None:
            self.set_sparql_endpoint_url(sparql_endpoint_url)

        if sparql_frontend_url is not None:
            self.set_sparql_frontend_url(sparql_frontend_url)

    def set_primary_language(self, primary_language: str):
        """Sets the primary language."""

        # if the language is already the primary one, nothing to do
        if self.primary_language and self.primary_language.language == primary_language:
            return

        # otherwise, lets mark all exising languages as non primary first
        for l in self.languages:
            l.primary = False

        # reuse existing if this language already exists as non primary
        try:
            existing_language_item = next(
                filter(lambda l: l.language == primary_language, self.languages)
            )
            existing_language_item.primary = True

        # add a new one otherwise
        except StopIteration:
            self.languages.append(
                WikibaseLanguageModel(language=primary_language, primary=True)
            )

    def set_additional_languages(self, additional_languages: list[str]):
        """Adds additional languages."""

        # for all the languages to add
        for additional_language in additional_languages:

            # check if it is there, ensure it is non primary, if it is there
            try:
                existing_language_item = next(
                    filter(
                        lambda l, lang=additional_language: l.language == lang,
                        self.languages,
                    )
                )
                existing_language_item.primary = False

            # otherwise add it
            except StopIteration:
                self.languages.append(WikibaseLanguageModel(additional_language))

    def set_article_path(self, article_path: str):
        """Sets the article path URL attribute."""
        if self.article_path is not None:
            self.article_path.url = article_path
        else:
            self.article_path = WikibaseURLModel(
                url=article_path, url_type=WikibaseURLType.ARTICLE_PATH
            )

    def set_script_path(self, script_path: str):
        """Sets the script path URL attribute."""
        if self.script_path is not None:
            self.script_path.url = script_path
        else:
            self.script_path = WikibaseURLModel(
                url=script_path, url_type=WikibaseURLType.SCRIPT_PATH
            )

    def set_sparql_endpoint_url(self, sparql_endpoint_url: str):
        """Sets the SPARQL endpoint URL attribute."""
        if self.sparql_endpoint_url is not None:
            self.sparql_endpoint_url.url = sparql_endpoint_url
        else:
            self.sparql_endpoint_url = WikibaseURLModel(
                url=sparql_endpoint_url,
                url_type=WikibaseURLType.SPARQL_ENDPOINT_URL,
            )

    def set_sparql_frontend_url(self, sparql_frontend_url: str):
        """Sets the SPARQL frontend URL attribute."""
        if self.sparql_frontend_url is not None:
            self.sparql_frontend_url.url = sparql_frontend_url
        else:
            self.sparql_frontend_url = WikibaseURLModel(
                url=sparql_frontend_url, url_type=WikibaseURLType.SPARQL_FRONTEND_URL
            )
