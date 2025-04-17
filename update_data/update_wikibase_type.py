"""Merge Software"""

from typing import Optional
from data.database_connection import get_async_session
from fetch_data.utils import get_wikibase_from_database
from model.database import WikibaseModel
from model.enum import WikibaseType


async def update_wikibase_type(
    wikibase_id: int, wikibase_type: Optional[WikibaseType]
) -> bool:
    """
    Update Wikibase Type
    """

    async with get_async_session() as async_session:
        wikibase: WikibaseModel = await get_wikibase_from_database(
            async_session, wikibase_id=wikibase_id
        )
        if wikibase_type != wikibase.wikibase_type:
            wikibase.wikibase_type = wikibase_type
        await async_session.commit()

    async with get_async_session() as async_session:
        wikibase: WikibaseModel = await get_wikibase_from_database(
            async_session, wikibase_id=wikibase_id
        )
        return wikibase_type == wikibase.wikibase_type
