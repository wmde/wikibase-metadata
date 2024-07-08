"""Aggregate Users"""

import strawberry


@strawberry.type
class WikibaseUserAggregate:
    total_users: int
    wikibase_count: int
