"""Wikibase Log Collection Strawberry Models"""

from typing import Optional
import strawberry

from model.database import WikibaseLogMonthObservationModel
from model.strawberry.output.observation.log.wikibase_log import (
    WikibaseLogStrawberryModel,
    WikibaseLogUserStrawberryModel,
)
from model.strawberry.output.observation.log.wikibase_log_collection import (
    WikibaseLogMonthLogTypeStrawberryModel,
    WikibaseLogMonthUserTypeStrawberryModel,
)
from model.strawberry.output.observation.wikibase_observation import (
    WikibaseObservationStrawberryModel,
)
from model.strawberry.scalars import BigInt


@strawberry.type(name="WikibaseLogMonth")
class WikibaseLogMonthStrawberryModel(WikibaseObservationStrawberryModel):
    """Wikibase Log Month"""

    all_users: Optional[int] = strawberry.field(
        description="Distinct User Count", graphql_type=Optional[BigInt]
    )
    active_users: Optional[int] = strawberry.field(
        description="Distinct User with 5+ Logs Count", graphql_type=Optional[BigInt]
    )
    log_count: Optional[int] = strawberry.field(
        description="Log Count", graphql_type=Optional[BigInt]
    )
    human_users: Optional[int] = strawberry.field(
        description="Distinct (Probably) Human User Count",
        graphql_type=Optional[BigInt],
    )
    active_human_users: Optional[int] = strawberry.field(
        description="Distinct (Probably) Human User with 5+ Logs Count",
        graphql_type=Optional[BigInt],
    )

    first_log: Optional[WikibaseLogStrawberryModel] = strawberry.field(
        description="First Log"
    )
    last_log: Optional[WikibaseLogUserStrawberryModel] = strawberry.field(
        description="Last Log"
    )

    log_type_records: list[WikibaseLogMonthLogTypeStrawberryModel] = strawberry.field(
        description="Records of Each Type"
    )
    user_type_records: list[WikibaseLogMonthUserTypeStrawberryModel] = strawberry.field(
        description="Records of Each Type"
    )

    @classmethod
    def marshal(
        cls, model: WikibaseLogMonthObservationModel
    ) -> "WikibaseLogMonthStrawberryModel":
        """Coerce Database Model to Strawberry Model"""

        return cls(
            id=strawberry.ID(model.id),
            observation_date=model.observation_date,
            returned_data=model.returned_data,
            log_count=model.log_count,
            all_users=model.user_count,
            active_users=model.active_user_count,
            human_users=model.human_user_count,
            active_human_users=model.active_human_user_count,
            first_log=(
                WikibaseLogStrawberryModel(date=model.first_log_date)
                if model.returned_data and model.first_log_date is not None
                else None
            ),
            last_log=(
                WikibaseLogUserStrawberryModel(
                    date=model.last_log_date,
                    user_type=(
                        model.last_log_user_type.name
                        if model.last_log_user_type is not None
                        else None
                    ),
                )
                if model.returned_data and model.last_log_date is not None
                else None
            ),
            log_type_records=sorted(
                [
                    WikibaseLogMonthLogTypeStrawberryModel.marshal(r)
                    for r in model.log_type_records
                ],
                key=lambda x: x.log_type.value,
            ),
            user_type_records=sorted(
                [
                    WikibaseLogMonthUserTypeStrawberryModel.marshal(r)
                    for r in model.user_type_records
                ],
                key=lambda x: x.user_type.value,
            ),
        )
