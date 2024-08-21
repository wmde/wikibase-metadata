"""Wikibase Quantity Data Observation Strawberry Model"""

from typing import Optional
import strawberry

from model.database import WikibaseQuantityObservationModel
from model.strawberry.output.observation.wikibase_observation import (
    WikibaseObservationStrawberryModel,
)
from model.strawberry.scalars import BigInt


@strawberry.type
class WikibaseQuantityObservationStrawberryModel(WikibaseObservationStrawberryModel):
    """Wikibase Quantity Data Observation"""

    total_items: Optional[int] = strawberry.field(
        description="Total Items", graphql_type=Optional[BigInt]
    )
    total_lexemes: Optional[int] = strawberry.field(
        description="Total Lexemes", graphql_type=Optional[BigInt]
    )
    total_properties: Optional[int] = strawberry.field(
        description="Total Properties", graphql_type=Optional[BigInt]
    )
    total_triples: Optional[int] = strawberry.field(
        description="Total Triples", graphql_type=Optional[BigInt]
    )

    @classmethod
    def marshal(
        cls, model: WikibaseQuantityObservationModel
    ) -> "WikibaseQuantityObservationStrawberryModel":
        """Coerce Database Model to Strawberry Model"""

        if model.returned_data and (
            model.total_items is None
            or model.total_lexemes is None
            or model.total_properties is None
        ):
            raise ValueError(
                f"Quantity Observation {model.id}: Expected totals when observation returned data"
            )
        return cls(
            id=strawberry.ID(model.id),
            observation_date=model.observation_date,
            returned_data=model.returned_data,
            total_items=model.total_items,
            total_lexemes=model.total_lexemes,
            total_properties=model.total_properties,
            total_triples=model.total_triples,
        )
