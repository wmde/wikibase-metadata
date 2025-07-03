"""Get Wikibase"""

from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from logger import logger
from model.database import WikibaseModel


async def get_wikibase_from_database(
    async_session: AsyncSession, wikibase_id: int
) -> WikibaseModel:
    """Get Wikibase"""

    logger.debug("Fetching Wikibase", extra={"wikibase": wikibase_id})

    query = select(WikibaseModel).where(WikibaseModel.id == wikibase_id)

    try:
        wikibase = (await async_session.scalars(query)).unique().one_or_none()
    except Exception as exc:
        logger.error(exc, extra={"wikibase": wikibase_id})
        raise exc

    logger.debug(
        f"Wikibase Is Not None: {wikibase is not None}", extra={"wikibase": wikibase_id}
    )
    assert wikibase is not None, "Wikibase Not Found"

    logger.debug(
        f"Wikibase Is Checked: {wikibase.checked}", extra={"wikibase": wikibase_id}
    )
    assert wikibase.checked, "Wikibase Invalid"

    return wikibase
