"""Wikibase Property Popularity Aggregate Count"""

import strawberry

from model.strawberry.output.observation.property_popularity.count import (
    WikibasePropertyPopularityCountStrawberryModel,
)


@strawberry.type
class WikibasePropertyPopularityAggregateCountStrawberryModel(
    WikibasePropertyPopularityCountStrawberryModel
):
    """Wikibase Property Popularity Aggregate Count"""

    wikibase_count: int = strawberry.field(description="Number of Wikibases Used")

    def __init__(
        self,
        id: int,  # pylint: disable=redefined-builtin
        property_url: str,
        usage_count: int,
        wikibase_count: int,
    ):
        self.id = strawberry.ID(id)
        self.property_url = property_url
        self.usage_count = usage_count
        self.wikibase_count = wikibase_count