"""Get Aggregate Year Created"""

from sqlalchemy import Select, and_, select, func

from data import get_async_session
from model.database import WikibaseLogMonthObservationModel, WikibaseModel
from model.strawberry.output import WikibaseYearCreatedAggregateStrawberryModel


async def get_aggregate_created() -> list[WikibaseYearCreatedAggregateStrawberryModel]:
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


def get_created_query() -> Select[tuple[int, int]]:
    """Get Year Created Query"""

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
        .where(
            and_(
                WikibaseLogMonthObservationModel.returned_data,
                WikibaseLogMonthObservationModel.first_month,
                WikibaseLogMonthObservationModel.wikibase.has(WikibaseModel.checked),
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
