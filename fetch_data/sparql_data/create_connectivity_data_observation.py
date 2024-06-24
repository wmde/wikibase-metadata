"""Create User Data Observation"""

from json import JSONDecodeError
from typing import List
from urllib.error import HTTPError, URLError
from SPARQLWrapper.SPARQLExceptions import EndPointInternalError
import numpy
from data import get_async_session
from fetch_data.sparql_data.pull_wikidata import get_results
from fetch_data.sparql_data.sparql_queries import (
    ITEM_LINKS_QUERY,
    ItemLink,
    clean_item_link_data,
)
from fetch_data.utils import counts, get_wikibase_from_database
from model.database import (
    WikibaseConnectivityObservationItemRelationshipCountModel,
    WikibaseConnectivityObservationObjectRelationshipCountModel,
    WikibaseConnectivityObservationModel,
)


async def create_connectivity_data_observation(wikibase_id: int) -> bool:
    """Create Connectivity Data Observation"""

    async with get_async_session() as async_session:
        wikibase = await get_wikibase_from_database(
            async_session=async_session, wikibase_id=wikibase_id
        )
        assert (
            wikibase.sparql_endpoint_url is not None
        ), "SPARQL Endpoint Must Be Populated"

        observation = compile_connectivity_observation(wikibase.sparql_endpoint_url)

        wikibase.connectivity_observations.append(observation)

        await async_session.commit()
        return observation.returned_data


def compile_connectivity_observation(
    sparql_endpoint_url: str,
) -> WikibaseConnectivityObservationModel:
    """Compile Quantity Observation"""

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
            item_link_dict = compile_link_dict(clean_data, all_nodes)

            print("\tCalculating Item Link Counts")
            item_link_counts = counts([len(a) for a in item_link_dict.values()])
            for link_count, item_count in item_link_counts.items():
                observation.item_relationship_count_observations.append(
                    WikibaseConnectivityObservationItemRelationshipCountModel(
                        relationship_count=link_count, item_count=item_count
                    )
                )

            unique_connection_count = numpy.dot(
                [int(k) for k in item_link_counts.keys()],
                [int(v) for v in item_link_counts.values()],
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

            print(
                f"\tCalculating Distance Dict: {len(all_nodes)}, {unique_connection_count}"
            )
            distance_dict = compile_distance_dict(all_nodes, item_link_dict)

            all_nonzero_distances = [
                distance
                for value in distance_dict.values()
                for distance in value.values()
                if distance > 0
            ]

            print("\tCalculating Connectivity")
            observation.connectivity = len(all_nonzero_distances) / (
                len(all_nodes) * (len(all_nodes) - 1)
            )
            print("\tCalculating Average Connected Distance")
            observation.average_connected_distance = numpy.mean(all_nonzero_distances)

    except (EndPointInternalError, JSONDecodeError, HTTPError, URLError):
        observation.returned_data = False

    return observation


def compile_distance_dict(
    all_nodes: List[str], link_dict: dict[str, set[str]]
) -> dict[str, dict[str, int]]:
    """Compile Distance Dictionary"""
    distance_dict: dict[str, dict[str, int]] = {}

    for node in all_nodes:
        distance_dict[node] = {}
        returning = True
        step = 0
        while returning:
            step_list = nth_step(link_dict, {node}, step) - set(
                distance_dict[node].keys()
            )
            returning = len(step_list) > 0
            for n in step_list:
                distance_dict[node][n] = step
            step += 1
        if node.endswith('0'):
            print(f"\t\t{node}: {step-1}")
    return distance_dict


def compile_link_dict(
    clean_data: List[ItemLink], all_nodes: List[str], reverse: bool = False
) -> dict[str, set[str]]:
    """Compile Connection Dictionary"""

    link_dict: dict[str, set[str]] = {}

    for node in all_nodes:
        link_dict[node] = set()
    for point in clean_data:
        link_dict[point.item_from if not reverse else point.item_to].add(
            point.item_to if not reverse else point.item_from
        )
    for node in all_nodes:
        link_dict[node].discard(node)
    return link_dict


def next_step(link_dict: dict[str, set[str]], node_list: set[str]) -> set[str]:
    """Return all nodes any node in the list is linked to"""

    return {n for node in node_list for n in link_dict[node]}


def nth_step(
    link_dict: dict[str, set[str]], node_list: set[str], step: int
) -> set[str]:
    """Return all nodes any node in the list is linked to, over n recursive steps"""

    if step < 0:
        raise ValueError("Step Cannot Be Negative")
    if step == 0:
        return node_list
    return nth_step(link_dict, next_step(link_dict, node_list), step - 1)
