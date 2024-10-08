"""Wikibase Log Collection Strawberry Models"""

from datetime import datetime
from typing import List, Optional
import strawberry

from model.database import (
    WikibaseLogMonthLogTypeObservationModel,
    WikibaseLogMonthObservationModel,
    WikibaseLogMonthUserTypeObservationModel,
)
from model.enum import WikibaseLogType, WikibaseUserType
from model.strawberry.scalars import BigInt


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
    last_log_date: datetime = strawberry.field(description="Last Log Date")


@strawberry.type
class WikibaseLogMonthLogTypeStrawberryModel(WikibaseLogCollectionStrawberryModel):
    """Wikibase Log Month, specific Log Type"""

    log_type: WikibaseLogType = strawberry.field(description="Log Type")
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
            log_type=model.log_type,
            log_count=model.log_count,
            all_users=model.user_count,
            human_users=model.human_user_count,
            first_log_date=model.first_log_date,
            last_log_date=model.last_log_date,
        )


@strawberry.type
class WikibaseLogMonthUserTypeStrawberryModel(WikibaseLogCollectionStrawberryModel):
    """Wikibase Log Month, specific User Type"""

    user_type: WikibaseUserType = strawberry.field(description="User Type")

    @classmethod
    def marshal(
        cls, model: WikibaseLogMonthUserTypeObservationModel
    ) -> "WikibaseLogMonthUserTypeStrawberryModel":
        """Coerce Database Model to Strawberry Model"""

        return cls(
            id=strawberry.ID(model.id),
            user_type=model.user_type,
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
