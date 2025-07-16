"""Get Aggregate Quantity"""

from typing import Optional
from sqlalchemy import Select, and_, select, func

from data import get_async_session
from model.database import WikibaseQuantityObservationModel
from model.strawberry.input import WikibaseFilterInput
from model.strawberry.output import WikibaseQuantityAggregateStrawberryModel
from resolvers.util import get_filtered_wikibase_query


async def get_aggregate_quantity(
    wikibase_filter: Optional[WikibaseFilterInput],
) -> WikibaseQuantityAggregateStrawberryModel:
    """Get Aggregate Quantity"""

    total_quantity_query = get_total_quantity_query(wikibase_filter)

    async with get_async_session() as async_session:
        total_items, total_lexemes, total_properties, total_triples, wikibase_count = (
            await async_session.execute(total_quantity_query)
        ).one()

        return WikibaseQuantityAggregateStrawberryModel(
            wikibase_count=wikibase_count,
            total_items=total_items,
            total_lexemes=total_lexemes,
            total_properties=total_properties,
            total_triples=total_triples,
        )


def get_total_quantity_query(
    wikibase_filter: Optional[WikibaseFilterInput],
) -> Select[tuple[int, int, int, int, int]]:
    """Get Total Quantity Query"""

    filtered_subquery = get_filtered_wikibase_query(wikibase_filter).subquery()

    rank_subquery = (
        select(
            WikibaseQuantityObservationModel.id,
            # pylint: disable-next=not-callable
            func.rank()
            .over(
                partition_by=WikibaseQuantityObservationModel.wikibase_id,
                order_by=WikibaseQuantityObservationModel.observation_date.desc(),
            )
            .label("rank"),
        )
        .join(
            filtered_subquery,
            onclause=WikibaseQuantityObservationModel.wikibase_id
            == filtered_subquery.c.id,
        )
        .where(
            WikibaseQuantityObservationModel.returned_data,
        )
        .subquery()
    )
    query = select(
        func.sum(WikibaseQuantityObservationModel.total_items).label("total_items"),
        func.sum(WikibaseQuantityObservationModel.total_lexemes).label("total_lexemes"),
        func.sum(WikibaseQuantityObservationModel.total_properties).label(
            "total_properties"
        ),
        func.sum(WikibaseQuantityObservationModel.total_triples).label("total_triples"),
        # pylint: disable-next=not-callable
        func.count().label("wikibase_count"),
    ).join(
        rank_subquery,
        onclause=and_(
            WikibaseQuantityObservationModel.id == rank_subquery.c.id,
            rank_subquery.c.rank == 1,
        ),
    )
    return query
