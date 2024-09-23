"""Wikibase Log Data Observation Strawberry Model"""

from datetime import datetime
from typing import Optional
import strawberry

from model.database import WikibaseLogObservationModel
from model.strawberry.output.observation.log.wikibase_log import (
    WikibaseLogStrawberryModel,
    WikibaseLogUserStrawberryModel,
)
from model.strawberry.output.observation.log.wikibase_log_collection import (
    WikibaseLogMonthStrawberryModel,
)
from model.strawberry.output.observation.wikibase_observation import (
    WikibaseObservationStrawberryModel,
)
from model.strawberry.scalars import BigInt


@strawberry.type
class WikibaseLogObservationStrawberryModel(WikibaseObservationStrawberryModel):
    """Wikibase Log Data Observation"""

    id: strawberry.ID

    instance_age: Optional[int] = strawberry.field(
        description="Age of Instance in Days (Estimated from First Log Date)",
        graphql_type=Optional[BigInt],
    )
    first_log: Optional[WikibaseLogStrawberryModel] = strawberry.field(
        description="First Log"
    )
    last_log: Optional[WikibaseLogUserStrawberryModel] = strawberry.field(
        description="Last Log"
    )

    first_month: Optional[WikibaseLogMonthStrawberryModel] = strawberry.field(
        description="First Month's Logs"
    )
    last_month: Optional[WikibaseLogMonthStrawberryModel] = strawberry.field(
        description="Last Month's Logs"
    )

    @classmethod
    def marshal(
        cls, model: WikibaseLogObservationModel
    ) -> "WikibaseLogObservationStrawberryModel":
        """Coerce Database Model to Strawberry Model"""

        if model.returned_data and (
            model.first_log_date is None
            or model.last_log_date is None
            or model.last_log_user_type is None
            or model.last_month is None
            # or model.first_month is None
        ):
            raise ValueError(
                f"Log Observation {model.id}: Expected data when observation returned data"
            )

        return cls(
            id=strawberry.ID(model.id),
            observation_date=model.observation_date,
            returned_data=model.returned_data,
            instance_age=(
                (datetime.now() - model.first_log_date).days
                if model.first_log_date is not None
                else None
            ),
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
            first_month=(
                WikibaseLogMonthStrawberryModel.marshal(model.first_month)
                if model.returned_data
                and model.first_month is not None
                and model.first_month.log_count > 0
                else None
            ),
            last_month=(
                WikibaseLogMonthStrawberryModel.marshal(model.last_month)
                if model.returned_data
                and model.last_month is not None
                and model.last_month.log_count > 0
                else None
            ),
        )
