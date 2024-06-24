"""Wikibase Instance Strawberry Model"""

import strawberry

from model.database import WikibaseModel
from model.strawberry.output.observation import (
    WikibaseConnectivityObservationStrawberryModel,
    WikibaseObservationSetStrawberryModel,
    WikibasePropertyPopularityObservationStrawberryModel,
    WikibaseQuantityObservationStrawberryModel,
    WikibaseUserObservationStrawberryModel,
)
from model.strawberry.output.wikibase_url_set import WikibaseURLSetStrawberryModel


@strawberry.type
class WikibaseStrawberryModel:
    """Wikibase Instance"""

    id: strawberry.ID
    urls: WikibaseURLSetStrawberryModel = strawberry.field(description="URLs")
    connectivity_observations: WikibaseObservationSetStrawberryModel[
        WikibaseConnectivityObservationStrawberryModel
    ] = strawberry.field(description="Connectivity Data")
    property_popularity_observations: WikibaseObservationSetStrawberryModel[
        WikibasePropertyPopularityObservationStrawberryModel
    ] = strawberry.field(description="Property Popularity Data")
    quantity_observations: WikibaseObservationSetStrawberryModel[
        WikibaseQuantityObservationStrawberryModel
    ] = strawberry.field(description="Quantity Data")
    user_observations: WikibaseObservationSetStrawberryModel[
        WikibaseUserObservationStrawberryModel
    ] = strawberry.field(description="User Data")

    @classmethod
    def marshal(cls, model: WikibaseModel) -> "WikibaseStrawberryModel":
        """Coerce Database Model to Strawberry Model"""

        return cls(
            id=strawberry.ID(model.id),
            urls=WikibaseURLSetStrawberryModel.marshal(model),
            connectivity_observations=WikibaseObservationSetStrawberryModel.marshal(
                [
                    WikibaseConnectivityObservationStrawberryModel.marshal(o)
                    for o in model.connectivity_observations
                ]
            ),
            property_popularity_observations=WikibaseObservationSetStrawberryModel.marshal(
                [
                    WikibasePropertyPopularityObservationStrawberryModel.marshal(o)
                    for o in model.property_popularity_observations
                ]
            ),
            quantity_observations=WikibaseObservationSetStrawberryModel.marshal(
                [
                    WikibaseQuantityObservationStrawberryModel.marshal(o)
                    for o in model.quantity_observations
                ]
            ),
            user_observations=WikibaseObservationSetStrawberryModel.marshal(
                [
                    WikibaseUserObservationStrawberryModel.marshal(o)
                    for o in model.user_observations
                ]
            ),
        )
