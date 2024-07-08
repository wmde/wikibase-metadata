"""Get Aggregate Year Created"""

from typing import List, Tuple

from sqlalchemy import Select, select, func

from data import get_async_session
from model.database.wikibase_observation.log.wikibase_log_observation_model import (
    WikibaseLogObservationModel,
)
from model.strawberry.output.observation.log.wikibase_created_aggregate import (
    WikibaseYearCreatedAggregated,
)


async def get_aggregate_created() -> List[WikibaseYearCreatedAggregated]:
    """Get Aggregate Year Created"""

    total_quantity_query = get_created_query()

    async with get_async_session() as async_session:
        results = (await async_session.execute(total_quantity_query)).all()
        return [WikibaseYearCreatedAggregated(year=year, wikibase_count=wikibase_count) for year, wikibase_count in results]



def get_created_query() -> Select[Tuple[int, int]]:
    """Get Year Created Query"""

    rank_subquery = (
        select(
            WikibaseLogObservationModel.id,
            func.rank()  # pylint: disable=not-callable
            .over(
                partition_by=WikibaseLogObservationModel.wikibase_id,
                order_by=WikibaseLogObservationModel.observation_date.desc(),
            )
            .label("rank"),
        )
        .where(WikibaseLogObservationModel.returned_data)
        .subquery()
    )
    query = (
        select(
            func.substr(WikibaseLogObservationModel.first_log_date, 1, 4).label("year"),
            func.count().label("wikibase_count"),  # pylint: disable=not-callable
        )
        .join(
            rank_subquery,
            onclause=WikibaseLogObservationModel.id == rank_subquery.c.id,
        )
        .where(rank_subquery.c.rank == 1)
        .group_by("year")
        .order_by('year')
    )
    return query
