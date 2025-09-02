"""
Update Observations in Bulk

Allow up to 4 simultaneous tasks across all observation types
"""

import asyncio
from sqlalchemy import Select
from fetch_data.api_data import (
    create_log_observation,
    create_recent_changes_observation,
    create_time_to_first_value_observation,
    create_user_observation,
)
from fetch_data.bulk.get_wikibase_list import get_wikibase_list
from fetch_data.soup_data import (
    create_software_version_observation,
    create_special_statistics_observation,
)
from fetch_data.sparql_data import (
    create_connectivity_observation,
    create_property_popularity_observation,
    create_quantity_observation,
)
from logger import logger
from model.database.wikibase_model import WikibaseModel
from model.strawberry.output import BulkTaskResult


sem = asyncio.Semaphore(4)


async def safe_update_connectivity_obs(wikibase_id: int) -> bool:
    """Waits for available worker, returns success/failure boolean"""
    async with sem:
        try:
            return await create_connectivity_observation(wikibase_id)
        # pylint: disable-next=bare-except
        except:
            logger.error(
                "ConnectivityDataError",
                exc_info=True,
                stack_info=True,
                extra={"wikibase": wikibase_id},
            )
        return False


async def update_bulk_connectivity_observations(
    query: Select[tuple[WikibaseModel]],
) -> BulkTaskResult:
    """Update Connectivity Observations"""

    wikibases = await get_wikibase_list(query)
    logger.info(f"Connectivity: {len(wikibases)} Wikibases to Update")

    tasks = [
        asyncio.ensure_future(safe_update_connectivity_obs(wiki.id))
        for wiki in wikibases
    ]
    await asyncio.gather(*tasks)

    return BulkTaskResult(tasks)


async def safe_update_log_obs(wikibase_id: int, first_month: bool) -> bool:
    """Waits for available worker, returns success/failure boolean"""
    async with sem:
        try:
            return await create_log_observation(wikibase_id, first_month=first_month)
        # pylint: disable-next=bare-except
        except:
            logger.error(
                "LogDataError",
                exc_info=True,
                stack_info=True,
                extra={"wikibase": wikibase_id},
            )
        return False


async def update_bulk_log_observations(
    query: Select[tuple[WikibaseModel]], first_month: bool
) -> BulkTaskResult:
    """Update Log (First Month) Observations"""

    wikibases = await get_wikibase_list(query)
    logger.info(f"Log (First Month): {len(wikibases)} Wikibases to Update")

    tasks = [
        asyncio.ensure_future(safe_update_log_obs(wiki.id, first_month=first_month))
        for wiki in wikibases
    ]
    await asyncio.gather(*tasks)

    return BulkTaskResult(tasks)


async def safe_update_property_obs(wikibase_id: int) -> bool:
    """Waits for available worker, returns success/failure boolean"""
    async with sem:
        try:
            return await create_property_popularity_observation(wikibase_id)
        # pylint: disable-next=bare-except
        except:
            logger.error(
                "PropertyPopularityDataError",
                exc_info=True,
                stack_info=True,
                extra={"wikibase": wikibase_id},
            )
        return False


async def update_bulk_property_observations(
    query: Select[tuple[WikibaseModel]],
) -> BulkTaskResult:
    """Update Property Popularity Observations"""

    wikibases = await get_wikibase_list(query)
    logger.info(f"Property Popularity: {len(wikibases)} Wikibases to Update")

    tasks = [
        asyncio.ensure_future(safe_update_property_obs(wiki.id)) for wiki in wikibases
    ]
    await asyncio.gather(*tasks)

    return BulkTaskResult(tasks)


async def safe_update_quantity_obs(wikibase_id: int) -> bool:
    """Waits for available worker, returns success/failure boolean"""
    async with sem:
        try:
            return await create_quantity_observation(wikibase_id)
        # pylint: disable-next=bare-except
        except:
            logger.error(
                "QuantityDataError",
                exc_info=True,
                stack_info=True,
                extra={"wikibase": wikibase_id},
            )
        return False


async def update_bulk_quantity_observations(
    query: Select[tuple[WikibaseModel]],
) -> BulkTaskResult:
    """Update Bulk Quantity Observations"""

    wikibases = await get_wikibase_list(query)
    logger.info(f"Quantity: {len(wikibases)} Wikibases to Update")

    tasks = [
        asyncio.ensure_future(safe_update_quantity_obs(wiki.id)) for wiki in wikibases
    ]
    await asyncio.gather(*tasks)

    return BulkTaskResult(tasks)


