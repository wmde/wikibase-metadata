"""Wikibase Instance Strawberry Model"""

from typing import Optional
import strawberry

from model.database import WikibaseModel
from model.enum.wikibase_category_enum import wikibase_category_name
from model.strawberry.output.observation import (
    WikibaseConnectivityObservationStrawberryModel,
    WikibaseLogObservationStrawberryModel,
    WikibaseObservationSetStrawberryModel,
    WikibasePropertyPopularityObservationStrawberryModel,
    WikibaseQuantityObservationStrawberryModel,
    WikibaseSoftwareVersionObservationStrawberryModel,
    WikibaseStatisticsObservationStrawberryModel,
    WikibaseUserObservationStrawberryModel,
)
from model.strawberry.output.wikibase_location import WikibaseLocationStrawberryModel
from model.strawberry.output.wikibase_url_set import WikibaseURLSetStrawberryModel


@strawberry.type
class WikibaseStrawberryModel:
    """Wikibase Instance"""

    id: strawberry.ID
    title: str = strawberry.field(description="Wikibase Name")
    organization: Optional[str] = strawberry.field(description="Organization")
    description: Optional[str] = strawberry.field(description="Description")
    category: Optional[str] = strawberry.field(description="Wikibase Category")

    location: WikibaseLocationStrawberryModel = strawberry.field(
        description="Wikibase Location"
    )

    urls: WikibaseURLSetStrawberryModel = strawberry.field(description="URLs")

    connectivity_observations: WikibaseObservationSetStrawberryModel[
        WikibaseConnectivityObservationStrawberryModel
    ] = strawberry.field(description="Connectivity Data")
    log_observations: WikibaseObservationSetStrawberryModel[
        WikibaseLogObservationStrawberryModel
    ] = strawberry.field(description="Log Data")
    property_popularity_observations: WikibaseObservationSetStrawberryModel[
        WikibasePropertyPopularityObservationStrawberryModel
    ] = strawberry.field(description="Property Popularity Data")
    quantity_observations: WikibaseObservationSetStrawberryModel[
        WikibaseQuantityObservationStrawberryModel
    ] = strawberry.field(description="Quantity Data")
    software_version_observations: WikibaseObservationSetStrawberryModel[
        WikibaseSoftwareVersionObservationStrawberryModel
    ] = strawberry.field(description="Software Version Data")
    statistics_observations: WikibaseObservationSetStrawberryModel[
        WikibaseStatisticsObservationStrawberryModel
    ] = strawberry.field(description="Statistics Data")
    user_observations: WikibaseObservationSetStrawberryModel[
        WikibaseUserObservationStrawberryModel
    ] = strawberry.field(description="User Data")

    @classmethod
    def marshal(cls, model: WikibaseModel) -> "WikibaseStrawberryModel":
        """Coerce Database Model to Strawberry Model"""

        return cls(
            id=strawberry.ID(model.id),
            title=model.wikibase_name,
            organization=model.organization,
            description=model.description,
            category=(
                wikibase_category_name(model.category.category)
                if model.category is not None
                else None
            ),
            location=WikibaseLocationStrawberryModel.marshal(model),
            urls=WikibaseURLSetStrawberryModel.marshal(model),
            connectivity_observations=WikibaseObservationSetStrawberryModel.marshal(
                [
                    WikibaseConnectivityObservationStrawberryModel.marshal(o)
                    for o in model.connectivity_observations
                ]
            ),
            log_observations=WikibaseObservationSetStrawberryModel.marshal(
                [
                    WikibaseLogObservationStrawberryModel.marshal(o)
                    for o in model.log_observations
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
            software_version_observations=WikibaseObservationSetStrawberryModel.marshal(
                [
                    WikibaseSoftwareVersionObservationStrawberryModel.marshal(o)
                    for o in model.software_version_observations
                ]
            ),
            statistics_observations=WikibaseObservationSetStrawberryModel.marshal(
                [
                    WikibaseStatisticsObservationStrawberryModel.marshal(o)
                    for o in model.statistics_observations
                ]
            ),
            user_observations=WikibaseObservationSetStrawberryModel.marshal(
                [
                    WikibaseUserObservationStrawberryModel.marshal(o)
                    for o in model.user_observations
                ]
            ),
        )
