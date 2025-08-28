"""Quantity CSV"""

import os
import uuid
from fastapi import BackgroundTasks
from fastapi.responses import StreamingResponse
from sqlalchemy import select

from export_csv.util import read_sql_query
from model.database.wikibase_model import WikibaseModel


CHUNK_SIZE = 1024 * 1024


async def export_quantity_csv(background_tasks: BackgroundTasks):
    """Quantity CSV"""

    select_query = select(WikibaseModel)

    df = await read_sql_query(select_query)

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