async def safe_update_recent_changes_obs(wikibase_id: int) -> bool:
    """Waits for available worker, returns success/failure boolean"""
    async with sem:
        try:
            return await create_recent_changes_observation(wikibase_id)
        # pylint: disable-next=bare-except
        except:
            logger.error(
                "RecentChangesDataError",
                exc_info=True,
                stack_info=True,
                extra={"wikibase": wikibase_id},
            )
        return False


async def update_bulk_recent_changes_observations(
    query: Select[tuple[WikibaseModel]],
) -> BulkTaskResult:
    """Update Recent Changes Observations"""

    wikibases = await get_wikibase_list(query)
    logger.info(f"Recent Changes: {len(wikibases)} Wikibases to Update")

    tasks = [
        asyncio.ensure_future(safe_update_recent_changes_obs(wiki.id))
        for wiki in wikibases
    ]
    await asyncio.gather(*tasks)

    return BulkTaskResult(tasks)


async def safe_update_software_obs(wikibase_id: int) -> bool:
    """Waits for available worker, returns success/failure boolean"""
    async with sem:
        try:
            return await create_software_version_observation(wikibase_id, None)
        # pylint: disable-next=bare-except
        except:
            logger.error(
                "SoftwareVersionDataError",
                exc_info=True,
                stack_info=True,
                extra={"wikibase": wikibase_id},
            )
        return False


async def update_bulk_software_observations(
    query: Select[tuple[WikibaseModel]],
) -> BulkTaskResult:
    """Update Software Version Observations"""

    wikibases = await get_wikibase_list(query)
    logger.info(f"Software Version: {len(wikibases)} Wikibases to Update")

    tasks = [
        asyncio.ensure_future(safe_update_software_obs(wiki.id)) for wiki in wikibases
    ]
    await asyncio.gather(*tasks)

    return BulkTaskResult(tasks)


async def safe_update_stats_obs(wikibase_id: int) -> bool:
    """Waits for available worker, returns success/failure boolean"""
    async with sem:
        try:
            return await create_special_statistics_observation(wikibase_id)
        # pylint: disable-next=bare-except
        except:
            logger.error(
                "StatisticsDataError",
                exc_info=True,
                stack_info=True,
                extra={"wikibase": wikibase_id},
            )
        return False


async def update_bulk_stats_observations(
    query: Select[tuple[WikibaseModel]],
) -> BulkTaskResult:
    """Update Special:Statistics Observations"""

    wikibases = await get_wikibase_list(query)
    logger.info(f"Statistics: {len(wikibases)} Wikibases to Update")

    tasks = [
        asyncio.ensure_future(safe_update_stats_obs(wiki.id)) for wiki in wikibases
    ]
    await asyncio.gather(*tasks)

    return BulkTaskResult(tasks)


async def safe_update_ttfv_obs(wikibase_id: int) -> bool:
    """Waits for available worker, returns success/failure boolean"""
    async with sem:
        try:
            return await create_time_to_first_value_observation(wikibase_id)
        # pylint: disable-next=bare-except
        except:
            logger.error(
                "TimeToFirstValueDataError",
                exc_info=True,
                stack_info=True,
                extra={"wikibase": wikibase_id},
            )
        return False


async def update_bulk_time_to_first_value_observations(
    query: Select[tuple[WikibaseModel]],
) -> BulkTaskResult:
    """Update Time to First Value Observations"""

    wikibases = await get_wikibase_list(query)
    logger.info(f"Time to First Value: {len(wikibases)} Wikibases to Update")

    tasks = [asyncio.ensure_future(safe_update_ttfv_obs(wiki.id)) for wiki in wikibases]
    await asyncio.gather(*tasks)

    return BulkTaskResult(tasks)


async def safe_update_user_obs(wikibase_id: int) -> bool:
    """Waits for available worker, returns success/failure boolean"""
    async with sem:
        try:
            return await create_user_observation(wikibase_id)
        # pylint: disable-next=bare-except
        except:
            logger.error(
                "UserDataError",
                exc_info=True,
                stack_info=True,
                extra={"wikibase": wikibase_id},
            )
        return False


async def update_bulk_user_observations(
    query: Select[tuple[WikibaseModel]],
) -> BulkTaskResult:
    """Update Bulk User Observations"""

    wikibases = await get_wikibase_list(query)
    logger.info(f"User: {len(wikibases)} Wikibases to Update")

    tasks = [asyncio.ensure_future(safe_update_user_obs(wiki.id)) for wiki in wikibases]
    await asyncio.gather(*tasks)

    return BulkTaskResult(tasks)
