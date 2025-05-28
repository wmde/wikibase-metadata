"""Wikibase Item Date Strawberry Models"""

from datetime import datetime
import strawberry


from model.database.wikibase_observation.initial_value.item_date_model import (
    WikibaseItemDateModel,
)
from model.strawberry.scalars import BigInt


@strawberry.type(name="WikibaseItemDate")
class WikibaseItemDateStrawberryModel:
    """Item Date"""

    id: strawberry.ID
    q: int = strawberry.field(description="Q# for Item", graphql_type=BigInt)
    creation_date: datetime = strawberry.field(description="Item Creation Date")

    @classmethod
    def marshal(cls, model: WikibaseItemDateModel) -> "WikibaseItemDateStrawberryModel":
        """Coerce Database Model to Strawberry Model"""

        return cls(
            id=strawberry.ID(model.id),
            q=model.item_number,
            creation_date=model.creation_date,
        )
