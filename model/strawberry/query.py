"""GraphQL Query"""

import strawberry

from resolvers import (
    get_aggregate_extension_version,
    get_aggregate_library_version,
    get_aggregate_property_popularity,
    get_aggregate_skin_version,
    get_aggregate_software_version,
    get_wikibase,
    get_wikibase_list,
)


@strawberry.type
class Query:
    """GraphQL Query"""

    wikibase = strawberry.field(description="Wikibase Instance", resolver=get_wikibase)
    wikibase_list = strawberry.field(
        description="List of Wikibases", resolver=get_wikibase_list
    )

    aggregate_property_popularity = strawberry.field(
        description="Aggregated Property Popularity - from the most current property popularity for each wikibase, ordered by # wikibases desc, # uses desc",
        resolver=get_aggregate_property_popularity,
    )

    aggregate_extension_popularity = strawberry.field(
        description="Aggregated Extension Popularity",
        resolver=get_aggregate_extension_version,
    )

    aggregate_library_popularity = strawberry.field(
        description="Aggregated Library Popularity",
        resolver=get_aggregate_library_version,
    )

    aggregate_skin_popularity = strawberry.field(
        description="Aggregated Skin Popularity",
        resolver=get_aggregate_skin_version,
    )

    aggregate_software_popularity = strawberry.field(
        description="Aggregated Software Popularity",
        resolver=get_aggregate_software_version,
    )
