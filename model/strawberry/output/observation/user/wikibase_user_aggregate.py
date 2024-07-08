"""Aggregate Users"""

import strawberry

from model.strawberry.scalars.big_int import BigInt


@strawberry.type
class WikibaseUserAggregate:
    """User Aggregate"""

    total_admin: int = strawberry.field(
        description="Total Administrators (estimated from group names)",
        graphql_type=BigInt,
    )
    total_users: int = strawberry.field(
        description="Total Users in all Wikibases (DOES NOT ACCOUNT FOR OVERLAP)",
        graphql_type=BigInt,
    )
    wikibase_count: int = strawberry.field(description="Wikibases with User Data")
