"""Wikibase Property Popularity Aggregate Count"""

import strawberry


@strawberry.type
class AggregateStrawberryModel:
    """Aggregate Model"""

    wikibase_count: int = strawberry.field(description="Number of Wikibases Used")
