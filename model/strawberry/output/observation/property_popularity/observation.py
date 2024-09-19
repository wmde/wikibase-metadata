"""Wikibase Property Popularity Observation Strawberry Model"""

from typing import List
import strawberry

from model.database import (
    WikibasePropertyPopularityCountModel,
    WikibasePropertyPopularityObservationModel,
)
from model.strawberry.output.observation.property_popularity.count import (
    WikibasePropertyPopularityCountStrawberryModel,
)
from model.strawberry.output.observation.wikibase_observation import (
    WikibaseObservationStrawberryModel,
)
from model.strawberry.output.page import Page, PageNumberType, PageSizeType


@strawberry.type
class WikibasePropertyPopularityObservationStrawberryModel(
    WikibaseObservationStrawberryModel
):
    """Wikibase Property Popularity Observation"""

    _pco_list: strawberry.Private[List[WikibasePropertyPopularityCountModel]]

    @strawberry.field(description="Number of Items with Number of Relationships")
    def property_popularity_counts(
        self, page_number: PageNumberType, page_size: PageSizeType
    ) -> Page[WikibasePropertyPopularityCountStrawberryModel]:
        """Number of Items with Number of Relationships"""

        return Page.marshal(
            page_number,
            page_size,
            len(self._pco_list),
            [
                WikibasePropertyPopularityCountStrawberryModel.marshal(o)
                for o in self._pco_list[
                    page_size * (page_number - 1) : page_size * page_number
                ]
            ],
        )

    @classmethod
    def marshal(
        cls, model: WikibasePropertyPopularityObservationModel
    ) -> "WikibasePropertyPopularityObservationStrawberryModel":
        """Coerce Database Model to Strawberry Model"""

        return cls(
            id=strawberry.ID(model.id),
            observation_date=model.observation_date,
            returned_data=model.returned_data,
            _pco_list=sorted(
                model.property_count_observations, key=lambda x: -x.usage_count
            ),
        )
