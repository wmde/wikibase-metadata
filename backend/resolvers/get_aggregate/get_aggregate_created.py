"""Get Aggregate Year Created"""

from typing import Optional
from sqlalchemy import Select, and_, select, func

from data import get_async_session
from model.database import WikibaseLogMonthObservationModel
from model.strawberry.input import WikibaseFilterInput
from model.strawberry.output import WikibaseYearCreatedAggregateStrawberryModel
from resolvers.util import get_filtered_wikibase_query


async def get_aggregate_created(
    wikibase_filter: Optional[WikibaseFilterInput],
) -> list[WikibaseYearCreatedAggregateStrawberryModel]:
    """Get Aggregate Year Created"""

    total_created_query = get_created_query(wikibase_filter)

    async with get_async_session() as async_session:
        results = (await async_session.execute(total_created_query)).all()
        return [
            WikibaseYearCreatedAggregateStrawberryModel(
                year=year, wikibase_count=wikibase_count
            )
            for year, wikibase_count in results
        ]


def get_created_query(
    wikibase_filter: Optional[WikibaseFilterInput],
) -> Select[tuple[int, int]]:
    """Get Year Created Query"""

    filtered_subquery = get_filtered_wikibase_query(wikibase_filter).subquery()

    rank_subquery = (
        select(
            WikibaseLogMonthObservationModel.id,
            # pylint: disable-next=not-callable
            func.rank()
            .over(
                partition_by=WikibaseLogMonthObservationModel.wikibase_id,
                order_by=WikibaseLogMonthObservationModel.observation_date.desc(),
            )
            .label("rank"),
        )
        .join(
            filtered_subquery,
            onclause=WikibaseLogMonthObservationModel.wikibase_id
            == filtered_subquery.c.id,
        )
        .where(
            and_(
                WikibaseLogMonthObservationModel.returned_data,
                WikibaseLogMonthObservationModel.first_month,
                # pylint: disable-next=singleton-comparison
                WikibaseLogMonthObservationModel.first_log_date != None,
            )
        )
        .subquery()
    )
    query = (
        select(
            func.substr(WikibaseLogMonthObservationModel.first_log_date, 1, 4).label(
                "year"
            ),
            # pylint: disable-next=not-callable
            func.count().label("wikibase_count"),
        )
        .join(
            rank_subquery,
            onclause=and_(
                WikibaseLogMonthObservationModel.id == rank_subquery.c.id,
                rank_subquery.c.rank == 1,
            ),
        )
        .group_by("year")
        .order_by("year")
    )
    return query
