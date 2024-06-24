"""Wikibase Property Popularity Aggregate Count"""

import strawberry

from model.strawberry.output.observation.property_popularity.property_popularity_count import (
    WikibasePropertyPopularityCountStrawberryModel,
)


@strawberry.type
class WikibasePropertyPopularityAggregateCountStrawberryModel(
    WikibasePropertyPopularityCountStrawberryModel
):
    """Wikibase Property Popularity Aggregate Count"""

    wikibase_count: int = strawberry.field(description="Number of Wikibases Used")

    def __init__(self, id: strawberry.ID, property_url: str):
        self.id = id
        self.property_url = property_url
        self.usage_count = 0
        self.wikibase_count = 0
