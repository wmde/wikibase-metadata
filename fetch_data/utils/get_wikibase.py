"""Get Wikibase"""

from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from model.database import WikibaseModel


# pylint: disable=too-many-arguments,too-many-positional-arguments
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

    query = select(WikibaseModel).where(WikibaseModel.id == wikibase_id)
    if include_observations:
        query = query.options(
            joinedload(WikibaseModel.connectivity_observations),
            joinedload(WikibaseModel.log_observations),
            joinedload(WikibaseModel.property_popularity_observations),
            joinedload(WikibaseModel.quantity_observations),
            joinedload(WikibaseModel.software_version_observations),
            joinedload(WikibaseModel.statistics_observations),
            joinedload(WikibaseModel.user_observations),
        )

    wikibase = (await async_session.scalars(query)).unique().one_or_none()
    assert wikibase is not None, "Wikibase Not Found"

    assert wikibase.checked, "Wikibase Invalid"

    if require_action_api:
        assert wikibase.action_api_url is not None, "Action API Must Be Populated"
    if require_sparql_endpoint:
        assert (
            wikibase.sparql_endpoint_url is not None
        ), "SPARQL Endpoint Must Be Populated"
    if require_special_statistics:
        assert (
            wikibase.special_statistics_url is not None
        ), "Special:Statistics URL Must Be Populated"
    if require_special_version:
        assert (
            wikibase.special_version_url is not None
        ), "Special:Version URL Must Be Populated"
    return wikibase
