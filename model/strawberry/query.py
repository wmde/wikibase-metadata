"""GraphQL Query"""

from typing import Annotated
import strawberry

from model.database import WikibaseSoftwareTypes
from model.strawberry.output import (
    Page,
    WikibasePropertyPopularityAggregateCountStrawberryModel,
    WikibaseSoftwareVersionDoubleAggregateStrawberryModel,
    WikibaseStrawberryModel,
)
from resolvers import (
    get_aggregate_property_popularity,
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
        page_number: Annotated[
            int, strawberry.argument(description="Page Number - 1-indexed")
        ],
        page_size: Annotated[int, strawberry.argument(description="Page Size")],
    ) -> Page[WikibaseStrawberryModel]:
        return await get_wikibase_list(page_number, page_size)

    @strawberry.field(description="Aggregated Extension Popularity")
    async def aggregate_extension_popularity(
        page_number: Annotated[
            int, strawberry.argument(description="Page Number - 1-indexed")
        ],
        page_size: Annotated[int, strawberry.argument(description="Page Size")],
    ) -> Page[WikibaseSoftwareVersionDoubleAggregateStrawberryModel]:
        return await get_aggregate_version(
            WikibaseSoftwareTypes.extension, page_number, page_size
        )

    @strawberry.field(description="Aggregated Library Popularity")
    async def aggregate_library_popularity(
        page_number: Annotated[
            int, strawberry.argument(description="Page Number - 1-indexed")
        ],
        page_size: Annotated[int, strawberry.argument(description="Page Size")],
    ) -> Page[WikibaseSoftwareVersionDoubleAggregateStrawberryModel]:
        return await get_aggregate_version(
            WikibaseSoftwareTypes.library, page_number, page_size
        )

    @strawberry.field(description="Aggregated Property Popularity")
    async def aggregate_property_popularity(
        page_number: Annotated[
            int, strawberry.argument(description="Page Number - 1-indexed")
        ],
        page_size: Annotated[int, strawberry.argument(description="Page Size")],
    ) -> Page[WikibasePropertyPopularityAggregateCountStrawberryModel]:
        return await get_aggregate_property_popularity(page_number, page_size)

    @strawberry.field(description="Aggregated Skin Popularity")
    async def aggregate_skin_popularity(
        page_number: Annotated[
            int, strawberry.argument(description="Page Number - 1-indexed")
        ],
        page_size: Annotated[int, strawberry.argument(description="Page Size")],
    ) -> Page[WikibaseSoftwareVersionDoubleAggregateStrawberryModel]:
        return await get_aggregate_version(
            WikibaseSoftwareTypes.skin, page_number, page_size
        )

    @strawberry.field(description="Aggregated Software Popularity")
    async def aggregate_software_popularity(
        page_number: Annotated[
            int, strawberry.argument(description="Page Number - 1-indexed")
        ],
        page_size: Annotated[int, strawberry.argument(description="Page Size")],
    ) -> Page[WikibaseSoftwareVersionDoubleAggregateStrawberryModel]:
        return await get_aggregate_version(
            WikibaseSoftwareTypes.software, page_number, page_size
        )
