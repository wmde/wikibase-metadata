"""Wikibase Observed User Group Strawberry Model"""

import strawberry

from model.database import (
    WikibaseUserObservationGroupModel,
)
from model.strawberry.output.observation.user.wikibase_user_group import (
    WikibaseUserGroupStrawberryModel,
)
from model.strawberry.scalars.big_int import BigInt


@strawberry.type
class WikibaseUserObservationGroupStrawberryModel:
    """Wikibase Observed User Group"""

    id: strawberry.ID
    group: WikibaseUserGroupStrawberryModel
    group_implicit: bool = strawberry.field(description="Group Marked Implicit?")
    user_count: int = strawberry.field(description="User Count", graphql_type=BigInt)

    @classmethod
    def marshal(
        cls, model: WikibaseUserObservationGroupModel
    ) -> "WikibaseUserObservationGroupStrawberryModel":
        """Coerce Database Model to Strawberry Model"""

        return cls(
            id=strawberry.ID(model.id),
            group=WikibaseUserGroupStrawberryModel.marshal(model.user_group),
            group_implicit=model.group_implicit,
            user_count=model.user_count,
        )
