"""GraphQL Query"""

from typing import Annotated, List
import strawberry

from model.database import WikibaseSoftwareTypes
from model.strawberry.output import (
    Page,
    WikibasePropertyPopularityAggregateCountStrawberryModel,
    WikibaseQuantityAggregate,
    WikibaseSoftwareVersionDoubleAggregateStrawberryModel,
    WikibaseStrawberryModel,
    WikibaseUserAggregate,
    WikibaseYearCreatedAggregated,
)
from resolvers import (
    get_aggregate_created,
    get_aggregate_property_popularity,
    get_aggregate_quantity,
    get_aggregate_users,
    get_aggregate_version,
    get_wikibase,
    get_wikibase_list,
)


@strawberry.type
class Query:
    """GraphQL Query"""

    wikibase = strawberry.field(description="Wikibase Instance", resolver=get_wikibase)

    @strawberry.field(description="List of Wikibases")
    async def wikibase_list(
        self,
        page_number: Annotated[
            int, strawberry.argument(description="Page Number - 1-indexed")
        ],
        page_size: Annotated[int, strawberry.argument(description="Page Size")],
    ) -> Page[WikibaseStrawberryModel]:
        """List of Wikibases"""

        return await get_wikibase_list(page_number, page_size)

    @strawberry.field(description="Year of First Log Date")
    async def aggregate_created(
        self,
    ) -> List[WikibaseYearCreatedAggregated]:
        """Aggregated Creation Year"""

        return await get_aggregate_created()

    @strawberry.field(description="Aggregated Extension Popularity")
    async def aggregate_extension_popularity(
        self,
        page_number: Annotated[
            int, strawberry.argument(description="Page Number - 1-indexed")
        ],
        page_size: Annotated[int, strawberry.argument(description="Page Size")],
    ) -> Page[WikibaseSoftwareVersionDoubleAggregateStrawberryModel]:
        """Aggregated Extension Popularity"""

        return await get_aggregate_version(
            WikibaseSoftwareTypes.EXTENSION, page_number, page_size
        )

    @strawberry.field(description="Aggregated Library Popularity")
    async def aggregate_library_popularity(
        self,
        page_number: Annotated[
            int, strawberry.argument(description="Page Number - 1-indexed")
        ],
        page_size: Annotated[int, strawberry.argument(description="Page Size")],
    ) -> Page[WikibaseSoftwareVersionDoubleAggregateStrawberryModel]:
        """Aggregated Library Popularity"""

        return await get_aggregate_version(
            WikibaseSoftwareTypes.LIBRARY, page_number, page_size
        )

    @strawberry.field(description="Aggregated Property Popularity")
    async def aggregate_property_popularity(
        self,
        page_number: Annotated[
            int, strawberry.argument(description="Page Number - 1-indexed")
        ],
        page_size: Annotated[int, strawberry.argument(description="Page Size")],
    ) -> Page[WikibasePropertyPopularityAggregateCountStrawberryModel]:
        """Aggregated Property Popularity"""

        return await get_aggregate_property_popularity(page_number, page_size)

    @strawberry.field(description="Aggregated Quantity")
    async def aggregate_quantity(
        self,
    ) -> WikibaseQuantityAggregate:
        """Aggregated Users"""

        return await get_aggregate_quantity()

    @strawberry.field(description="Aggregated Skin Popularity")
    async def aggregate_skin_popularity(
        self,
        page_number: Annotated[
            int, strawberry.argument(description="Page Number - 1-indexed")
        ],
        page_size: Annotated[int, strawberry.argument(description="Page Size")],
    ) -> Page[WikibaseSoftwareVersionDoubleAggregateStrawberryModel]:
        """Aggregated Skin Popularity"""

        return await get_aggregate_version(
            WikibaseSoftwareTypes.SKIN, page_number, page_size
        )

    @strawberry.field(description="Aggregated Software Popularity")
    async def aggregate_software_popularity(
        self,
        page_number: Annotated[
            int, strawberry.argument(description="Page Number - 1-indexed")
        ],
        page_size: Annotated[int, strawberry.argument(description="Page Size")],
    ) -> Page[WikibaseSoftwareVersionDoubleAggregateStrawberryModel]:
        """Aggregated Software Popularity"""

        return await get_aggregate_version(
            WikibaseSoftwareTypes.SOFTWARE, page_number, page_size
        )

    @strawberry.field(description="Aggregated Users")
    async def aggregate_users(
        self,
    ) -> WikibaseUserAggregate:
        """Aggregated Users"""

        return await get_aggregate_users()
