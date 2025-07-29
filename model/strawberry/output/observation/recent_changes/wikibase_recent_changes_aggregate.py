"""Aggregate Recent Changes Strawberry Model"""

import strawberry

from model.strawberry.scalars import BigInt


@strawberry.type(name="WikibaseRecentChangesAggregate")
class WikibaseRecentChangesAggregateStrawberryModel:
    """Aggregate Recent Changes"""

    human_change_count: int = strawberry.field(
        description="Total Human Changes", graphql_type=BigInt
    )
    human_user_count: int = strawberry.field(
        description="Total Human Users", graphql_type=BigInt
    )
    bot_change_count: int = strawberry.field(
        description="Total Bot Changes", graphql_type=BigInt
    )
    bot_user_count: int = strawberry.field(
        description="Total Bot Users", graphql_type=BigInt
    )

    wikibase_count: int = strawberry.field(
        description="Wikibases with Recent Changes Data"
    )

    def __init__(
        self,
        human_change_count: int,
        human_user_count: int,
        bot_change_count: int,
        bot_user_count: int,
        wikibase_count: int,
    ) -> "WikibaseRecentChangesAggregateStrawberryModel":
        self.human_change_count = human_change_count
        self.human_user_count = human_user_count
        self.bot_change_count = bot_change_count
        self.bot_user_count = bot_user_count
        self.wikibase_count = wikibase_count
