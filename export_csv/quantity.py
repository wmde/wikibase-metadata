"""Quantity CSV"""

import os
import uuid
from fastapi import BackgroundTasks
from fastapi.responses import StreamingResponse
from sqlalchemy import and_, func, or_, select

from export_csv.util import read_sql_query
from model.database import WikibaseModel, WikibaseQuantityObservationModel
from model.enum import WikibaseType


CHUNK_SIZE = 1024 * 1024


async def export_quantity_csv(background_tasks: BackgroundTasks):
    """Quantity CSV"""

    filtered_subquery = (
        select(WikibaseModel)
        .where(
            and_(
                WikibaseModel.checked,
                or_(
                    # pylint: disable-next=singleton-comparison
                    WikibaseModel.wikibase_type == None,
                    and_(
                        # WikibaseModel.wikibase_type != WikibaseType.CLOUD,
                        WikibaseModel.wikibase_type != WikibaseType.TEST,
                    ),
                ),
            )
        )
        .cte(name="filtered_wikibases")
    )
    quantity_rank_subquery = (
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
        .where((WikibaseQuantityObservationModel.returned_data)).subquery()
    )
    most_recent_successful_quantity_obs = (
        select(WikibaseQuantityObservationModel)
        .join(
            quantity_rank_subquery,
            onclause=and_(
                WikibaseQuantityObservationModel.id == quantity_rank_subquery.c.id,
                quantity_rank_subquery.c.rank == 1,
            ),
        )
        .cte(name='filtered_quantity_observations')
    )

    query = select(
        filtered_subquery.c.id.label('wikibase_id'),
        filtered_subquery.c.wb_type.label('wikibase_type'),
        most_recent_successful_quantity_obs.c.date.label("quantity_observation_date"),
        most_recent_successful_quantity_obs.c.total_items,
        most_recent_successful_quantity_obs.c.total_lexemes,
        most_recent_successful_quantity_obs.c.total_properties,
        most_recent_successful_quantity_obs.c.total_triples,
        most_recent_successful_quantity_obs.c.total_external_identifier_properties.label('total_ei_properties'),
        most_recent_successful_quantity_obs.c.total_external_identifier_statements.label('total_ei_statements'),
        most_recent_successful_quantity_obs.c.total_url_properties,
        most_recent_successful_quantity_obs.c.total_url_statements,
    ).join(
        most_recent_successful_quantity_obs,
        onclause=filtered_subquery.c.id
        == most_recent_successful_quantity_obs.c.wikibase_id,
        isouter=True,
    )

    df = await read_sql_query(query, index_col="wikibase_id")

    filename = f"{uuid.uuid4()}.csv"
    df.to_csv(filename)
    del df

    def iterfile():
        with open(filename, "rb") as f:
            while chunk := f.read(CHUNK_SIZE):
                yield chunk

    background_tasks.add_task(os.remove, filename)

    headers = {"Content-Disposition": 'attachment; filename="quantity_data.csv"'}
    return StreamingResponse(iterfile(), headers=headers, media_type="text/csv")
