"""Get Aggregate Quantity"""

from sqlalchemy import Select, and_, select, func

from data import get_async_session
from model.database import WikibaseModel, WikibaseQuantityObservationModel
from model.strawberry.output import WikibaseQuantityAggregateStrawberryModel


async def get_aggregate_quantity() -> WikibaseQuantityAggregateStrawberryModel:
    """Get Aggregate Quantity"""

    total_quantity_query = get_total_quantity_query()

    async with get_async_session() as async_session:
        (
            total_items,
            total_lexemes,
            total_properties,
            total_triples,
            total_external_identifier_properties,
            total_external_identifier_statements,
            total_url_properties,
            total_url_statements,
            wikibase_count,
        ) = (await async_session.execute(total_quantity_query)).one()

        return WikibaseQuantityAggregateStrawberryModel(
            wikibase_count=wikibase_count,
            total_items=total_items,
            total_lexemes=total_lexemes,
            total_properties=total_properties,
            total_triples=total_triples,
            total_external_identifier_properties=total_external_identifier_properties,
            total_external_identifier_statements=total_external_identifier_statements,
            total_url_properties=total_url_properties,
            total_url_statements=total_url_statements,
        )


def get_total_quantity_query() -> Select[tuple[int, int, int, int, int]]:
    """Get Total Quantity Query"""

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
        .where(
            and_(
                WikibaseQuantityObservationModel.returned_data,
                WikibaseQuantityObservationModel.wikibase.has(WikibaseModel.checked),
            )
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
        func.sum(
            WikibaseQuantityObservationModel.total_external_identifier_properties
        ).label("total_external_identifier_properties"),
        func.sum(
            WikibaseQuantityObservationModel.total_external_identifier_statements
        ).label("total_external_identifier_statements"),
        func.sum(WikibaseQuantityObservationModel.total_url_properties).label(
            "total_url_properties"
        ),
        func.sum(WikibaseQuantityObservationModel.total_url_statements).label(
            "total_url_statements"
        ),
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
