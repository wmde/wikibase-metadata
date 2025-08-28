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
                        WikibaseModel.wikibase_type != WikibaseType.CLOUD,
                        WikibaseModel.wikibase_type != WikibaseType.TEST,
                    ),
                ),
            )
        )
        .subquery()
    )
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
        .where((WikibaseQuantityObservationModel.returned_data))
        .subquery()
    )
    query = select(WikibaseQuantityObservationModel).join(
        rank_subquery,
        onclause=and_(
            WikibaseQuantityObservationModel.id == rank_subquery.c.id,
            rank_subquery.c.rank == 1,
        ),
    )

    df = await read_sql_query(query)

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
