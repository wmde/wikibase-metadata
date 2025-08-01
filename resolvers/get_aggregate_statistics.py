"""Get Aggregate Statistics"""

from typing import Optional
from sqlalchemy import Select, and_, select, func

from data import get_async_session
from model.database import WikibaseStatisticsObservationModel
from model.strawberry.input import WikibaseFilterInput
from model.strawberry.output import WikibaseStatisticsAggregateStrawberryModel
from resolvers.util import get_filtered_wikibase_query


async def get_aggregate_statistics(
    wikibase_filter: Optional[WikibaseFilterInput],
) -> WikibaseStatisticsAggregateStrawberryModel:
    """Get Aggregate Statistics"""

    total_statistics_query = get_total_statistics_query(wikibase_filter)

    async with get_async_session() as async_session:
        (
            total_pages,
            content_pages,
            total_files,
            total_edits,
            content_page_word_count_total,
            total_users,
            active_users,
            total_admin,
            wikibase_count,
        ) = (await async_session.execute(total_statistics_query)).one()

        return WikibaseStatisticsAggregateStrawberryModel(
            wikibase_count=wikibase_count,
            total_pages=total_pages or 0,
            content_pages=content_pages or 0,
            total_files=total_files or 0,
            total_edits=total_edits or 0,
            total_users=total_users or 0,
            active_users=active_users or 0,
            total_admin=total_admin or 0,
            content_page_word_count_total=content_page_word_count_total or 0,
        )


def get_total_statistics_query(
    wikibase_filter: Optional[WikibaseFilterInput],
) -> Select[tuple[int, int, int, int, int, int, int, int, int]]:
    """Get Total Statistics Query"""

    filtered_subquery = get_filtered_wikibase_query(wikibase_filter).subquery()

    rank_subquery = (
        select(
            WikibaseStatisticsObservationModel.id,
            # pylint: disable-next=not-callable
            func.rank()
            .over(
                partition_by=WikibaseStatisticsObservationModel.wikibase_id,
                order_by=WikibaseStatisticsObservationModel.observation_date.desc(),
            )
            .label("rank"),
        )
        .join(
            filtered_subquery,
            onclause=WikibaseStatisticsObservationModel.wikibase_id
            == filtered_subquery.c.id,
        )
        .where(
            WikibaseStatisticsObservationModel.returned_data,
        )
        .subquery()
    )
    query = select(
        func.sum(WikibaseStatisticsObservationModel.total_pages).label("total_pages"),
        func.sum(WikibaseStatisticsObservationModel.content_pages).label(
            "content_pages"
        ),
        func.sum(WikibaseStatisticsObservationModel.total_files).label("total_files"),
        func.sum(WikibaseStatisticsObservationModel.total_edits).label("total_edits"),
        func.sum(
            WikibaseStatisticsObservationModel.content_page_word_count_total
        ).label("words_in_content_pages"),
        func.sum(WikibaseStatisticsObservationModel.total_users).label("total_users"),
        func.sum(WikibaseStatisticsObservationModel.active_users).label("active_users"),
        func.sum(WikibaseStatisticsObservationModel.total_admin).label("total_admin"),
        # pylint: disable-next=not-callable
        func.count().label("wikibase_count"),
    ).join(
        rank_subquery,
        onclause=and_(
            WikibaseStatisticsObservationModel.id == rank_subquery.c.id,
            rank_subquery.c.rank == 1,
        ),
    )
    return query
