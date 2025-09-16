"""Create External Identifier Data Observation"""

from requests.exceptions import ReadTimeout, SSLError, TooManyRedirects
from urllib.error import HTTPError, URLError
from urllib3.exceptions import ConnectTimeoutError, MaxRetryError, NameResolutionError
from SPARQLWrapper.SPARQLExceptions import EndPointInternalError, EndPointNotFound

from data import get_async_session
from fetch_data.sparql_data.pull_wikidata import (
    SPARQLResponseMalformed,
    get_sparql_results,
)
from fetch_data.sparql_data.sparql_queries import (
    COUNT_EXTERNAL_IDENTIFIER_PROPERTIES_QUERY,
    COUNT_EXTERNAL_IDENTIFIER_STATEMENTS_QUERY,
    COUNT_URL_PROPERTIES_QUERY,
    COUNT_URL_STATEMENTS_QUERY,
)
from fetch_data.utils import get_wikibase_from_database
from logger import logger
from model.database import WikibaseModel, WikibaseExternalIdentifierObservationModel


async def create_external_identifier_observation(wikibase_id: int) -> bool:
    """Create External Identifier Data Observation"""

    logger.debug("EI: Attempting Observation", extra={"wikibase": wikibase_id})

    async with get_async_session() as async_session:
        wikibase: WikibaseModel = await get_wikibase_from_database(
            async_session=async_session,
            wikibase_id=wikibase_id,
            join_external_identifier_observations=True,
            require_sparql_endpoint=True,
        )

        observation = await compile_external_identifier_observation(wikibase)

        wikibase.external_identifier_observations.append(observation)

        await async_session.commit()

        logger.debug(
            "ExternalIdentifier: Observation returned data: " + str(observation.returned_data),
            extra={"wikibase": wikibase_id},
        )
        return observation.returned_data


async def compile_external_identifier_observation(
    wikibase: WikibaseModel,
) -> WikibaseExternalIdentifierObservationModel:
    """Compile External Identifier Observation"""

    observation = WikibaseExternalIdentifierObservationModel()
    try:
        logger.info(
            "Fetching External Identifier Properties Count",
            extra={"wikibase": wikibase.id},
        )
        external_identifier_properties_count_results = await get_sparql_results(
            wikibase.sparql_endpoint_url.url,
            COUNT_EXTERNAL_IDENTIFIER_PROPERTIES_QUERY,
            "COUNT_EXTERNAL_IDENTIFIER_PROPERTIES_QUERY",
        )
        observation.total_external_identifier_properties = int(
            external_identifier_properties_count_results["results"]["bindings"][0][
                "count"
            ]["value"]
        )

        logger.info(
            "Fetching External Identifier Statements Count",
            extra={"wikibase": wikibase.id},
        )
        external_identifier_statements_count_results = await get_sparql_results(
            wikibase.sparql_endpoint_url.url,
            COUNT_EXTERNAL_IDENTIFIER_STATEMENTS_QUERY,
            "COUNT_EXTERNAL_IDENTIFIER_STATEMENTS_QUERY",
        )
        observation.total_external_identifier_statements = int(
            external_identifier_statements_count_results["results"]["bindings"][0][
                "count"
            ]["value"]
        )

        logger.info(
            "Fetching URL Properties Count",
            extra={"wikibase": wikibase.id},
        )
        url_properties_count_results = await get_sparql_results(
            wikibase.sparql_endpoint_url.url,
            COUNT_URL_PROPERTIES_QUERY,
            "COUNT_URL_PROPERTIES_QUERY",
        )
        observation.total_url_properties = int(
            url_properties_count_results["results"]["bindings"][0]["count"]["value"]
        )

        logger.info(
            "Fetching URL Statements Count",
            extra={"wikibase": wikibase.id},
        )
        url_statements_count_results = await get_sparql_results(
            wikibase.sparql_endpoint_url.url,
            COUNT_URL_STATEMENTS_QUERY,
            "COUNT_URL_STATEMENTS_QUERY",
        )
        observation.total_url_statements = int(
            url_statements_count_results["results"]["bindings"][0]["count"]["value"]
        )

        observation.returned_data = True
    except (
        ConnectTimeoutError,
        ConnectionError,
        EndPointNotFound,
        MaxRetryError,
        NameResolutionError,
        ReadTimeout,
        SSLError,
        TimeoutError,
        TooManyRedirects,
    ):
        logger.error("SuspectWikibaseOfflineError", extra={"wikibase": wikibase.id})
        observation.returned_data = False
    except (EndPointInternalError, HTTPError, SPARQLResponseMalformed, URLError):
        logger.warning(
            "ExternalIdentifierDataError",
            # exc_info=True,
            # stack_info=True,
            extra={"wikibase": wikibase.id},
        )
        observation.returned_data = False

    return observation
