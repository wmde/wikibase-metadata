"""Create Connectivity Data Observation"""

from json import JSONDecodeError
from urllib.error import HTTPError, URLError
from SPARQLWrapper.SPARQLExceptions import EndPointInternalError
import numpy
from data import get_async_session
from fetch_data.sparql_data.connectivity_math import (
    compile_distance_dict,
    compile_link_dict,
)
from fetch_data.sparql_data.pull_wikidata import get_results
from fetch_data.sparql_data.sparql_queries import ITEM_LINKS_QUERY, clean_item_link_data
from fetch_data.utils import counts, get_wikibase_from_database
from model.database import (
    WikibaseConnectivityObservationItemRelationshipCountModel,
    WikibaseConnectivityObservationObjectRelationshipCountModel,
    WikibaseConnectivityObservationModel,
    WikibaseModel,
)


async def create_connectivity_observation(wikibase_id: int) -> bool:
    """Create Connectivity Data Observation"""

    async with get_async_session() as async_session:
        wikibase: WikibaseModel = await get_wikibase_from_database(
            async_session=async_session,
            wikibase_id=wikibase_id,
            require_sparql_endpoint=True,
        )

        observation = compile_connectivity_observation(wikibase.sparql_endpoint_url.url)

        wikibase.connectivity_observations.append(observation)

        await async_session.commit()
        return observation.returned_data


def compile_connectivity_observation(
    sparql_endpoint_url: str,
) -> WikibaseConnectivityObservationModel:
    """Compile Connectivity Observation"""

    observation = WikibaseConnectivityObservationModel()
    try:
        print("FETCHING ITEM LINKS")
        item_link_results = get_results(
            sparql_endpoint_url, ITEM_LINKS_QUERY, "ITEM_LINKS_QUERY"
        )

        clean_data = clean_item_link_data(item_link_results)

        observation.returned_data = True
        observation.returned_links = len(clean_data)

        if observation.returned_links > 0:
            print(f"RUNNING ITEM LINK MATH: {observation.returned_links}")

            all_nodes = sorted(
                {p.item_from for p in clean_data} | {p.item_to for p in clean_data}
            )

            print("\tCalculating Item Link Counts")
            item_link_dict = compile_link_dict(clean_data, all_nodes)
            item_link_counts = counts([len(a) for a in item_link_dict.values()])
            for link_count, item_count in item_link_counts.items():
                observation.item_relationship_count_observations.append(
                    WikibaseConnectivityObservationItemRelationshipCountModel(
                        relationship_count=link_count, item_count=item_count
                    )
                )

            print("\tCalculating Object Link Counts")
            object_link_dict = compile_link_dict(clean_data, all_nodes, reverse=True)
            object_link_counts = counts([len(a) for a in object_link_dict.values()])
            for link_count, object_count in object_link_counts.items():
                observation.object_relationship_count_observations.append(
                    WikibaseConnectivityObservationObjectRelationshipCountModel(
                        relationship_count=link_count, object_count=object_count
                    )
                )

            print("\tCalculating Distance Dict")
            distance_dict = compile_distance_dict(all_nodes, item_link_dict)

            all_nonzero_distances = [
                distance
                for value in distance_dict.values()
                for distance in value.values()
                if distance > 0
            ]

            print("\tCalculating Connectivity")
            observation.connectivity = (
                (len(all_nonzero_distances) / (len(all_nodes) * (len(all_nodes) - 1)))
                if (len(all_nodes) * (len(all_nodes) - 1) != 0)
                else None
            )
            print("\tCalculating Average Connected Distance")
            observation.average_connected_distance = (
                numpy.mean(all_nonzero_distances)
                if len(all_nonzero_distances) > 0
                else None
            )

    except (EndPointInternalError, JSONDecodeError, HTTPError, URLError):
        observation.returned_data = False

    return observation
