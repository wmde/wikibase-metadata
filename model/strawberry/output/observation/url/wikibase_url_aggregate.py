"""Aggregate URL Strawberry Model"""

import strawberry

from model.strawberry.scalars import BigInt


@strawberry.type(name="WikibaseURLAggregate")
class WikibaseURLAggregateStrawberryModel:
    """Aggregate URL"""

    total_url_properties: int = strawberry.field(
        description="Total URL Properties", graphql_type=BigInt
    )
    total_url_statements: int = strawberry.field(
        description="Total URL Statements", graphql_type=BigInt
    )

    wikibase_count: int = strawberry.field(description="Wikibases with URL Data")
