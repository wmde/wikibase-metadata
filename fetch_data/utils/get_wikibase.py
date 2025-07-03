"""Get Wikibase"""

from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from logger import logger
from model.database import WikibaseModel


async def get_wikibase_from_database(
    async_session: AsyncSession,
    wikibase_id: int,
    join_connectivity_observations: bool = False,
    join_log_observations: bool = False,
    join_property_observations: bool = False,
    join_quantity_observations: bool = False,
    join_statistics_observations: bool = False,
    join_user_observations: bool = False,
    join_version_observations: bool = False,
    require_article_path: bool = False,
    require_script_path: bool = False,
    require_sparql_endpoint: bool = False,
) -> WikibaseModel:
    """Get Wikibase"""

    logger.debug("Fetching Wikibase", extra={"wikibase": wikibase_id})

    query = select(WikibaseModel).where(WikibaseModel.id == wikibase_id)
    if join_connectivity_observations:
        query = query.options(joinedload(WikibaseModel.connectivity_observations))
    if join_log_observations:
        query = query.options(joinedload(WikibaseModel.log_month_observations))
    if join_property_observations:
        query = query.options(
            joinedload(WikibaseModel.property_popularity_observations)
        )
    if join_quantity_observations:
        query = query.options(joinedload(WikibaseModel.quantity_observations))
    if join_statistics_observations:
        query = query.options(joinedload(WikibaseModel.statistics_observations))
    if join_user_observations:
        query = query.options(joinedload(WikibaseModel.user_observations))
    if join_version_observations:
        query = query.options(joinedload(WikibaseModel.software_version_observations))

    try:
        wikibase = (await async_session.scalars(query)).unique().one_or_none()
        logger.debug("Retrieved Wikibase", extra={"wikibase": wikibase_id})
        assert wikibase is not None, "Wikibase Not Found"
        assert wikibase.checked, "Wikibase Invalid"
        if require_article_path:
            assert (
                wikibase.article_path is not None
            ), "Wikibase Missing Expected articlePath"
        if require_script_path:
            assert (
                wikibase.script_path is not None
            ), "Wikibase Missing Expected scriptPath"
        if require_sparql_endpoint:
            assert (
                wikibase.sparql_endpoint_url is not None
            ), "Wikibase Missing Expected sparqlEndpointUrl"
    except Exception as exc:
        logger.error(exc, extra={"wikibase": wikibase_id})
        raise exc

    return wikibase
