"""Get Aggregate URLs"""

from typing import Optional
from sqlalchemy import Select, and_, select, func

from data import get_async_session
from model.database import WikibaseURLObservationModel
from model.strawberry.input import WikibaseFilterInput
from model.strawberry.output import WikibaseURLAggregateStrawberryModel
from resolvers.util import get_filtered_wikibase_query


async def get_aggregate_urls(
    wikibase_filter: Optional[WikibaseFilterInput],
) -> WikibaseURLAggregateStrawberryModel:
    """Get Aggregate URLs"""

    total_query = get_total_urls_query(wikibase_filter)

    async with get_async_session() as async_session:
        (
            total_url_properties,
            total_url_statements,
            wikibase_count,
        ) = (await async_session.execute(total_query)).one()

        return WikibaseURLAggregateStrawberryModel(
            wikibase_count=wikibase_count,
            total_url_properties=total_url_properties or 0,
            total_url_statements=total_url_statements or 0,
        )


def get_total_urls_query(
    wikibase_filter: Optional[WikibaseFilterInput],
) -> Select[tuple[int, int, int]]:
    """Get Total URL Query"""

    filtered_subquery = get_filtered_wikibase_query(wikibase_filter).subquery()

    rank_subquery = (
        select(
            WikibaseURLObservationModel.id,
            # pylint: disable-next=not-callable
            func.rank()
            .over(
                partition_by=WikibaseURLObservationModel.wikibase_id,
                order_by=WikibaseURLObservationModel.observation_date.desc(),
            )
            .label("rank"),
        )
        .join(
            filtered_subquery,
            onclause=WikibaseURLObservationModel.wikibase_id
            == filtered_subquery.c.id,
        )
        .where(
            WikibaseURLObservationModel.returned_data,
        )
        .subquery()
    )
    query = select(
        func.sum(WikibaseURLObservationModel.total_url_properties).label(
            "total_url_properties"
        ),
        func.sum(WikibaseURLObservationModel.total_url_statements).label(
            "total_url_statements"
        ),
        # pylint: disable-next=not-callable
        func.count().label("wikibase_count"),
    ).join(
        rank_subquery,
        onclause=and_(
            WikibaseURLObservationModel.id == rank_subquery.c.id,
            rank_subquery.c.rank == 1,
        ),
    )
    return query

