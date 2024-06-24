"""Wikibase Property Popularity Observation Strawberry Model"""

from typing import List
import strawberry

from model.database import (
    WikibasePropertyPopularityObservationModel,
)
from model.strawberry.output.observation.property_popularity.property_popularity_count import (
    WikibasePropertyPopularityCountStrawberryModel,
)
from model.strawberry.output.observation.wikibase_observation import (
    WikibaseObservationStrawberryModel,
)


@strawberry.type
class WikibasePropertyPopularityObservationStrawberryModel(
    WikibaseObservationStrawberryModel
):
    """Wikibase Property Popularity Observation"""

    property_popularity_counts: List[
        WikibasePropertyPopularityCountStrawberryModel
    ] = strawberry.field(description="Number of Items with Number of Relationships")

    @classmethod
    def marshal(
        cls, model: WikibasePropertyPopularityObservationModel
    ) -> "WikibasePropertyPopularityObservationStrawberryModel":
        """Coerce Database Model to Strawberry Model"""

        return cls(
            id=strawberry.ID(model.id),
            observation_date=model.observation_date,
            returned_data=model.returned_data,
            property_popularity_counts=sorted(
                [
                    WikibasePropertyPopularityCountStrawberryModel.marshal(o)
                    for o in model.property_count_observations
                ],
                key=lambda x: x.usage_count,
                reverse=True,
            ),
        )
