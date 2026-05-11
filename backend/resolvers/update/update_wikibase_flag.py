"""Update Wikibase Reuse Flag"""

from data.database_connection import get_async_session
from fetch_data.utils import get_wikibase_from_database
from logger import logger


async def update_wikibase_reuse_flag(wikibase_id: int, reuse: bool) -> bool:
    """Update Wikibase Reuse Flag"""

    logger.info(f"Setting Reuse Flag: {reuse}", extra={"wikibase": wikibase_id})

    async with get_async_session() as async_session:
        wikibase = await get_wikibase_from_database(async_session, wikibase_id)
        wikibase.reuse = reuse

        await async_session.commit()

    async with get_async_session() as async_session:
        wikibase = await get_wikibase_from_database(async_session, wikibase_id)

        return wikibase.reuse == reuse
