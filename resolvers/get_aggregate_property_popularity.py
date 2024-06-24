"""Get Aggregate Property Popularity"""

from typing import List

from sqlalchemy import desc, select, func

from data.database_connection import get_async_session
from model.database import (
    WikibasePropertyPopularityCountModel,
    WikibasePropertyPopularityObservationModel,
)
from model.strawberry.output import (
    WikibasePropertyPopularityAggregateCountStrawberryModel,
)


async def get_aggregate_property_popularity() -> List[
    WikibasePropertyPopularityAggregateCountStrawberryModel
]:
    """Get Aggregate Property Popularity"""

    rank_subquery = (
        select(
            WikibasePropertyPopularityObservationModel,
            func.rank()
            .over(
                partition_by=WikibasePropertyPopularityObservationModel.wikibase_id,
                order_by=WikibasePropertyPopularityObservationModel.observation_date.desc(),
            )
            .label("rank"),
        )
        .where(WikibasePropertyPopularityObservationModel.returned_data)
        .subquery()
    )
    observation_subquery = (
        select(rank_subquery).where(rank_subquery.c.rank == 1).subquery()
    )
    query = (
        select(
            func.min(WikibasePropertyPopularityCountModel.id).label("id"),
            WikibasePropertyPopularityCountModel.property_url,
            func.sum(WikibasePropertyPopularityCountModel.usage_count).label(
                "usage_count"
            ),
            func.count().label("wikibase_count"),
        )
        .join(observation_subquery)
        .group_by(WikibasePropertyPopularityCountModel.property_url)
        .order_by(desc("wikibase_count"))
        .order_by(desc("usage_count"))
        .order_by("id")
    )

    async with get_async_session() as async_session:
        results = (await async_session.execute(query)).all()

        return [
            WikibasePropertyPopularityAggregateCountStrawberryModel(
                r[0], r[1], r[2], r[3]
            )
            for r in results
        ]
