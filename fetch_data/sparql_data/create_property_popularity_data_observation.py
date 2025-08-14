"""Create Property Popularity Data Observation"""

from requests.exceptions import ReadTimeout, SSLError, TooManyRedirects
from urllib.error import HTTPError, URLError
from urllib3.exceptions import ConnectTimeoutError, MaxRetryError, NameResolutionError
from SPARQLWrapper.SPARQLExceptions import EndPointInternalError, EndPointNotFound

from data import get_async_session
from fetch_data.sparql_data.pull_wikidata import get_sparql_results
from fetch_data.sparql_data.sparql_queries import PROPERTY_POPULARITY_QUERY
from fetch_data.utils.get_wikibase import get_wikibase_from_database
from logger import logger
from model.database import (
    WikibaseModel,
    WikibasePropertyPopularityCountModel,
    WikibasePropertyPopularityObservationModel,
)


async def create_property_popularity_observation(wikibase_id: int) -> bool:
    """Create Property Popularity Observation"""

    logger.debug("Property: Attempting Observation", extra={"wikibase": wikibase_id})

    async with get_async_session() as async_session:
        wikibase = await get_wikibase_from_database(
            async_session=async_session,
            wikibase_id=wikibase_id,
            join_property_popularity_observations=True,
            require_sparql_endpoint=True,
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
    except (
        ConnectTimeoutError,
        ConnectionError,
        EndPointNotFound,
        MaxRetryError,
        NameResolutionError,
        ReadTimeout,
        SSLError,
        TooManyRedirects,
    ):
        logger.error("SuspectWikibaseOfflineError", extra={"wikibase": wikibase.id})
        observation.returned_data = False
    except (EndPointInternalError, HTTPError, URLError):
        logger.warning(
            "PropertyPopularityDataError",
            # exc_info=True,
            # stack_info=True,
            extra={"wikibase": wikibase.id},
        )
        observation.returned_data = False
    return observation
