"""Get Aggregate Property Popularity"""

from typing import Tuple

from sqlalchemy import Select, select, func

from data import get_async_session
from model.database.wikibase_observation.quantity.wikibase_quantity_observation_model import (
    WikibaseQuantityObservationModel,
)
from model.strawberry.output.observation.quantity.wikibase_quantity_aggregate import (
    WikibaseQuantityAggregate,
)


async def get_aggregate_quantity() -> WikibaseQuantityAggregate:
    """Get Aggregate Property Popularity"""

    total_quantity_query = get_total_quantity_query()

    async with get_async_session() as async_session:
        total_items, total_lexemes, total_properties, total_triples, wikibase_count = (
            await async_session.execute(total_quantity_query)
        ).one()

        return WikibaseQuantityAggregate(
            wikibase_count=wikibase_count,
            total_items=total_items,
            total_lexemes=total_lexemes,
            total_properties=total_properties,
            total_triples=total_triples,
        )


def get_total_quantity_query() -> Select[Tuple[int, int, int, int, int]]:
    """Get Total Quantity Query"""

    rank_subquery = (
        select(
            WikibaseQuantityObservationModel.id,
            func.rank()  # pylint: disable=not-callable
            .over(
                partition_by=WikibaseQuantityObservationModel.wikibase_id,
                order_by=WikibaseQuantityObservationModel.observation_date.desc(),
            )
            .label("rank"),
        )
        .where(WikibaseQuantityObservationModel.returned_data)
        .subquery()
    )
    query = (
        select(
            func.sum(WikibaseQuantityObservationModel.total_items).label("total_items"),
            func.sum(WikibaseQuantityObservationModel.total_lexemes).label(
                "total_lexemes"
            ),
            func.sum(WikibaseQuantityObservationModel.total_properties).label(
                "total_properties"
            ),
            func.sum(WikibaseQuantityObservationModel.total_triples).label(
                "total_triples"
            ),
            func.count().label("wikibase_count"),  # pylint: disable=not-callable
        )
        .join(
            rank_subquery,
            onclause=WikibaseQuantityObservationModel.id == rank_subquery.c.id,
        )
        .where(rank_subquery.c.rank == 1)
    )
    return query
