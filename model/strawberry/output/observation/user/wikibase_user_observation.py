"""Wikibase User Data Observation Strawberry Model"""

from typing import List, Optional
import strawberry

from model.database import WikibaseUserObservationModel
from model.strawberry.output.observation.user.wikibase_user_observation_group import (
    WikibaseUserObservationGroupStrawberryModel,
)
from model.strawberry.output.observation.wikibase_observation import (
    WikibaseObservationStrawberryModel,
)


@strawberry.type
class WikibaseUserObservationStrawberryModel(WikibaseObservationStrawberryModel):
    """Wikibase User Data Observation"""

    total_users: Optional[int] = strawberry.field(description="Total Users")
    user_groups: List[WikibaseUserObservationGroupStrawberryModel] = strawberry.field(
        description="User Groups and Counts"
    )

    @classmethod
    def marshal(
        cls, model: WikibaseUserObservationModel
    ) -> "WikibaseUserObservationStrawberryModel":
        """Coerce Database Model to Strawberry Model"""

        if model.returned_data and model.total_users is None:
            raise ValueError(
                f"Observation {model.id}: Expected total users when observation returned data"
            )
        return cls(
            id=strawberry.ID(model.id),
            observation_date=model.observation_date,
            returned_data=model.returned_data,
            total_users=model.total_users,
            user_groups=sorted(
                [
                    WikibaseUserObservationGroupStrawberryModel.marshal(o)
                    for o in model.user_group_observations
                ],
                key=lambda x: (x.user_count, x.group_implicit),
                reverse=True,
            ),
        )
