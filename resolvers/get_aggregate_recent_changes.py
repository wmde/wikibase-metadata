"""Get Aggregate Recent Changes"""

from typing import Optional
from sqlalchemy import Select, and_, select, func

from data import get_async_session
from model.database import WikibaseRecentChangesObservationModel
from model.strawberry.input import WikibaseFilterInput
from model.strawberry.output import (
    WikibaseRecentChangesAggregateStrawberryModel,
)
from resolvers.util import get_filtered_wikibase_query


async def get_aggregate_recent_changes(
    wikibase_filter: Optional[WikibaseFilterInput],
) -> WikibaseRecentChangesAggregateStrawberryModel:
    """Get Aggregate Recent Changes"""

    query = get_total_recent_changes_query(wikibase_filter)

    async with get_async_session() as async_session:
        (
            human_change_count,
            human_user_count,
            bot_change_count,
            bot_user_count,
            wikibase_count,
        ) = (await async_session.execute(query)).one()

        return WikibaseRecentChangesAggregateStrawberryModel(
            human_change_count=human_change_count or 0,
            human_user_count=human_user_count or 0,
            bot_change_count=bot_change_count or 0,
            bot_user_count=bot_user_count or 0,
            wikibase_count=wikibase_count,
        )


def get_total_recent_changes_query(
    wikibase_filter: Optional[WikibaseFilterInput],
) -> Select[tuple[int, int, int, int, int]]:
    """Get Total Recent Changes Query"""

    filtered_subquery = get_filtered_wikibase_query(wikibase_filter).subquery()

    rank_subquery = (
        select(
            WikibaseRecentChangesObservationModel.id,
            # pylint: disable-next=not-callable
            func.rank()
            .over(
                partition_by=WikibaseRecentChangesObservationModel.wikibase_id,
                order_by=WikibaseRecentChangesObservationModel.observation_date.desc(),
            )
            .label("rank"),
        )
        .join(
            filtered_subquery,
            onclause=WikibaseRecentChangesObservationModel.wikibase_id
            == filtered_subquery.c.id,
        )
        .where(
            WikibaseRecentChangesObservationModel.returned_data,
        )
        .subquery()
    )
    query = select(
        func.sum(WikibaseRecentChangesObservationModel.human_change_count).label(
            "human_change_count"
        ),
        func.sum(WikibaseRecentChangesObservationModel.human_change_user_count).label(
            "human_user_count"
        ),
        func.sum(WikibaseRecentChangesObservationModel.bot_change_count).label(
            "bot_change_count"
        ),
        func.sum(WikibaseRecentChangesObservationModel.bot_change_user_count).label(
            "bot_user_count"
        ),
        # pylint: disable-next=not-callable
        func.count().label("wikibase_count"),
    ).join(
        rank_subquery,
        onclause=and_(
            WikibaseRecentChangesObservationModel.id == rank_subquery.c.id,
            rank_subquery.c.rank == 1,
        ),
    )
    return query
