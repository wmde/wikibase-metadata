"""Aggregate Year Created Strawberry Model"""

import strawberry

from model.strawberry.scalars import BigInt


@strawberry.type
class WikibaseYearCreatedAggregateStrawberryModel:
    """Aggregate Year Created"""

    year: int = strawberry.field(description="Year of First Log", graphql_type=BigInt)
    wikibase_count: int = strawberry.field(
        description="Wikibase Count Count", graphql_type=BigInt
    )
