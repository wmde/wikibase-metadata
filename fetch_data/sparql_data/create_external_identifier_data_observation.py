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
    COUNT_EXTERNAL_IDENTIFIER_PROPERTIES_QUERY_WHERE,
    COUNT_EXTERNAL_IDENTIFIER_STATEMENTS_QUERY_WHERE,
)
from fetch_data.utils import get_wikibase_from_database
from logger.get_logger import logger
from model.database import (
    WikibaseModel,
    WikibaseExternalIdentifierObservationModel,
)


COUNT_QUERIES_WHERE = [
    (
        COUNT_EXTERNAL_IDENTIFIER_PROPERTIES_QUERY_WHERE,
        "External Identifier Properties Count",
        "total_external_identifier_properties",
    ),
    (
        COUNT_EXTERNAL_IDENTIFIER_STATEMENTS_QUERY_WHERE,
        "External Identifier Statements Count",
        "total_external_identifier_statements",
    ),
]


async def create_external_identifier_observation(wikibase_id: int) -> bool:
    """Create External Identifier Data Observation"""

    logger.debug("ExternalIdentifier: Attempting Observation", extra={"wikibase": wikibase_id})

    async with get_async_session() as async_session:
        wikibase: WikibaseModel = await get_wikibase_from_database(
            async_session=async_session,
            wikibase_id=wikibase_id,
            join_external_identifier_observations=True,
            require_sparql_endpoint=True,
        )

        extid_observation, encountered_error = await compile_external_identifier_observation(
            wikibase
        )

        success = False
        if extid_observation.returned_data:
            wikibase.external_identifier_observations.append(extid_observation)
            success = True

        await async_session.commit()
        return success and not encountered_error


async def compile_external_identifier_observation(
    wikibase: WikibaseModel,
):
    """Compile External Identifier Observation"""

    extid_observation = WikibaseExternalIdentifierObservationModel()
    extid_observation.returned_data = False

    encountered_error = False
    for query_where, label, attribute_name in COUNT_QUERIES_WHERE:
        logger.info(f"Fetching {label}", extra={"wikibase": wikibase.id})
        count_value = None

        try:
            query = "SELECT (COUNT(*) AS ?count) WHERE {"
            query += query_where
            query += "}"
            results = await get_sparql_results(
                wikibase.sparql_endpoint_url.url, query, label
            )
            count_value = int(results["results"]["bindings"][0]["count"]["value"])

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
        ) as e:
            logger.error(
                f"SuspectWikibaseOfflineError: {e}",
                extra={"wikibase": wikibase.id},
            )
            encountered_error = True
            break

        except (HTTPError, SPARQLResponseMalformed, URLError) as e:
            logger.warning(
                f"ExternalIdentifierDataError: {e}",
                extra={"wikibase": wikibase.id},
            )
            encountered_error = True
            continue

        except EndPointInternalError:
            logger.warning(
                f"Failed to get count via sparql with simple query: {query}",
                extra={"wikibase": wikibase.id},
            )
            encountered_error = True
            continue

        except StopIteration:
            encountered_error = True
            break

        assert count_value is not None
        logger.debug(
            f"Got {attribute_name}={count_value}",
            extra={"wikibase": wikibase.id},
        )
        setattr(extid_observation, attribute_name, count_value)
        extid_observation.returned_data = True

    return extid_observation, encountered_error

