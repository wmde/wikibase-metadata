"""Query"""

from typing import Optional
import strawberry
from strawberry import Info

from model.enum import WikibaseSoftwareType
from model.strawberry.input import WikibaseFilterInput
from model.strawberry.output import (
    Page,
    PageNumberType,
    PageSizeType,
    WikibaseExternalIdentifierAggregateStrawberryModel,
    WikibaseLanguageAggregateStrawberryModel,
    WikibasePropertyPopularityAggregateCountStrawberryModel,
    WikibaseQuantityAggregateStrawberryModel,
    WikibaseRecentChangesAggregateStrawberryModel,
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
    get_aggregate_external_identifier,
    get_aggregate_property_popularity,
    get_aggregate_quantity,
    get_aggregate_recent_changes,
    get_aggregate_statistics,
    get_aggregate_users,
    get_aggregate_version,
    get_language_list,
    get_software_list,
    get_wikibase,
    get_wikibase_page,
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
        self,
        info: Info,
        page_number: PageNumberType,
        page_size: PageSizeType,
        wikibase_filter: Optional[WikibaseFilterInput] = None,
    ) -> Page[WikibaseStrawberryModel]:
        """List of Wikibases"""

        authenticate(info)
        return await get_wikibase_page(
            page_number=page_number,
            page_size=page_size,
            wikibase_filter=wikibase_filter,
        )

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
        self, info: Info, wikibase_filter: Optional[WikibaseFilterInput] = None
    ) -> list[WikibaseYearCreatedAggregateStrawberryModel]:
        """Aggregated Year of First Log Date"""

        authenticate(info)
        return await get_aggregate_created(wikibase_filter)

    @strawberry.field(description="Aggregated Extension Popularity")
    async def aggregate_extension_popularity(
        self,
        info: Info,
        page_number: PageNumberType,
        page_size: PageSizeType,
        wikibase_filter: Optional[WikibaseFilterInput] = None,
    ) -> Page[WikibaseSoftwareVersionDoubleAggregateStrawberryModel]:
        """Aggregated Extension Popularity"""

        authenticate(info)
        return await get_aggregate_version(
            software_type=WikibaseSoftwareType.EXTENSION,
            page_number=page_number,
            page_size=page_size,
            wikibase_filter=wikibase_filter,
        )

    @strawberry.field(description="Aggregated External Identifier")
    async def aggregate_external_identifier(
        self, info: Info, wikibase_filter: Optional[WikibaseFilterInput] = None
    ) -> WikibaseExternalIdentifierAggregateStrawberryModel:
        """Aggregated External Identifier"""

        authenticate(info)
        return await get_aggregate_external_identifier(wikibase_filter)

    @strawberry.field(description="Aggregated Language Popularity")
    async def aggregate_language_popularity(
        self,
        info: Info,
        page_number: PageNumberType,
        page_size: PageSizeType,
        wikibase_filter: Optional[WikibaseFilterInput] = None,
    ) -> Page[WikibaseLanguageAggregateStrawberryModel]:
        """Aggregated Language Popularity"""

        authenticate(info)
        return await get_language_list(
            page_number=page_number,
            page_size=page_size,
            wikibase_filter=wikibase_filter,
        )

    @strawberry.field(description="Aggregated Library Popularity")
    async def aggregate_library_popularity(
        self,
        info: Info,
        page_number: PageNumberType,
        page_size: PageSizeType,
        wikibase_filter: Optional[WikibaseFilterInput] = None,
    ) -> Page[WikibaseSoftwareVersionDoubleAggregateStrawberryModel]:
        """Aggregated Library Popularity"""

        authenticate(info)
        return await get_aggregate_version(
            software_type=WikibaseSoftwareType.LIBRARY,
            page_number=page_number,
            page_size=page_size,
            wikibase_filter=wikibase_filter,
        )

    @strawberry.field(description="Aggregated Property Popularity")
    async def aggregate_property_popularity(
        self,
        info: Info,
        page_number: PageNumberType,
        page_size: PageSizeType,
        wikibase_filter: Optional[WikibaseFilterInput] = None,
    ) -> Page[WikibasePropertyPopularityAggregateCountStrawberryModel]:
        """Aggregated Property Popularity"""

        authenticate(info)
        return await get_aggregate_property_popularity(
            page_number=page_number,
            page_size=page_size,
            wikibase_filter=wikibase_filter,
        )

    @strawberry.field(description="Aggregated Quantity")
    async def aggregate_quantity(
        self, info: Info, wikibase_filter: Optional[WikibaseFilterInput] = None
    ) -> WikibaseQuantityAggregateStrawberryModel:
        """Aggregated Quantity"""

        authenticate(info)
        return await get_aggregate_quantity(wikibase_filter)

    @strawberry.field(description="Aggregated Recent Changes")
    async def aggregate_recent_changes(
        self, info: Info, wikibase_filter: Optional[WikibaseFilterInput] = None
    ) -> WikibaseRecentChangesAggregateStrawberryModel:
        """Aggregated Recent Changes"""

        authenticate(info)
        return await get_aggregate_recent_changes(wikibase_filter)

    @strawberry.field(description="Aggregated Skin Popularity")
    async def aggregate_skin_popularity(
        self,
        info: Info,
        page_number: PageNumberType,
        page_size: PageSizeType,
        wikibase_filter: Optional[WikibaseFilterInput] = None,
    ) -> Page[WikibaseSoftwareVersionDoubleAggregateStrawberryModel]:
        """Aggregated Skin Popularity"""

        authenticate(info)
        return await get_aggregate_version(
            software_type=WikibaseSoftwareType.SKIN,
            page_number=page_number,
            page_size=page_size,
            wikibase_filter=wikibase_filter,
        )

    @strawberry.field(description="Aggregated Software Popularity")
    async def aggregate_software_popularity(
        self,
        info: Info,
        page_number: PageNumberType,
        page_size: PageSizeType,
        wikibase_filter: Optional[WikibaseFilterInput] = None,
    ) -> Page[WikibaseSoftwareVersionDoubleAggregateStrawberryModel]:
        """Aggregated Software Popularity"""

        authenticate(info)
        return await get_aggregate_version(
            software_type=WikibaseSoftwareType.SOFTWARE,
            page_number=page_number,
            page_size=page_size,
            wikibase_filter=wikibase_filter,
        )

    @strawberry.field(description="Aggregated Statistics")
    async def aggregate_statistics(
        self, info: Info, wikibase_filter: Optional[WikibaseFilterInput] = None
    ) -> WikibaseStatisticsAggregateStrawberryModel:
        """Aggregated Statistics"""

        authenticate(info)
        return await get_aggregate_statistics(wikibase_filter)

    @strawberry.field(description="Aggregated Users")
    async def aggregate_users(
        self, info: Info, wikibase_filter: Optional[WikibaseFilterInput] = None
    ) -> WikibaseUserAggregateStrawberryModel:
        """Aggregated Users"""

        authenticate(info)
        return await get_aggregate_users(wikibase_filter)
