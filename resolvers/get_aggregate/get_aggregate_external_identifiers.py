"""Get Aggregate External Identifiers"""

from typing import Optional
from sqlalchemy import Select, and_, select, func

from data import get_async_session
from model.database import WikibaseExternalIdentifierObservationModel
from model.strawberry.input import WikibaseFilterInput
from model.strawberry.output import (
    WikibaseExternalIdentifierAggregateStrawberryModel,
)
from resolvers.util import get_filtered_wikibase_query


async def get_aggregate_external_identifiers(
    wikibase_filter: Optional[WikibaseFilterInput],
) -> WikibaseExternalIdentifierAggregateStrawberryModel:
    """Get Aggregate External Identifiers"""

    total_query = get_total_external_identifiers_query(wikibase_filter)

    async with get_async_session() as async_session:
        (
            total_external_identifier_properties,
            total_external_identifier_statements,
            wikibase_count,
        ) = (await async_session.execute(total_query)).one()

        return WikibaseExternalIdentifierAggregateStrawberryModel(
            wikibase_count=wikibase_count,
            total_external_identifier_properties=total_external_identifier_properties
            or 0,
            total_external_identifier_statements=total_external_identifier_statements
            or 0,
        )


def get_total_external_identifiers_query(
    wikibase_filter: Optional[WikibaseFilterInput],
) -> Select[tuple[int, int, int]]:
    """Get Total External Identifier Query"""

    filtered_subquery = get_filtered_wikibase_query(wikibase_filter).subquery()

    rank_subquery = (
        select(
            WikibaseExternalIdentifierObservationModel.id,
            # pylint: disable-next=not-callable
            func.rank()
            .over(
                partition_by=WikibaseExternalIdentifierObservationModel.wikibase_id,
                order_by=WikibaseExternalIdentifierObservationModel.observation_date.desc(),
            )
            .label("rank"),
        )
        .join(
            filtered_subquery,
            onclause=WikibaseExternalIdentifierObservationModel.wikibase_id
            == filtered_subquery.c.id,
        )
        .where(
            WikibaseExternalIdentifierObservationModel.returned_data,
        )
        .subquery()
    )
    query = select(
        func.sum(
            WikibaseExternalIdentifierObservationModel.total_external_identifier_properties
        ).label("total_external_identifier_properties"),
        func.sum(
            WikibaseExternalIdentifierObservationModel.total_external_identifier_statements
        ).label("total_external_identifier_statements"),
        # pylint: disable-next=not-callable
        func.count().label("wikibase_count"),
    ).join(
        rank_subquery,
        onclause=and_(
            WikibaseExternalIdentifierObservationModel.id == rank_subquery.c.id,
            rank_subquery.c.rank == 1,
        ),
    )
    return query
