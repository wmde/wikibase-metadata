"""Utilities"""

from typing import Optional
from fastapi.responses import Response
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


async def export_csv(
    query: Select,
    export_filename: str,
    index_col: Optional[str] = None,
):
    """Export CSV"""

    df = await read_sql_query(query, index_col=index_col)
    if index_col == "wikibase_id":
        assert len(set(df.index)) == len(df), "Returned Multiple Rows per Wikibase"

    csv = df.to_csv()
    del df

    headers = {"Content-Disposition": f'attachment; filename="{export_filename}.csv"'}
    return Response(csv, headers=headers, media_type="text/csv")
