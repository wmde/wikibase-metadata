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
class WikibaseLogStrawberryModel:
    """Wikibase Log"""

    date: datetime = strawberry.field(description="Log Date")


@strawberry.type
class WikibaseLogUserStrawberryModel(WikibaseLogStrawberryModel):
    """Wikibase Log"""

    user_type: str = strawberry.field(description="User Type - Bot, User, or Missing?")


@strawberry.type
class UserCountStrawberryModel:
    """Wikibase Log"""

    all_users: int = strawberry.field(description="Distinct User Count")
    human_users: int = strawberry.field(
        description="Distinct (Probably) Human User Count"
    )


@strawberry.type
class WikibaseLogObservationStrawberryModel(WikibaseObservationStrawberryModel):
    """Wikibase Log Data Observation"""

    first_log: WikibaseLogStrawberryModel = strawberry.field(description="First Log")
    last_log: WikibaseLogUserStrawberryModel = strawberry.field(description="Last Log")

    last_month_log_count: int = strawberry.field(
        description="Logs from the Last 30 Days"
    )
    last_month_user_count: UserCountStrawberryModel = strawberry.field(
        description="Users from the Last Month's Logs"
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
            first_log=WikibaseLogStrawberryModel(date=model.first_log_date),
            last_log=WikibaseLogUserStrawberryModel(
                date=model.last_log_date, user_type=model.last_log_user_type.name
            ),
            last_month_log_count=model.last_month_log_count,
            last_month_user_count=UserCountStrawberryModel(
                all_users=model.last_month_user_count,
                human_users=model.last_month_human_user_count,
            ),
        )
