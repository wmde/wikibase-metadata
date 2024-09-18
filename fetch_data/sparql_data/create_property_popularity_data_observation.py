"""Create Property Popularity Data Observation"""

from urllib.error import HTTPError
from SPARQLWrapper.SPARQLExceptions import EndPointInternalError
from data import get_async_session
from fetch_data.sparql_data.pull_wikidata import get_results
from fetch_data.sparql_data.sparql_queries import PROPERTY_POPULARITY_QUERY
from fetch_data.utils.get_wikibase import get_wikibase_from_database
from model.database import (
    WikibasePropertyPopularityCountModel,
    WikibasePropertyPopularityObservationModel,
)


async def create_property_popularity_observation(wikibase_id: int) -> bool:
    """Create Property Popularity Observation"""

    async with get_async_session() as async_session:
        wikibase = await get_wikibase_from_database(
            async_session=async_session,
            wikibase_id=wikibase_id,
            include_observations=True,
            require_sparql_endpoint=True,
        )

        observation = compile_property_popularity_observation(
            wikibase.sparql_endpoint_url.url
        )

        wikibase.property_popularity_observations.append(observation)

        await async_session.commit()
        return observation.returned_data


def compile_property_popularity_observation(
    sparql_endpoint_url: str,
) -> WikibasePropertyPopularityObservationModel:
    """Compile Property Popularity Observation"""

    observation = WikibasePropertyPopularityObservationModel()

    try:
        print("FETCHING PROPERTY DATA")
        property_count_results = get_results(
            sparql_endpoint_url, PROPERTY_POPULARITY_QUERY, "PROPERTY_POPULARITY_QUERY"
        )

        observation.returned_data = True

        for result in property_count_results["results"]["bindings"]:
            record = WikibasePropertyPopularityCountModel(
                property_url=result["property"]["value"],
                usage_count=result["propertyCount"]["value"],
            )
            observation.property_count_observations.append(record)
    except (HTTPError, EndPointInternalError):
        observation.returned_data = False
    return observation
