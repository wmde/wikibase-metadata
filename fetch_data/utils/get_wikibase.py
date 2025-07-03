"""Get Wikibase"""

from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from logger import logger
from model.database import WikibaseModel


async def get_wikibase_from_database(
    async_session: AsyncSession,
    wikibase_id: int,
    include_observations: bool = False,
    require_action_api: bool = False,
    require_sparql_endpoint: bool = False,
    require_special_statistics: bool = False,
    require_special_version: bool = False,
) -> WikibaseModel:
    """Get Wikibase"""

    logger.debug("Fetching Wikibase", extra={"wikibase": wikibase_id})

    query = select(WikibaseModel).where(WikibaseModel.id == wikibase_id)
    if include_observations:
        query = query.options(
            joinedload(WikibaseModel.connectivity_observations),
            joinedload(WikibaseModel.log_month_observations),
            joinedload(WikibaseModel.property_popularity_observations),
            joinedload(WikibaseModel.quantity_observations),
            joinedload(WikibaseModel.software_version_observations),
            joinedload(WikibaseModel.statistics_observations),
            joinedload(WikibaseModel.user_observations),
        )

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

    if require_action_api:
        logger.debug(
            f"Wikibase Has scriptPath: {wikibase.script_path is not None}",
            extra={"wikibase": wikibase_id},
        )
        assert wikibase.script_path is not None, "Script Path Must Be Populated"
    if require_sparql_endpoint:
        logger.debug(
            f"Wikibase Has sparqlEndpointUrl: {wikibase.sparql_endpoint_url is not None}",
            extra={"wikibase": wikibase_id},
        )
        assert (
            wikibase.sparql_endpoint_url is not None
        ), "SPARQL Endpoint Must Be Populated"
    if require_special_statistics or require_special_version:
        logger.debug(
            f"Wikibase Has articlePath: {wikibase.article_path is not None}",
            extra={"wikibase": wikibase_id},
        )
        assert wikibase.article_path is not None, "Article Path Must Be Populated"

    return wikibase
