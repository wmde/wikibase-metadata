"""Wikibase Log Data Observation Strawberry Model"""

from datetime import datetime
from typing import List, Optional
import strawberry

from model.database import (
    WikibaseLogMonthLogTypeObservationModel,
    WikibaseLogMonthObservationModel,
    WikibaseLogMonthUserTypeObservationModel,
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

    id: strawberry.ID

    all_users: int = strawberry.field(
        description="Distinct User Count", graphql_type=BigInt
    )
    log_count: Optional[int] = strawberry.field(
        description="Log Count", graphql_type=Optional[BigInt]
    )
    first_log_date: datetime = strawberry.field(description="First Log Date")
    last_log_date: datetime = strawberry.field(description="First Log Date")


@strawberry.type
class WikibaseLogMonthLogTypeStrawberryModel(WikibaseLogCollectionStrawberryModel):
    """Wikibase Log Month, specific Log Type"""

    log_type: str = strawberry.field(description="Log Type")
    human_users: int = strawberry.field(
        description="Distinct (Probably) Human User Count", graphql_type=BigInt
    )

    @classmethod
    def marshal(
        cls, model: WikibaseLogMonthLogTypeObservationModel
    ) -> "WikibaseLogMonthLogTypeStrawberryModel":
        """Coerce Database Model to Strawberry Model"""

        return cls(
            id=strawberry.ID(model.id),
            log_type=model.log_type.name,
            log_count=model.log_count,
            all_users=model.user_count,
            human_users=model.human_user_count,
            first_log_date=model.first_log_date,
            last_log_date=model.last_log_date,
        )


@strawberry.type
class WikibaseLogMonthUserTypeStrawberryModel(WikibaseLogCollectionStrawberryModel):
    """Wikibase Log Month, specific User Type"""

    user_type: str = strawberry.field(description="User Type")

    @classmethod
    def marshal(
        cls, model: WikibaseLogMonthUserTypeObservationModel
    ) -> "WikibaseLogMonthLogTypeStrawberryModel":
        """Coerce Database Model to Strawberry Model"""

        return cls(
            id=strawberry.ID(model.id),
            user_type=model.user_type.name,
            log_count=model.log_count,
            all_users=model.user_count,
            first_log_date=model.first_log_date,
            last_log_date=model.last_log_date,
        )


@strawberry.type
class WikibaseLogMonthStrawberryModel(WikibaseLogCollectionStrawberryModel):
    """Wikibase Log Month"""

    log_type_records: List[WikibaseLogMonthLogTypeStrawberryModel] = strawberry.field(
        description="Records of Each Type"
    )
    user_type_records: List[WikibaseLogMonthUserTypeStrawberryModel] = strawberry.field(
        description="Records of Each Type"
    )
    human_users: int = strawberry.field(
        description="Distinct (Probably) Human User Count", graphql_type=BigInt
    )

    @classmethod
    def marshal(
        cls, model: WikibaseLogMonthObservationModel
    ) -> "WikibaseLogMonthStrawberryModel":
        """Coerce Database Model to Strawberry Model"""

        return cls(
            id=strawberry.ID(model.id),
            log_count=model.log_count,
            all_users=model.user_count,
            human_users=model.human_user_count,
            first_log_date=model.first_log_date,
            last_log_date=model.last_log_date,
            log_type_records=sorted(
                [
                    WikibaseLogMonthLogTypeStrawberryModel.marshal(r)
                    for r in model.log_type_records
                ],
                key=lambda x: x.log_type,
            ),
            user_type_records=sorted(
                [
                    WikibaseLogMonthUserTypeStrawberryModel.marshal(r)
                    for r in model.user_type_records
                ],
                key=lambda x: x.user_type,
            ),
        )


@strawberry.type
class WikibaseLogObservationStrawberryModel(WikibaseObservationStrawberryModel):
    """Wikibase Log Data Observation"""

    id: strawberry.ID

    instance_age: Optional[int] = strawberry.field(
        description="Age of Instance in Days (Estimated from First Log Date)",
        graphql_type=BigInt,
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

        if model.returned_data and (  # pylint: disable=too-many-boolean-expressions
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
