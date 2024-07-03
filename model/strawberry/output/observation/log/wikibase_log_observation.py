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


@strawberry.type
class WikibaseLogObservationStrawberryModel(WikibaseObservationStrawberryModel):
    """Wikibase Log Data Observation"""

    first_log_date: datetime = strawberry.field(description="First Log Date")
    last_log_date: datetime = strawberry.field(description="Last Log Date")
    last_log_user_type: str = strawberry.field(
        description="Last Log User Type - Bot, User, or Missing?"
    )
    last_month_log_count: int = strawberry.field(
        description="Logs from the Last 30 Days"
    )
    last_month_user_count: int = strawberry.field(
        description="Distinct Users from the Last Month's Logs"
    )
    last_month_human_user_count: int = strawberry.field(
        description="Distinct (Probably) Human Users from the Last Month's Logs"
    )

    @classmethod
    def marshal(
        cls, model: WikibaseLogObservationModel
    ) -> "WikibaseLogObservationStrawberryModel":
        """Coerce Database Model to Strawberry Model"""

        return cls(
            id=strawberry.ID(model.id),
            observation_date=model.observation_date,
            returned_data=model.returned_data,
            first_log_date=model.first_log_date,
            last_log_date=model.last_log_date,
            last_log_user_type=model.last_log_user_type.name,
            last_month_log_count=model.last_month_log_count,
            last_month_user_count=model.last_month_user_count,
            last_month_human_user_count=model.last_month_human_user_count,
        )
