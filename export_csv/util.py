"""Utilities"""

import pandas
from sqlalchemy import Connection, Select

from data.database_connection import async_engine


def _read_sql_query(con: Connection, stmt: Select):
    return pandas.read_sql_query(stmt, con)


async def read_sql_query(stmt: Select) -> pandas.DataFrame:
    async with async_engine.begin() as conn:
        df = await conn.run_sync(_read_sql_query, stmt)
        return df
