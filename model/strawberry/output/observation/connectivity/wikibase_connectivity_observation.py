"""Wikibase Connectivity Data Observation Strawberry Model"""

from typing import List, Optional
import strawberry

from model.database import (
    WikibaseConnectivityObservationModel,
    WikibaseConnectivityObservationItemRelationshipCountModel,
    WikibaseConnectivityObservationObjectRelationshipCountModel,
)
from model.strawberry.output.observation.connectivity.relationship_count import (
    WikibaseConnectivityObservationItemRelationshipCountStrawberryModel,
    WikibaseConnectivityObservationObjectRelationshipCountStrawberryModel,
)
from model.strawberry.output.observation.wikibase_observation import (
    WikibaseObservationStrawberryModel,
)
from model.strawberry.output.page import (
    Page,
    PageNumberType,
    PageSizeType,
    page_records,
)
from model.strawberry.scalars import BigInt


@strawberry.type
class WikibaseConnectivityObservationStrawberryModel(
    WikibaseObservationStrawberryModel
):
    """Wikibase Connectivity Data Observation"""

    average_connected_distance: Optional[float] = strawberry.field(
        description="Average Distance of Connected Items"
    )
    connectivity: Optional[float] = strawberry.field(
        description="""Number of Unique Item -> Item Connections (regardless of steps) /
        Number of Items Squared"""
    )
    returned_links: Optional[int] = strawberry.field(
        description="Number of Non-Unique Item -> Item Links Returned",
        graphql_type=Optional[BigInt],
    )

    _relationship_item_counts: strawberry.Private[
        List[WikibaseConnectivityObservationItemRelationshipCountModel]
    ]

    @strawberry.field(description="Number of Items with Number of Relationships")
    def relationship_item_counts(
        self, page_number: PageNumberType, page_size: PageSizeType
    ) -> Page[WikibaseConnectivityObservationItemRelationshipCountStrawberryModel]:
        """Number of Items with Number of Relationships"""

        return Page.marshal(
            page_number,
            page_size,
            len(self._relationship_item_counts),
            [
                WikibaseConnectivityObservationItemRelationshipCountStrawberryModel.marshal(
                    o
                )
                for o in page_records(
                    self._relationship_item_counts, page_number, page_size
                )
            ],
        )

    _relationship_object_counts: strawberry.Private[
        List[WikibaseConnectivityObservationObjectRelationshipCountModel]
    ]

    @strawberry.field(description="Number of Objects with Number of Relationships")
    def relationship_object_counts(
        self, page_number: PageNumberType, page_size: PageSizeType
    ) -> Page[WikibaseConnectivityObservationObjectRelationshipCountStrawberryModel]:
        """Number of Objects with Number of Relationships"""

        return Page.marshal(
            page_number,
            page_size,
            len(self._relationship_object_counts),
            [
                WikibaseConnectivityObservationObjectRelationshipCountStrawberryModel.marshal(
                    o
                )
                for o in page_records(
                    self._relationship_object_counts, page_number, page_size
                )
            ],
        )

    @strawberry.field(
        description="Number of Unique Item -> Item Connections (direct or indirect)",
        graphql_type=Optional[BigInt],
    )
    def total_connections(self):
        """Item -> Item Connections; assert that math works"""

        if self.returned_data:
            item_sum = sum(
                i.item_count * i.relationship_count
                for i in self._relationship_item_counts
            )
            object_sum = sum(
                o.object_count * o.relationship_count
                for o in self._relationship_object_counts
            )
            assert item_sum == object_sum, "Error: Math Has Stopped Working"
            return item_sum
        return None

    @classmethod
    def marshal(
        cls, model: WikibaseConnectivityObservationModel
    ) -> "WikibaseConnectivityObservationStrawberryModel":
        """Coerce Database Model to Strawberry Model"""

        return cls(
            id=strawberry.ID(model.id),
            observation_date=model.observation_date,
            returned_data=model.returned_data,
            average_connected_distance=model.average_connected_distance,
            connectivity=model.connectivity,
            returned_links=model.returned_links,
            _relationship_item_counts=sorted(
                model.item_relationship_count_observations, key=lambda x: x.id
            ),
            _relationship_object_counts=sorted(
                model.object_relationship_count_observations, key=lambda x: x.id
            ),
        )
