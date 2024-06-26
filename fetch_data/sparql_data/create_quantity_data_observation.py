"""Create User Data Observation"""

from urllib.error import HTTPError
from SPARQLWrapper.SPARQLExceptions import EndPointInternalError
from data import get_async_session
from fetch_data.sparql_data.pull_wikidata import get_results
from fetch_data.sparql_data.sparql_queries import (
    COUNT_ITEMS_QUERY,
    COUNT_LEXEMES_QUERY,
    COUNT_PROPERTIES_QUERY,
)
from fetch_data.utils.get_wikibase import get_wikibase_from_database
from model.database import WikibaseQuantityObservationModel


async def create_quantity_data_observation(wikibase_id: int) -> bool:
    """Create Quantity Data Observation"""

    async with get_async_session() as async_session:
        wikibase = await get_wikibase_from_database(
            async_session=async_session,
            wikibase_id=wikibase_id,
            require_sparql_endpoint=True,
        )

        observation = compile_quantity_observation(wikibase.sparql_endpoint_url.url)

        wikibase.quantity_observations.append(observation)

        await async_session.commit()
        return observation.returned_data


def compile_quantity_observation(
    sparql_endpoint_url: str,
) -> WikibaseQuantityObservationModel:
    """Compile Quantity Observation"""

    observation = WikibaseQuantityObservationModel()
    try:
        print("FETCHING PROPERTY COUNT")
        property_count_results = get_results(
            sparql_endpoint_url, COUNT_PROPERTIES_QUERY, "COUNT_PROPERTIES_QUERY"
        )
        observation.total_properties = int(
            property_count_results["results"]["bindings"][0]["count"]["value"]
        )

        print("FETCHING ITEM COUNT")
        item_count_results = get_results(
            sparql_endpoint_url, COUNT_ITEMS_QUERY, "COUNT_ITEMS_QUERY"
        )
        observation.total_items = int(
            item_count_results["results"]["bindings"][0]["count"]["value"]
        )

        print("FETCHING LEXEME COUNT")
        lexeme_count_results = get_results(
            sparql_endpoint_url, COUNT_LEXEMES_QUERY, "COUNT_LEXEMES_QUERY"
        )
        observation.total_lexemes = int(
            lexeme_count_results["results"]["bindings"][0]["count"]["value"]
        )

        observation.returned_data = True
    except (HTTPError, EndPointInternalError):
        observation.returned_data = False

    return observation
