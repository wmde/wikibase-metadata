"""Update Wikibase URL"""

from typing import Optional

from sqlalchemy import and_, delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from data.database_connection import get_async_session
from model.database.wikibase_url_model import WikibaseURLModel
from model.enum import WikibaseURLType
from logger import logger
from resolvers.util.clean_wikibase_url import clean_up_url


async def upsert_wikibase_url(
    wikibase_id: int, url: str, url_type: WikibaseURLType
) -> bool:
    """Add or Update Wikibase URL"""

    assert url_type != WikibaseURLType.ACTION_QUERY_URL, "Please use `SCRIPT_PATH`"
    assert url_type != WikibaseURLType.INDEX_QUERY_URL, "Please use `SCRIPT_PATH`"
    assert (
        url_type != WikibaseURLType.SPARQL_QUERY_URL
    ), "Please use `SPARQL_FRONTEND_URL`"
    assert (
        url_type != WikibaseURLType.SPECIAL_STATISTICS_URL
    ), "Please use `ARTICLE_PATH`"
    assert url_type != WikibaseURLType.SPECIAL_VERSION_URL, "Please use `ARTICLE_PATH`"

    clean_url = clean_up_url(url, url_type)

    logger.info(f"Upserting {url_type}: {clean_url}", extra={"wikibase": wikibase_id})

    async with get_async_session() as async_session:
        wikibase_url: Optional[WikibaseURLModel] = await fetch_wikibase_url(
            async_session, wikibase_id, url_type
        )

        if wikibase_url is not None:
            wikibase_url.url = clean_url
        else:
            async_session.add(
                WikibaseURLModel(wikibase_id=wikibase_id, url=url, url_type=url_type)
            )

        await async_session.commit()

    async with get_async_session() as async_session:
        wikibase_url: Optional[WikibaseURLModel] = await fetch_wikibase_url(
            async_session, wikibase_id, url_type
        )

        return wikibase_url is not None and wikibase_url.url == clean_url


async def remove_wikibase_url(wikibase_id: int, url_type: WikibaseURLType) -> bool:
    """Remove URL from Wikibase"""

    assert url_type != WikibaseURLType.BASE_URL, "CANNOT DELETE BASE URL"

    logger.info(f"Removing {url_type}", extra={"wikibase": wikibase_id})

    async with get_async_session() as async_session:
        await async_session.execute(
            delete(WikibaseURLModel).where(
                and_(
                    WikibaseURLModel.wikibase_id == wikibase_id,
                    WikibaseURLModel.url_type == url_type,
                )
            )
        )
        await async_session.commit()

    async with get_async_session() as async_session:
        wikibase_url: Optional[WikibaseURLModel] = await fetch_wikibase_url(
            async_session, wikibase_id, url_type
        )

        return wikibase_url is None


async def fetch_wikibase_url(
    async_session: AsyncSession, wikibase_id: int, url_type: WikibaseURLType
) -> Optional[WikibaseURLModel]:
    """Fetch WikibaseURL from Database"""

    return (
        await async_session.scalars(
            select(WikibaseURLModel).where(
                and_(
                    WikibaseURLModel.wikibase_id == wikibase_id,
                    WikibaseURLModel.url_type == url_type,
                )
            )
        )
    ).one_or_none()
