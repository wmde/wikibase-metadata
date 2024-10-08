"""Get Aggregate Year Created"""

from typing import List, Tuple

from sqlalchemy import Select, and_, select, func

from data import get_async_session
from model.database import WikibaseLogObservationModel, WikibaseModel
from model.strawberry.output import WikibaseYearCreatedAggregateStrawberryModel


async def get_aggregate_created() -> List[WikibaseYearCreatedAggregateStrawberryModel]:
    """Get Aggregate Year Created"""

    total_quantity_query = get_created_query()

    async with get_async_session() as async_session:
        results = (await async_session.execute(total_quantity_query)).all()
        return [
            WikibaseYearCreatedAggregateStrawberryModel(
                year=year, wikibase_count=wikibase_count
            )
            for year, wikibase_count in results
        ]


def get_created_query() -> Select[Tuple[int, int]]:
    """Get Year Created Query"""

    rank_subquery = (
        select(
            WikibaseLogObservationModel.id,
            # pylint: disable=not-callable
            func.rank()
            .over(
                partition_by=WikibaseLogObservationModel.wikibase_id,
                order_by=WikibaseLogObservationModel.observation_date.desc(),
            )
            .label("rank"),
        )
        .where(
            and_(
                WikibaseLogObservationModel.returned_data,
                WikibaseLogObservationModel.wikibase.has(WikibaseModel.checked),
            )
        )
        .subquery()
    )
    query = (
        select(
            func.substr(WikibaseLogObservationModel.first_log_date, 1, 4).label("year"),
            # pylint: disable=not-callable
            func.count().label("wikibase_count"),
        )
        .join(
            rank_subquery,
            onclause=and_(
                WikibaseLogObservationModel.id == rank_subquery.c.id,
                rank_subquery.c.rank == 1,
            ),
        )
        .group_by("year")
        .order_by("year")
    )
    return query
