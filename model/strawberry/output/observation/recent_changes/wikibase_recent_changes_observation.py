"""Wikibase Recent Changes Observation Strawberry Model"""

from datetime import datetime
from typing import Optional
import strawberry

from model.database import WikibaseRecentChangesObservationModel
from model.strawberry.output.observation.wikibase_observation import (
    WikibaseObservationStrawberryModel,
)
from model.strawberry.scalars import BigInt


@strawberry.type(name="WikibaseRecentChangesObservation")
class WikibaseRecentChangesObservationStrawberryModel(
    WikibaseObservationStrawberryModel
):
    """Wikibase Recent Changes Observation"""

    change_count: Optional[int] = strawberry.field(
        description="Number of changes (excluding bots)", graphql_type=Optional[BigInt]
    )
    user_count: Optional[int] = strawberry.field(
        description="Number of unique users (excluding bots)",
        graphql_type=Optional[BigInt],
    )
    total_change_count: Optional[int] = strawberry.field(
        description="Total number of changes (including bots)",
        graphql_type=Optional[BigInt],
    )
    total_user_count: Optional[int] = strawberry.field(
        description="Total number of unique users (including bots)",
        graphql_type=Optional[BigInt],
    )
    first_change_date: Optional[datetime] = strawberry.field(
        description="Date of first change"
    )
    last_change_date: Optional[datetime] = strawberry.field(
        description="Date of last change"
    )

    @classmethod
    def marshal(
        cls, model: WikibaseRecentChangesObservationModel
    ) -> "WikibaseRecentChangesObservationStrawberryModel":
        """Coerce Database Model to Strawberry Model"""

        return cls(
            id=strawberry.ID(model.id),
            observation_date=model.observation_date,
            returned_data=model.returned_data,
            change_count=model.change_count,
            user_count=model.user_count,
            total_change_count=model.total_change_count,
            total_user_count=model.total_user_count,
            first_change_date=model.first_change_date,
            last_change_date=model.last_change_date,
        )
