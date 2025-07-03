"""Create Connectivity Data Observation"""

import asyncio
from json import JSONDecodeError
from typing import Optional
from urllib.error import HTTPError, URLError
import numpy
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from SPARQLWrapper.SPARQLExceptions import EndPointInternalError

from data import get_async_session
from fetch_data.sparql_data.connectivity_math import (
    compile_distance_dict,
    compile_link_dict,
)
from fetch_data.sparql_data.pull_wikidata import get_sparql_results
from fetch_data.sparql_data.sparql_queries import ITEM_LINKS_QUERY, clean_item_link_data
from fetch_data.utils import counts
from logger import logger
from model.database import (
    WikibaseModel,
    WikibaseConnectivityObservationModel,
    WikibaseConnectivityObservationItemRelationshipCountModel,
    WikibaseConnectivityObservationObjectRelationshipCountModel,
)


async def create_connectivity_observation(wikibase_id: int) -> bool:
    """Create Connectivity Data Observation"""

    async with get_async_session() as async_session:
        wikibase: WikibaseModel = await fetch_wikibase(
            async_session=async_session, wikibase_id=wikibase_id
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

    except (EndPointInternalError, JSONDecodeError, HTTPError, URLError):
        logger.warning(
            "ConnectivityDataError",
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
                    .options(joinedload(WikibaseModel.connectivity_observations))
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

    logger.debug("Connectivity: Retrieved Wikibase", extra={"wikibase": wikibase_id})
    return wikibase
