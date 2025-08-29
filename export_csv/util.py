"""Utilities"""

from typing import Optional
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
