"""Get Aggregate Property Popularity"""

from typing import Tuple

from sqlalchemy import Select, select, func

from data import get_async_session
from model.database.wikibase_observation.user.wikibase_user_observation_model import (
    WikibaseUserObservationModel,
)
from model.strawberry.output.observation.user.wikibase_user_aggregate import (
    WikibaseUserAggregate,
)


async def get_aggregate_users() -> WikibaseUserAggregate:
    """Get Aggregate Property Popularity"""

    query = get_aggregate_query()

    async with get_async_session() as async_session:
        total_users, wikibase_count = (await async_session.execute(query)).one()

        return WikibaseUserAggregate(
            total_users=total_users, wikibase_count=wikibase_count
        )


def get_aggregate_query() -> Select[Tuple[int, int]]:
    """Get Unordered Property Popularity Query"""

    rank_subquery = (
        select(
            WikibaseUserObservationModel,
            func.rank()  # pylint: disable=not-callable
            .over(
                partition_by=WikibaseUserObservationModel.wikibase_id,
                order_by=WikibaseUserObservationModel.observation_date.desc(),
            )
            .label("rank"),
        )
        .where(WikibaseUserObservationModel.returned_data)
        .subquery()
    )
    query = (
        select(
            func.sum(WikibaseUserObservationModel.total_users).label("total_users"),
            func.count().label("wikibase_count"),  # pylint: disable=not-callable
        )
        .join(
            rank_subquery,
            onclause=WikibaseUserObservationModel.id == rank_subquery.c.id,
        )
        .where(rank_subquery.c.rank == 1)
    )
    return query
