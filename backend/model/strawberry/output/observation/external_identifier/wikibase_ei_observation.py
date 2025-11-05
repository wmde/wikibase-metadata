"""Wikibase External Identifier Data Observation Strawberry Model"""

from typing import Optional
import strawberry

from model.database import WikibaseExternalIdentifierObservationModel
from model.strawberry.output.observation.wikibase_observation import (
    WikibaseObservationStrawberryModel,
)
from model.strawberry.scalars import BigInt


@strawberry.type(name="WikibaseExternalIdentifierObservation")
class WikibaseExternalIdentifierObservationStrawberryModel(
    WikibaseObservationStrawberryModel
):
    """Wikibase External Identifier Data Observation"""

    total_external_identifier_properties: Optional[int] = strawberry.field(
        description="Total External Identifier Properties",
        graphql_type=Optional[BigInt],
    )
    total_external_identifier_statements: Optional[int] = strawberry.field(
        description="Total External Identifier Statements",
        graphql_type=Optional[BigInt],
    )
    total_url_properties: Optional[int] = strawberry.field(
        description="Total URL Properties", graphql_type=Optional[BigInt]
    )
    total_url_statements: Optional[int] = strawberry.field(
        description="Total URL Statements", graphql_type=Optional[BigInt]
    )

    @classmethod
    def marshal(
        cls, model: WikibaseExternalIdentifierObservationModel
    ) -> "WikibaseExternalIdentifierObservationStrawberryModel":
        """Coerce Database Model to Strawberry Model"""

        if model.returned_data and (
            model.total_external_identifier_properties is None
            or model.total_external_identifier_statements is None
            or model.total_url_properties is None
            or model.total_url_statements is None
        ):
            raise ValueError(
                f"External Identifier Observation {model.id}: "
                + "Expected totals when observation returned data"
            )
        return cls(
            id=strawberry.ID(model.id),
            observation_date=model.observation_date,
            returned_data=model.returned_data,
            total_external_identifier_properties=model.total_external_identifier_properties,
            total_external_identifier_statements=model.total_external_identifier_statements,
            total_url_properties=model.total_url_properties,
            total_url_statements=model.total_url_statements,
        )
