"""Wikibase URL Observation Strawberry Model"""

from typing import Optional
import strawberry

from model.database import WikibaseURLObservationModel
from model.strawberry.output.observation.wikibase_observation import (
    WikibaseObservationStrawberryModel,
)
from model.strawberry.scalars import BigInt


@strawberry.type(name="WikibaseURLObservation")
class WikibaseURLObservationStrawberryModel(WikibaseObservationStrawberryModel):
    """Wikibase URL Data Observation"""

    total_url_properties: Optional[int] = strawberry.field(
        description="Total URL Properties", graphql_type=Optional[BigInt]
    )
    total_url_statements: Optional[int] = strawberry.field(
        description="Total URL Statements", graphql_type=Optional[BigInt]
    )

    @classmethod
    def marshal(
        cls, model: WikibaseURLObservationModel
    ) -> "WikibaseURLObservationStrawberryModel":
        """Coerce Database Model to Strawberry Model"""

        return cls(
            id=strawberry.ID(model.id),
            observation_date=model.observation_date,
            returned_data=model.returned_data,
            total_url_properties=model.total_url_properties,
            total_url_statements=model.total_url_statements,
        )
