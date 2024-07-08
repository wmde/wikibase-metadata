"""Wikibase Log Data Observation Strawberry Model"""

from datetime import datetime
from typing import Optional
import strawberry

from model.database import (
    WikibaseLogObservationModel,
)
from model.strawberry.output.observation.wikibase_observation import (
    WikibaseObservationStrawberryModel,
)
from model.strawberry.scalars.big_int import BigInt


@strawberry.type
class WikibaseLogStrawberryModel:
    """Wikibase Log"""

    date: datetime = strawberry.field(description="Log Date")


@strawberry.type
class WikibaseLogUserStrawberryModel(WikibaseLogStrawberryModel):
    """Wikibase Log"""

    user_type: str = strawberry.field(description="User Type - Bot, User, or Missing?")


@strawberry.type
class WikibaseLogCollectionStrawberryModel:
    """Wikibase Log Collection"""

    all_users: int = strawberry.field(
        description="Distinct User Count", graphql_type=BigInt
    )
    human_users: int = strawberry.field(
        description="Distinct (Probably) Human User Count", graphql_type=BigInt
    )
    log_count: Optional[int] = strawberry.field(
        description="Log Count", graphql_type=Optional[BigInt]
    )


@strawberry.type
class WikibaseLogObservationStrawberryModel(WikibaseObservationStrawberryModel):
    """Wikibase Log Data Observation"""

    first_log: Optional[WikibaseLogStrawberryModel] = strawberry.field(
        description="First Log"
    )
    last_log: Optional[WikibaseLogUserStrawberryModel] = strawberry.field(
        description="Last Log"
    )

    last_month: Optional[WikibaseLogCollectionStrawberryModel] = strawberry.field(
        description="Last Month's Logs"
    )

    @classmethod
    def marshal(
        cls, model: WikibaseLogObservationModel
    ) -> "WikibaseLogObservationStrawberryModel":
        """Coerce Database Model to Strawberry Model"""

        if model.returned_data and (  # pylint: disable=too-many-boolean-expressions
            model.first_log_date is None
            or model.last_log_date is None
            or model.last_log_user_type is None
            or model.last_month_log_count is None
            or model.last_month_user_count is None
            or model.last_month_human_user_count is None
        ):
            raise ValueError(
                f"Log Observation {model.id}: Expected data when observation returned data"
            )

        return cls(
            id=strawberry.ID(model.id),
            observation_date=model.observation_date,
            returned_data=model.returned_data,
            first_log=(
                WikibaseLogStrawberryModel(date=model.first_log_date)
                if model.returned_data
                else None
            ),
            last_log=(
                WikibaseLogUserStrawberryModel(
                    date=model.last_log_date, user_type=model.last_log_user_type.name
                )
                if model.returned_data
                else None
            ),
            last_month=(
                WikibaseLogCollectionStrawberryModel(
                    all_users=model.last_month_user_count,
                    human_users=model.last_month_human_user_count,
                    log_count=model.last_month_log_count,
                )
                if model.returned_data
                else None
            ),
        )
