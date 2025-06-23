"""Query"""

import strawberry
from strawberry import Info

from model.enum import WikibaseSoftwareType
from model.strawberry.output import (
    Page,
    PageNumberType,
    PageSizeType,
    WikibaseLanguageAggregateStrawberryModel,
    WikibasePropertyPopularityAggregateCountStrawberryModel,
    WikibaseQuantityAggregateStrawberryModel,
    WikibaseSoftwareVersionDoubleAggregateStrawberryModel,
    WikibaseSoftwareStrawberryModel,
    WikibaseStatisticsAggregateStrawberryModel,
    WikibaseStrawberryModel,
    WikibaseUserAggregateStrawberryModel,
    WikibaseYearCreatedAggregateStrawberryModel,
)
from resolvers import (
    authenticate,
    get_aggregate_created,
    get_aggregate_property_popularity,
    get_aggregate_quantity,
    get_aggregate_statistics,
    get_aggregate_users,
    get_aggregate_version,
    get_language_list,
    get_software_list,
    get_wikibase,
    get_wikibase_list,
)


@strawberry.type
class Query:
    """Query"""

    @strawberry.field(description="Wikibase Instance")
    async def wikibase(self, wikibase_id: int, info: Info) -> WikibaseStrawberryModel:
        """Wikibase Istance"""

        authenticate(info)
        return await get_wikibase(wikibase_id)

    @strawberry.field(description="List of Wikibases")
    async def wikibase_list(
        self, page_number: PageNumberType, page_size: PageSizeType, info: Info
    ) -> Page[WikibaseStrawberryModel]:
        """List of Wikibases"""

        authenticate(info)
        return await get_wikibase_list(page_number, page_size)

    @strawberry.field(description="List of Extensions")
    async def extension_list(
        self, page_number: PageNumberType, page_size: PageSizeType, info: Info
    ) -> Page[WikibaseSoftwareStrawberryModel]:
        """List of Wikibases"""

        authenticate(info)
        return await get_software_list(
                page_number, page_size, WikibaseSoftwareType.EXTENSION
            )

    @strawberry.field(description="Aggregated Year of First Log Date")
    async def aggregate_created(
        self, info: Info
    ) -> list[WikibaseYearCreatedAggregateStrawberryModel]:
        """Aggregated Year of First Log Date"""

        authenticate(info)
        return await get_aggregate_created()

    @strawberry.field(description="Aggregated Extension Popularity")
    async def aggregate_extension_popularity(
        self, page_number: PageNumberType, page_size: PageSizeType, info: Info
    ) -> Page[WikibaseSoftwareVersionDoubleAggregateStrawberryModel]:
        """Aggregated Extension Popularity"""

        authenticate(info)
        return await get_aggregate_version(
                WikibaseSoftwareType.EXTENSION, page_number, page_size
            )

    @strawberry.field(description="Aggregated Language Popularity")
    async def aggregate_language_popularity(
        self, page_number: PageNumberType, page_size: PageSizeType, info: Info
    ) -> Page[WikibaseLanguageAggregateStrawberryModel]:
        """Aggregated Language Popularity"""

        authenticate(info)
        return await get_language_list(page_number, page_size)

    @strawberry.field(description="Aggregated Library Popularity")
    async def aggregate_library_popularity(
        self, page_number: PageNumberType, page_size: PageSizeType, info: Info
    ) -> Page[WikibaseSoftwareVersionDoubleAggregateStrawberryModel]:
        """Aggregated Library Popularity"""

        authenticate(info)
        return await get_aggregate_version(
                WikibaseSoftwareType.LIBRARY, page_number, page_size
            )

    @strawberry.field(description="Aggregated Property Popularity")
    async def aggregate_property_popularity(
        self, page_number: PageNumberType, page_size: PageSizeType, info: Info
    ) -> Page[WikibasePropertyPopularityAggregateCountStrawberryModel]:
        """Aggregated Property Popularity"""

        authenticate(info)
        return await get_aggregate_property_popularity(page_number, page_size)

    @strawberry.field(description="Aggregated Quantity")
    async def aggregate_quantity(
        self, info: Info
    ) -> WikibaseQuantityAggregateStrawberryModel:
        """Aggregated Quantity"""

        authenticate(info)
        return await get_aggregate_quantity()

    @strawberry.field(description="Aggregated Skin Popularity")
    async def aggregate_skin_popularity(
        self, page_number: PageNumberType, page_size: PageSizeType, info: Info
    ) -> Page[WikibaseSoftwareVersionDoubleAggregateStrawberryModel]:
        """Aggregated Skin Popularity"""

        authenticate(info)
        return await get_aggregate_version(
                WikibaseSoftwareType.SKIN, page_number, page_size
            )

    @strawberry.field(description="Aggregated Software Popularity")
    async def aggregate_software_popularity(
        self, page_number: PageNumberType, page_size: PageSizeType, info: Info
    ) -> Page[WikibaseSoftwareVersionDoubleAggregateStrawberryModel]:
        """Aggregated Software Popularity"""

        authenticate(info)
        return await get_aggregate_version(
                WikibaseSoftwareType.SOFTWARE, page_number, page_size
            )

    @strawberry.field(description="Aggregated Statistics")
    async def aggregate_statistics(
        self, info: Info
    ) -> WikibaseStatisticsAggregateStrawberryModel:
        """Aggregated Statistics"""

        authenticate(info)
        return await get_aggregate_statistics()

    @strawberry.field(description="Aggregated Users")
    async def aggregate_users(self, info: Info) -> WikibaseUserAggregateStrawberryModel:
        """Aggregated Users"""

        authenticate(info)
        return await get_aggregate_users()
