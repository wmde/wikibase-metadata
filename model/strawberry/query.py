"""GraphQL Query"""

from typing import List
import strawberry

from model.strawberry.output import WikibaseStrawberryModel
from resolvers import get_aggregate_property_popularity, get_wikibase, get_wikibase_list


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
