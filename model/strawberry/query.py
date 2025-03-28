"""Query"""

import strawberry

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

    wikibase = strawberry.field(description="Wikibase Instance", resolver=get_wikibase)
    """Wikibase Instance"""

    @strawberry.field(description="List of Wikibases")
    async def wikibase_list(
        self, page_number: PageNumberType, page_size: PageSizeType
    ) -> Page[WikibaseStrawberryModel]:
        """List of Wikibases"""

        return await get_wikibase_list(page_number, page_size)

    @strawberry.field(description="List of Extensions")
    async def extension_list(
        self, page_number: PageNumberType, page_size: PageSizeType
    ) -> Page[WikibaseSoftwareStrawberryModel]:
        """List of Wikibases"""

        return await get_software_list(
            page_number, page_size, WikibaseSoftwareType.EXTENSION
        )

    @strawberry.field(description="Aggregated Year of First Log Date")
    async def aggregate_created(
        self,
    ) -> list[WikibaseYearCreatedAggregateStrawberryModel]:
        """Aggregated Year of First Log Date"""

        return await get_aggregate_created()

    @strawberry.field(description="Aggregated Extension Popularity")
    async def aggregate_extension_popularity(
        self, page_number: PageNumberType, page_size: PageSizeType
    ) -> Page[WikibaseSoftwareVersionDoubleAggregateStrawberryModel]:
        """Aggregated Extension Popularity"""

        return await get_aggregate_version(
            WikibaseSoftwareType.EXTENSION, page_number, page_size
        )

    @strawberry.field(description="Aggregated Language Popularity")
    async def aggregate_language_popularity(
        self, page_number: PageNumberType, page_size: PageSizeType
    ) -> Page[WikibaseLanguageAggregateStrawberryModel]:
        """Aggregated Language Popularity"""

        return await get_language_list(page_number, page_size)

    @strawberry.field(description="Aggregated Library Popularity")
    async def aggregate_library_popularity(
        self, page_number: PageNumberType, page_size: PageSizeType
    ) -> Page[WikibaseSoftwareVersionDoubleAggregateStrawberryModel]:
        """Aggregated Library Popularity"""

        return await get_aggregate_version(
            WikibaseSoftwareType.LIBRARY, page_number, page_size
        )

    @strawberry.field(description="Aggregated Property Popularity")
    async def aggregate_property_popularity(
        self, page_number: PageNumberType, page_size: PageSizeType
    ) -> Page[WikibasePropertyPopularityAggregateCountStrawberryModel]:
        """Aggregated Property Popularity"""

        return await get_aggregate_property_popularity(page_number, page_size)

    @strawberry.field(description="Aggregated Quantity")
    async def aggregate_quantity(self) -> WikibaseQuantityAggregateStrawberryModel:
        """Aggregated Quantity"""

        return await get_aggregate_quantity()

    @strawberry.field(description="Aggregated Skin Popularity")
    async def aggregate_skin_popularity(
        self, page_number: PageNumberType, page_size: PageSizeType
    ) -> Page[WikibaseSoftwareVersionDoubleAggregateStrawberryModel]:
        """Aggregated Skin Popularity"""

        return await get_aggregate_version(
            WikibaseSoftwareType.SKIN, page_number, page_size
        )

    @strawberry.field(description="Aggregated Software Popularity")
    async def aggregate_software_popularity(
        self, page_number: PageNumberType, page_size: PageSizeType
    ) -> Page[WikibaseSoftwareVersionDoubleAggregateStrawberryModel]:
        """Aggregated Software Popularity"""

        return await get_aggregate_version(
            WikibaseSoftwareType.SOFTWARE, page_number, page_size
        )

    @strawberry.field(description="Aggregated Statistics")
    async def aggregate_statistics(self) -> WikibaseStatisticsAggregateStrawberryModel:
        """Aggregated Statistics"""

        return await get_aggregate_statistics()

    @strawberry.field(description="Aggregated Users")
    async def aggregate_users(self) -> WikibaseUserAggregateStrawberryModel:
        """Aggregated Users"""

        return await get_aggregate_users()
