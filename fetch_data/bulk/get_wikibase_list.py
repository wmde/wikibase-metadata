"""Get List of Wikibases"""

from random import shuffle
from sqlalchemy import Select
from data.database_connection import get_async_session
from model.database import WikibaseModel


async def get_wikibase_list(query: Select[tuple[WikibaseModel]]) -> list[WikibaseModel]:
    """Get List of Wikibases from Query"""

    async with get_async_session() as async_session:
        wikibase_list = (await async_session.scalars(query)).unique().all()
        shuffle(wikibase_list)
        return wikibase_list
