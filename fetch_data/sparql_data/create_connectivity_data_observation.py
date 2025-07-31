"""Create Connectivity Data Observation"""

import asyncio
from json import JSONDecodeError
from urllib.error import HTTPError, URLError
import numpy
from SPARQLWrapper.SPARQLExceptions import EndPointInternalError

from data import get_async_session
from fetch_data.sparql_data.connectivity_math import (
    compile_distance_dict,
    compile_link_dict,
)
from fetch_data.sparql_data.pull_wikidata import get_sparql_results
from fetch_data.sparql_data.sparql_queries import ITEM_LINKS_QUERY, clean_item_link_data
from fetch_data.utils import counts, get_wikibase_from_database
from logger import logger
from model.database import (
    WikibaseConnectivityObservationModel,
    WikibaseConnectivityObservationItemRelationshipCountModel,
    WikibaseConnectivityObservationObjectRelationshipCountModel,
    WikibaseModel,
)


async def create_connectivity_observation(wikibase_id: int) -> bool:
    """Create Connectivity Data Observation"""

    logger.debug(
        "Connectivity: Attempting Observation", extra={"wikibase": wikibase_id}
    )

    async with get_async_session() as async_session:
        wikibase: WikibaseModel = await get_wikibase_from_database(
            async_session=async_session,
            wikibase_id=wikibase_id,
            join_connectivity_observations=True,
            require_sparql_endpoint=True,
        )

        observation = await compile_connectivity_observation(wikibase)

        wikibase.connectivity_observations.append(observation)

        await async_session.commit()
        return observation.returned_data


async def compile_connectivity_observation(
    wikibase: WikibaseModel,
) -> WikibaseConnectivityObservationModel:
    """Compile Connectivity Observation"""

    observation = WikibaseConnectivityObservationModel()
    try:
        logger.info("Fetching Item Links", extra={"wikibase": wikibase.id})
        item_link_results = await get_sparql_results(
            wikibase.sparql_endpoint_url.url, ITEM_LINKS_QUERY, "ITEM_LINKS_QUERY"
        )

        clean_data = clean_item_link_data(item_link_results)

        observation.returned_data = True
        observation.returned_links = len(clean_data)

        if observation.returned_links > 0:
            logger.info(
                f"Running Item Link Math: {observation.returned_links}",
                extra={"wikibase": wikibase.id},
            )

            all_nodes = sorted(
                {p.item_from for p in clean_data} | {p.item_to for p in clean_data}
            )

            logger.debug(
                "Calculating Item Link Counts", extra={"wikibase": wikibase.id}
            )
            item_link_dict = compile_link_dict(clean_data, all_nodes)
            item_link_counts = counts([len(a) for a in item_link_dict.values()])
            for link_count, item_count in item_link_counts.items():
                observation.item_relationship_count_observations.append(
                    WikibaseConnectivityObservationItemRelationshipCountModel(
                        relationship_count=link_count, item_count=item_count
                    )
                )

            logger.debug(
                "Calculating Object Link Counts", extra={"wikibase": wikibase.id}
            )
            object_link_dict = compile_link_dict(clean_data, all_nodes, reverse=True)
            object_link_counts = counts([len(a) for a in object_link_dict.values()])
            for link_count, object_count in object_link_counts.items():
                observation.object_relationship_count_observations.append(
                    WikibaseConnectivityObservationObjectRelationshipCountModel(
                        relationship_count=link_count, object_count=object_count
                    )
                )

            logger.debug("Calculating Distance Dict", extra={"wikibase": wikibase.id})
            distance_dict = await asyncio.to_thread(
                compile_distance_dict, all_nodes, item_link_dict
            )

            all_nonzero_distances = [
                distance
                for value in distance_dict.values()
                for distance in value.values()
                if distance > 0
            ]

            logger.debug("Calculating Connectivity", extra={"wikibase": wikibase.id})
            observation.connectivity = (
                (len(all_nonzero_distances) / (len(all_nodes) * (len(all_nodes) - 1)))
                if (len(all_nodes) * (len(all_nodes) - 1) != 0)
                else None
            )
            logger.debug(
                "Calculating Average Connected Distance",
                extra={"wikibase": wikibase.id},
            )
            observation.average_connected_distance = (
                numpy.mean(all_nonzero_distances)
                if len(all_nonzero_distances) > 0
                else None
            )

    except (
        ConnectionError,
        EndPointInternalError,
        JSONDecodeError,
        HTTPError,
        URLError,
    ):
        logger.warning(
            "ConnectivityDataError",
            # exc_info=True,
            # stack_info=True,
            extra={"wikibase": wikibase.id},
        )
        observation.returned_data = False

    return observation
