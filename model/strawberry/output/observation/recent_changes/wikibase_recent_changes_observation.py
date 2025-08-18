"""Wikibase Recent Changes Observation Strawberry Model"""

from datetime import datetime
from typing import Optional
import strawberry

from model.database import WikibaseRecentChangesObservationModel
from model.strawberry.output.observation.wikibase_observation import (
    WikibaseObservationStrawberryModel,
)
from model.strawberry.scalars import BigInt


@strawberry.type(name="WikibaseRecentChangesObservation")
class WikibaseRecentChangesObservationStrawberryModel(
    WikibaseObservationStrawberryModel
):
    """Wikibase Recent Changes Observation"""

    human_change_count: Optional[int] = strawberry.field(
        description=(
            "Number of changes made by humans as reported by the "
            "MediaWiki Recent Changes API when called with the !bot flag."
        ),
        graphql_type=Optional[BigInt],
    )
    human_change_user_count: Optional[int] = strawberry.field(
        description=(
            "Number of unique users found in changes requested "
            "with !bot flag, derived from all usernames, IP addresses "
            "for anonymous edits as well as userid in the userhidden case."
        ),
        graphql_type=Optional[BigInt],
    )
    bot_change_count: Optional[int] = strawberry.field(
        description=(
            "Number of changes made by bots as reported by the "
            "MediaWiki Recent Changes API when called with the bot flag."
        ),
        graphql_type=Optional[BigInt],
    )
    bot_change_user_count: Optional[int] = strawberry.field(
        description=(
            "Number of unique bots found in changes requested with "
            "bot flag, derived from all bot/usernames."
        ),
        graphql_type=Optional[BigInt],
    )
    first_change_date: Optional[datetime] = strawberry.field(
        description="Date of first change, no matter if it was made by a human or bot."
    )
    last_change_date: Optional[datetime] = strawberry.field(
        description="Date of last change, no matter if it was made by a human or bot."
    )

    @classmethod
    def marshal(
        cls, model: WikibaseRecentChangesObservationModel
    ) -> "WikibaseRecentChangesObservationStrawberryModel":
        """Coerce Database Model to Strawberry Model"""

        return cls(
            id=strawberry.ID(model.id),
            observation_date=model.observation_date,
            returned_data=model.returned_data,
            human_change_count=model.human_change_count,
            human_change_user_count=model.human_change_user_count,
            bot_change_count=model.bot_change_count,
            bot_change_user_count=model.bot_change_user_count,
            first_change_date=model.first_change_date,
            last_change_date=model.last_change_date,
        )
