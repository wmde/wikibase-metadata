"""Wikibase Instance Strawberry Model"""

from typing import Optional
from sqlalchemy import select
from sqlalchemy.orm import joinedload
import strawberry

from data.database_connection import get_async_session
from model.database import WikibaseModel
from model.enum import WikibaseCategory, WikibaseType
from model.strawberry.output.observation import (
    WikibaseConnectivityObservationStrawberryModel,
    WikibaseExternalIdentifierObservationStrawberryModel,
    WikibaseLogObservationStrawberryModel,
    WikibaseObservationSetStrawberryModel,
    WikibasePropertyPopularityObservationStrawberryModel,
    WikibaseQuantityObservationStrawberryModel,
    WikibaseRecentChangesObservationStrawberryModel,
    WikibaseSoftwareVersionObservationStrawberryModel,
    WikibaseStatisticsObservationStrawberryModel,
    WikibaseTimeToFirstValueObservationStrawberryModel,
    WikibaseUserObservationStrawberryModel,
)
from model.strawberry.output.wikibase_language_set import (
    WikibaseLanguageSetStrawberryModel,
)
from model.strawberry.output.wikibase_location import WikibaseLocationStrawberryModel
from model.strawberry.output.wikibase_url_set import WikibaseURLSetStrawberryModel


