"""Create Quantity Data Observation"""

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
    COUNT_ITEMS_QUERY_WHERE,
    COUNT_LEXEMES_QUERY_WHERE,
    COUNT_PROPERTIES_QUERY_WHERE,
    COUNT_URL_PROPERTIES_QUERY_WHERE,
    COUNT_URL_STATEMENTS_QUERY_WHERE,
    COUNT_TRIPLES_QUERY_WHERE,
)
from fetch_data.utils import get_wikibase_from_database
from logger.get_logger import logger
from model.database import WikibaseModel, WikibaseQuantityObservationModel


COUNT_QUERIES_WHERE = [
    (
        COUNT_PROPERTIES_QUERY_WHERE,
        "Property Count",
        "total_properties",
    ),
    (
        COUNT_ITEMS_QUERY_WHERE,
        "Item Count",
        "total_items",
    ),
    (
        COUNT_LEXEMES_QUERY_WHERE,
        "Lexeme Count",
        "total_lexemes",
    ),
    (
        COUNT_TRIPLES_QUERY_WHERE,
        "Triple Count",
        "total_triples",
    ),
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
    (
        COUNT_URL_PROPERTIES_QUERY_WHERE,
        "URL Properties Count",
        "total_url_properties",
    ),
    (
        COUNT_URL_STATEMENTS_QUERY_WHERE,
        "URL Statements Count",
        "total_url_statements",
    ),
]


async def create_quantity_observation(wikibase_id: int) -> bool:
    """Create Quantity Data Observation"""

    logger.debug("Quantity: Attempting Observation", extra={"wikibase": wikibase_id})

    async with get_async_session() as async_session:
        wikibase: WikibaseModel = await get_wikibase_from_database(
            async_session=async_session,
            wikibase_id=wikibase_id,
            join_quantity_observations=True,
            require_sparql_endpoint=True,
        )

        observation = await compile_quantity_observation(wikibase)

        wikibase.quantity_observations.append(observation)

        await async_session.commit()
        return observation.returned_data


async def compile_quantity_observation(
    wikibase: WikibaseModel,
) -> WikibaseQuantityObservationModel:
    """Compile Quantity Observation"""

    observation = WikibaseQuantityObservationModel()
    observation.returned_data = False

    for query_where, label, attribute_name in COUNT_QUERIES_WHERE:
        logger.info(f"Fetching {label}", extra={"wikibase": wikibase.id})
        count_value = None

        # straight query, just as it is, counting the number of rows
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
                # exc_info=True,
                # stack_info=True,
            )
            break  # no need to try the other queries

        except (HTTPError, SPARQLResponseMalformed, URLError) as e:
            logger.warning(
                f"QuantityDataError: {e}",
                extra={"wikibase": wikibase.id},
                # exc_info=True,
                # stack_info=True,
            )
            continue  # who knows, lets try the other queries

        except EndPointInternalError:
            logger.warning(
                f"Failed to get count via sparql with simple query: {query}",
                extra={"wikibase": wikibase.id},
                # exc_info=True,
                # stack_info=True,
            )
            continue  # try the other queries for what it is worth

        assert count_value is not None
        logger.debug(
            f"Got {attribute_name}={count_value}",
            extra={"wikibase": wikibase.id},
        )
        setattr(observation, attribute_name, count_value)
        observation.returned_data = True

    return observation
