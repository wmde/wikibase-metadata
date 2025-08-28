"""Main Application"""

import os
import uuid
from fastapi import BackgroundTasks
from fastapi.responses import StreamingResponse
import pandas
from sqlalchemy import Connection, Select, select

from data.database_connection import async_engine, get_async_session
from model.database.wikibase_model import WikibaseModel


CHUNK_SIZE = 1024 * 1024


def _read_sql_query(con: Connection, stmt: Select):
    return pandas.read_sql_query(stmt, con)


async def export_quantity_csv(background_tasks: BackgroundTasks):
    """Quantity CSV"""

    select_query = select(WikibaseModel)

    async with async_engine.begin() as conn:
        df = await conn.run_sync(_read_sql_query, select_query)

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