@strawberry.type(name="Wikibase")
class WikibaseStrawberryModel:
    """Wikibase Instance"""

    id: strawberry.ID
    title: str = strawberry.field(description="Wikibase Name")
    organization: Optional[str] = strawberry.field(description="Organization")
    description: Optional[str] = strawberry.field(description="Description")
    category: Optional[WikibaseCategory] = strawberry.field(
        description="Wikibase Category"
    )
    wikibase_type: WikibaseType = strawberry.field(description="Cloud, Suite, Other")

    location: WikibaseLocationStrawberryModel = strawberry.field(
        description="Wikibase Location"
    )

    languages: WikibaseLanguageSetStrawberryModel = strawberry.field(
        description="Languages"
    )

    urls: WikibaseURLSetStrawberryModel = strawberry.field(description="URLs")

    @strawberry.field(description="Connectivity Data")
    async def connectivity_observations(
        self,
    ) -> WikibaseObservationSetStrawberryModel[
        WikibaseConnectivityObservationStrawberryModel
    ]:
        """Summon Connectivity Data on Specific Request"""

        async with get_async_session() as async_session:
            model = (
                (
                    await async_session.scalars(
                        select(WikibaseModel)
                        .options(joinedload(WikibaseModel.connectivity_observations))
                        .where(WikibaseModel.id == int(self.id))
                    )
                )
                .unique()
                .one()
            )
            return WikibaseObservationSetStrawberryModel.marshal(
                [
                    WikibaseConnectivityObservationStrawberryModel.marshal(o)
                    for o in model.connectivity_observations
                ]
            )

    @strawberry.field(description="External Identifier Data")
    async def external_identifier_observations(
        self,
    ) -> WikibaseObservationSetStrawberryModel[
        WikibaseExternalIdentifierObservationStrawberryModel
    ]:
        """Summon External Identifier Data on Specific Request"""

        async with get_async_session() as async_session:
            model = (
                (
                    await async_session.scalars(
                        select(WikibaseModel)
                        .options(
                            joinedload(WikibaseModel.external_identifier_observations)
                        )
                        .where(WikibaseModel.id == int(self.id))
                    )
                )
                .unique()
                .one()
            )
            return WikibaseObservationSetStrawberryModel.marshal(
                [
                    WikibaseExternalIdentifierObservationStrawberryModel.marshal(o)
                    for o in model.external_identifier_observations
                ]
            )

    @strawberry.field(description="Log Data")
    async def log_observations(self) -> WikibaseLogObservationStrawberryModel:
        """Summon Log Data on Specific Request"""

        async with get_async_session() as async_session:
            model = (
                (
                    await async_session.scalars(
                        select(WikibaseModel)
                        .options(joinedload(WikibaseModel.log_month_observations))
                        .where(WikibaseModel.id == int(self.id))
                    )
                )
                .unique()
                .one()
            )
            return WikibaseLogObservationStrawberryModel.marshal(model)

    @strawberry.field(description="Property Popularity Data")
    async def property_popularity_observations(
        self,
    ) -> WikibaseObservationSetStrawberryModel[
        WikibasePropertyPopularityObservationStrawberryModel
    ]:
        """Summon Property Popularity Data on Specific Request"""

        async with get_async_session() as async_session:
            model = (
                (
                    await async_session.scalars(
                        select(WikibaseModel)
                        .options(
                            joinedload(WikibaseModel.property_popularity_observations)
                        )
                        .where(WikibaseModel.id == int(self.id))
                    )
                )
                .unique()
                .one()
            )
            return WikibaseObservationSetStrawberryModel.marshal(
                [
                    WikibasePropertyPopularityObservationStrawberryModel.marshal(o)
                    for o in model.property_popularity_observations
                ]
            )

    @strawberry.field(description="Quantity Data")
    async def quantity_observations(
        self,
    ) -> WikibaseObservationSetStrawberryModel[
        WikibaseQuantityObservationStrawberryModel
    ]:
        """Summon Quantity Data on Specific Request"""

        async with get_async_session() as async_session:
            model = (
                (
                    await async_session.scalars(
                        select(WikibaseModel)
                        .options(joinedload(WikibaseModel.quantity_observations))
                        .where(WikibaseModel.id == int(self.id))
                    )
                )
                .unique()
                .one()
            )
            return WikibaseObservationSetStrawberryModel.marshal(
                [
                    WikibaseQuantityObservationStrawberryModel.marshal(o)
                    for o in model.quantity_observations
                ]
            )

    @strawberry.field(description="Recent Changes Data")
    async def recent_changes_observations(
        self,
    ) -> WikibaseObservationSetStrawberryModel[
        WikibaseRecentChangesObservationStrawberryModel
    ]:
        """Summon Recent Changes Data on Specific Request"""

        async with get_async_session() as async_session:
            model = (
                (
                    await async_session.scalars(
                        select(WikibaseModel)
                        .options(joinedload(WikibaseModel.recent_changes_observations))
                        .where(WikibaseModel.id == int(self.id))
                    )
                )
                .unique()
                .one()
            )
            return WikibaseObservationSetStrawberryModel.marshal(
                [
                    WikibaseRecentChangesObservationStrawberryModel.marshal(o)
                    for o in model.recent_changes_observations
                ]
            )

    @strawberry.field(description="Software Version Data")
    async def software_version_observations(
        self,
    ) -> WikibaseObservationSetStrawberryModel[
        WikibaseSoftwareVersionObservationStrawberryModel
    ]:
        """Summon Software Version Data on Specific Request"""

        async with get_async_session() as async_session:
            model = (
                (
                    await async_session.scalars(
                        select(WikibaseModel)
                        .options(
                            joinedload(WikibaseModel.software_version_observations)
                        )
                        .where(WikibaseModel.id == int(self.id))
                    )
                )
                .unique()
                .one()
            )
            return WikibaseObservationSetStrawberryModel.marshal(
                [
                    WikibaseSoftwareVersionObservationStrawberryModel.marshal(o)
                    for o in model.software_version_observations
                ]
            )

    @strawberry.field(description="Statistics Data")
    async def statistics_observations(
        self,
    ) -> WikibaseObservationSetStrawberryModel[
        WikibaseStatisticsObservationStrawberryModel
    ]:
        """Summon Statistics Data on Specific Request"""

        async with get_async_session() as async_session:
            model = (
                (
                    await async_session.scalars(
                        select(WikibaseModel)
                        .options(joinedload(WikibaseModel.statistics_observations))
                        .where(WikibaseModel.id == int(self.id))
                    )
                )
                .unique()
                .one()
            )
            return WikibaseObservationSetStrawberryModel.marshal(
                [
                    WikibaseStatisticsObservationStrawberryModel.marshal(o)
                    for o in model.statistics_observations
                ]
            )

    @strawberry.field(description="Time to First Value Data")
    async def time_to_first_value_observations(
        self,
    ) -> WikibaseObservationSetStrawberryModel[
        WikibaseTimeToFirstValueObservationStrawberryModel
    ]:
        """Summon Time to First Value Data on Specific Request"""

        async with get_async_session() as async_session:
            model = (
                (
                    await async_session.scalars(
                        select(WikibaseModel)
                        .options(
                            joinedload(WikibaseModel.time_to_first_value_observations)
                        )
                        .where(WikibaseModel.id == int(self.id))
                    )
                )
                .unique()
                .one()
            )
            return WikibaseObservationSetStrawberryModel.marshal(
                [
                    WikibaseTimeToFirstValueObservationStrawberryModel.marshal(o)
                    for o in model.time_to_first_value_observations
                ]
            )

    @strawberry.field(description="User Data")
    async def user_observations(
        self,
    ) -> WikibaseObservationSetStrawberryModel[WikibaseUserObservationStrawberryModel]:
        """Summon User Data on Specific Request"""

        async with get_async_session() as async_session:
            model = (
                (
                    await async_session.scalars(
                        select(WikibaseModel)
                        .options(joinedload(WikibaseModel.user_observations))
                        .where(WikibaseModel.id == int(self.id))
                    )
                )
                .unique()
                .one()
            )
            return WikibaseObservationSetStrawberryModel.marshal(
                [
                    WikibaseUserObservationStrawberryModel.marshal(o)
                    for o in model.user_observations
                ]
            )

    @classmethod
    def marshal(cls, model: WikibaseModel) -> "WikibaseStrawberryModel":
        """Coerce Database Model to Strawberry Model"""

        return cls(
            id=strawberry.ID(model.id),
            title=model.wikibase_name,
            organization=model.organization,
            description=model.description,
            category=model.category.category if model.category is not None else None,
            location=WikibaseLocationStrawberryModel.marshal(model),
            languages=WikibaseLanguageSetStrawberryModel.marshal(model),
            urls=WikibaseURLSetStrawberryModel.marshal(model),
            wikibase_type=model.wikibase_type or WikibaseType.UNKNOWN,
        )
