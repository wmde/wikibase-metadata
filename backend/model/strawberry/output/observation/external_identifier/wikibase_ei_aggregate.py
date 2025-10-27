"""Aggregate External Identifier Strawberry Model"""

import strawberry

from model.strawberry.scalars import BigInt


@strawberry.type(name="WikibaseExternalIdentifierAggregate")
class WikibaseExternalIdentifierAggregateStrawberryModel:
    """Aggregate External Identifier"""

    total_external_identifier_properties: int = strawberry.field(
        description="Total External Identifier Properties", graphql_type=BigInt
    )
    total_external_identifier_statements: int = strawberry.field(
        description="Total External Identifier Statements", graphql_type=BigInt
    )
    total_url_properties: int = strawberry.field(
        description="Total URL Properties", graphql_type=BigInt
    )
    total_url_statements: int = strawberry.field(
        description="Total URL Statements", graphql_type=BigInt
    )

    wikibase_count: int = strawberry.field(
        description="Wikibases with External Identifier Data"
    )
