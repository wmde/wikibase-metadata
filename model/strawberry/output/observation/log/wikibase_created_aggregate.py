"""Wikibase First Log Date Strawberry Model"""

import strawberry

from model.strawberry.scalars.big_int import BigInt


@strawberry.type
class WikibaseYearCreatedAggregated:
    """Wikibases Created in Year"""

    year: int = strawberry.field(description="Year of First Log", graphql_type=BigInt)
    wikibase_count: int = strawberry.field(
        description="Wikibase Count Count", graphql_type=BigInt
    )