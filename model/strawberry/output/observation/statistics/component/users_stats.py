"""Wikibase Statistics Data Observation Strawberry Models"""

import strawberry

from model.database import WikibaseStatisticsObservationModel
from model.strawberry.scalars import BigInt


@strawberry.type(name="WikibaseStatisticsUsersObservation")
class WikibaseStatisticsUsersObservationStrawberryModel:
    """Wikibase Statistics User Data"""

    total_users: int = strawberry.field(description="Total Users", graphql_type=BigInt)
    active_users: int = strawberry.field(
        description="Active Users", graphql_type=BigInt
    )
    total_admin: int = strawberry.field(description="Total Admin", graphql_type=BigInt)

    @classmethod
    def marshal(
        cls, model: WikibaseStatisticsObservationModel
    ) -> "WikibaseStatisticsUsersObservationStrawberryModel":
        """Coerce Database Model to Strawberry Model"""

        if (
            model.total_users is None
            or model.active_users is None
            or model.total_admin is None
        ):
            raise ValueError(
                f"Statistics Observation {model.id}: Expected totals when observation returned data"
            )
        return cls(
            total_users=model.total_users,
            active_users=model.active_users,
            total_admin=model.total_admin,
        )

    def __init__(
        self, total_users: int, active_users: int, total_admin: int
    ) -> "WikibaseStatisticsUsersObservationStrawberryModel":
        self.total_users = total_users
        self.active_users = active_users
        self.total_admin = total_admin
