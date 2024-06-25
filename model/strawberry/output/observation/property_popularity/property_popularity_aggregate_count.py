"""Wikibase Property Popularity Aggregate Count"""

import strawberry

from model.strawberry.output.observation.observation_aggregate import (
    AggregateStrawberryModel,
)
from model.strawberry.output.observation.property_popularity.property_popularity_count import (
    WikibasePropertyPopularityCountStrawberryModel,
)


@strawberry.type
class WikibasePropertyPopularityAggregateCountStrawberryModel(
    WikibasePropertyPopularityCountStrawberryModel, AggregateStrawberryModel
):
    """Wikibase Property Popularity Aggregate Count"""

    def __init__(
        self, id: int, property_url: str, usage_count: int, wikibase_count: int
    ):
        self.id = strawberry.ID(id)
        self.property_url = property_url
        self.usage_count = usage_count
        self.wikibase_count = wikibase_count
