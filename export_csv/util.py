"""Utilities"""

import os
from typing import Optional
import uuid
from fastapi import BackgroundTasks
from fastapi.responses import StreamingResponse
import pandas
from sqlalchemy import Connection, Select

from data.database_connection import async_engine


def _read_sql_query(con: Connection, stmt: Select, index_col: Optional[str] = None):
    return pandas.read_sql_query(stmt, con, index_col=index_col)


async def read_sql_query(
    stmt: Select, index_col: Optional[str] = None
) -> pandas.DataFrame:
    """Read SQL to DataFrame"""

    async with async_engine.begin() as conn:
        df = await conn.run_sync(_read_sql_query, stmt, index_col=index_col)
        return df


CHUNK_SIZE = 1024 * 1024


async def export_csv(
    query: Select,
    export_filename: str,
    background_tasks: BackgroundTasks,
    index_col: Optional[str] = None,
):
    """Export CSV"""

    df = await read_sql_query(query, index_col=index_col)

    filename = f"{uuid.uuid4()}.csv"
    df.to_csv(filename)
    del df

    def iterfile():
        with open(filename, "rb") as f:
            while chunk := f.read(CHUNK_SIZE):
                yield chunk

    background_tasks.add_task(os.remove, filename)

    headers = {"Content-Disposition": f'attachment; filename="{export_filename}.csv"'}
    return StreamingResponse(iterfile(), headers=headers, media_type="text/csv")
