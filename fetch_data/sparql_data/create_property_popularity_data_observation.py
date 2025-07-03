"""Create Property Popularity Data Observation"""

from typing import Optional
from urllib.error import HTTPError
from SPARQLWrapper.SPARQLExceptions import EndPointInternalError
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from data import get_async_session
from fetch_data.sparql_data.pull_wikidata import get_sparql_results
from fetch_data.sparql_data.sparql_queries import PROPERTY_POPULARITY_QUERY
from logger import logger
from model.database import (
    WikibaseModel,
    WikibasePropertyPopularityCountModel,
    WikibasePropertyPopularityObservationModel,
)


async def create_property_popularity_observation(wikibase_id: int) -> bool:
    """Create Property Popularity Observation"""

    async with get_async_session() as async_session:
        wikibase = await fetch_wikibase(
            async_session=async_session, wikibase_id=wikibase_id
        )

        observation = await compile_property_popularity_observation(wikibase)

        wikibase.property_popularity_observations.append(observation)

        await async_session.commit()
        return observation.returned_data


async def compile_property_popularity_observation(
    wikibase: WikibaseModel,
) -> WikibasePropertyPopularityObservationModel:
    """Compile Property Popularity Observation"""

    observation = WikibasePropertyPopularityObservationModel()

    try:
        logger.info("Fetching Property Data", extra={"wikibase": wikibase.id})
        property_count_results = await get_sparql_results(
            wikibase.sparql_endpoint_url.url,
            PROPERTY_POPULARITY_QUERY,
            "PROPERTY_POPULARITY_QUERY",
        )

        observation.returned_data = True

        for result in property_count_results["results"]["bindings"]:
            record = WikibasePropertyPopularityCountModel(
                property_url=result["property"]["value"],
                usage_count=result["propertyCount"]["value"],
            )
            observation.property_count_observations.append(record)
    except (HTTPError, EndPointInternalError):
        logger.warning(
            "PropertyPopularityDataError",
            exc_info=True,
            stack_info=True,
            extra={"wikibase": wikibase.id},
        )
        observation.returned_data = False
    return observation


async def fetch_wikibase(
    async_session: AsyncSession, wikibase_id: int
) -> WikibaseModel:
    """Fetch Wikibase"""

    try:
        wikibase: Optional[WikibaseModel] = (
            (
                await async_session.scalars(
                    select(WikibaseModel)
                    .options(joinedload(WikibaseModel.property_popularity_observations))
                    .where(WikibaseModel.id == wikibase_id)
                )
            )
            .unique()
            .one_or_none()
        )
    except Exception as exc:
        logger.error(exc, extra={"wikibase": wikibase_id})
        raise exc
    try:
        assert wikibase is not None
        assert wikibase.sparql_endpoint_url is not None
    except AssertionError as exc:
        logger.error(exc, extra={"wikibase": wikibase_id})
        raise exc

    logger.debug("Property: Retrieved Wikibase", extra={"wikibase": wikibase_id})
    return wikibase
