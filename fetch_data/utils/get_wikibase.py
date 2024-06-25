"""Get Wikibase"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from model.database import WikibaseModel


async def get_wikibase_from_database(
    async_session: AsyncSession,
    wikibase_id: int,
    require_sparql_endpoint: bool = False,
    require_special_version: bool = False,
) -> WikibaseModel:
    """Get Wikibase"""

    wikibase = (
        await async_session.scalars(
            select(WikibaseModel).where(WikibaseModel.id == wikibase_id)
        )
    ).one_or_none()
    assert wikibase is not None, "Wikibase Not Found"
    if require_sparql_endpoint:
        assert (
            wikibase.sparql_endpoint_url is not None
        ), "SPARQL Endpoint Must Be Populated"
    if require_special_version:
        assert (
            wikibase.special_version_url is not None
        ), "Special:Version URL Must Be Populated"
    return wikibase
