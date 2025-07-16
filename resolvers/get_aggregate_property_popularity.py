"""Get Aggregate Property Popularity"""

from typing import Optional
from sqlalchemy import Select, and_, desc, select, func

from data import get_async_session
from model.database import (
    WikibasePropertyPopularityCountModel,
    WikibasePropertyPopularityObservationModel,
)
from model.strawberry.input import WikibaseFilterInput
from model.strawberry.output import (
    Page,
    PageNumberType,
    PageSizeType,
    WikibasePropertyPopularityAggregateCountStrawberryModel,
)
from resolvers.util import get_filtered_wikibase_query


async def get_aggregate_property_popularity(
    page_number: PageNumberType,
    page_size: PageSizeType,
    wikibase_filter: Optional[WikibaseFilterInput],
) -> Page[WikibasePropertyPopularityAggregateCountStrawberryModel]:
    """Get Aggregate Property Popularity"""

    query = get_unordered_query(wikibase_filter)

    async with get_async_session() as async_session:
        total_count = await async_session.scalar(
            # pylint: disable-next=not-callable
            select(func.count()).select_from(query.subquery())
        )
        results = (
            await async_session.execute(
                query.order_by(desc("wikibase_count"))
                .order_by(desc("usage_count"))
                .order_by("id")
                .offset((page_number - 1) * page_size)
                .limit(page_size)
            )
        ).all()

        return Page.marshal(
            page_number,
            page_size,
            total_count,
            [
                WikibasePropertyPopularityAggregateCountStrawberryModel(
                    id=id,
                    property_url=property_url,
                    usage_count=usage_count,
                    wikibase_count=wikibase_count,
                )
                for (id, property_url, usage_count, wikibase_count) in results
            ],
        )


def get_unordered_query(
    wikibase_filter: Optional[WikibaseFilterInput],
) -> Select[tuple[int, str, int, int]]:
    """Get Unordered Property Popularity Query"""

    filtered_wikibase_subquery = get_filtered_wikibase_query(wikibase_filter)

    rank_subquery = (
        select(
            WikibasePropertyPopularityObservationModel.id,
            # pylint: disable-next=not-callable
            func.rank()
            .over(
                partition_by=WikibasePropertyPopularityObservationModel.wikibase_id,
                order_by=WikibasePropertyPopularityObservationModel.observation_date.desc(),
            )
            .label("rank"),
        )
        .join(
            filtered_wikibase_subquery,
            onclause=WikibasePropertyPopularityObservationModel.wikibase_id
            == filtered_wikibase_subquery.c.id,
        )
        .where(WikibasePropertyPopularityObservationModel.returned_data)
        .subquery()
    )
    query = (
        select(
            func.min(WikibasePropertyPopularityCountModel.id).label("id"),
            WikibasePropertyPopularityCountModel.property_url,
            func.sum(WikibasePropertyPopularityCountModel.usage_count).label(
                "usage_count"
            ),
            # pylint: disable-next=not-callable
            func.count().label("wikibase_count"),
        )
        .join(
            rank_subquery,
            onclause=and_(
                rank_subquery.c.id
                == WikibasePropertyPopularityCountModel.wikibase_property_popularity_observation_id,
                rank_subquery.c.rank == 1,
            ),
        )
        .group_by(WikibasePropertyPopularityCountModel.property_url)
    )
    return query
