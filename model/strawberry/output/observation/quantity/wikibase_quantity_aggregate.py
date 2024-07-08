"""Aggregate Users"""

import strawberry

from model.strawberry.scalars.big_int import BigInt


@strawberry.type
class WikibaseQuantityAggregate:
    """Quantity Aggregate"""

    total_items: int = strawberry.field(description="Total Items", graphql_type=BigInt)
    total_lexemes: int = strawberry.field(
        description="Total Lexemes", graphql_type=BigInt
    )
    total_properties: int = strawberry.field(
        description="Total Properties", graphql_type=BigInt
    )
    total_triples: int = strawberry.field(
        description="Total Triples", graphql_type=BigInt
    )
    wikibase_count: int = strawberry.field(description="Wikibases with User Data")
