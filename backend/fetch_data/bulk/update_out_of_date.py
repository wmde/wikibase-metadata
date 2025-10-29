"""Update Out of Date Observations"""

from fetch_data.bulk.bulk_task_result import BulkTaskResult
from fetch_data.bulk.get_out_of_date_wikibase_query import (
    get_wikibase_with_out_of_date_connectivity_obs_query,
    get_wikibase_with_out_of_date_external_identifier_obs_query,
    get_wikibase_with_out_of_date_log_first_obs_query,
    get_wikibase_with_out_of_date_log_last_obs_query,
    get_wikibase_with_out_of_date_property_popularity_obs_query,
    get_wikibase_with_out_of_date_quantity_obs_query,
    get_wikibase_with_out_of_date_recent_changes_obs_query,
    get_wikibase_with_out_of_date_software_obs_query,
    get_wikibase_with_out_of_date_stats_obs_query,
    get_wikibase_with_out_of_date_time_to_first_value_obs_query,
    get_wikibase_with_out_of_date_user_obs_query,
)
from fetch_data.bulk.update_bulk import (
    update_bulk_connectivity_observations,
    update_bulk_external_identifier_observations,
    update_bulk_log_observations,
    update_bulk_property_observations,
    update_bulk_quantity_observations,
    update_bulk_recent_changes_observations,
    update_bulk_software_observations,
    update_bulk_stats_observations,
    update_bulk_time_to_first_value_observations,
    update_bulk_user_observations,
)
from fetch_data.cloud_api_data import update_cloud_instances
from logger import logger


async def update_out_of_date_connectivity_observations() -> BulkTaskResult:
    """Update Out of Date Connectivity Observations"""

    query = get_wikibase_with_out_of_date_connectivity_obs_query()
    return await update_bulk_connectivity_observations(query)


async def update_out_of_date_external_identifier_observations() -> BulkTaskResult:
    """Update Out of Date External Identifier Observations"""

    query = get_wikibase_with_out_of_date_external_identifier_obs_query()
    return await update_bulk_external_identifier_observations(query)


async def update_out_of_date_log_first_observations() -> BulkTaskResult:
    """Update Out of Date Log (First Month) Observations"""

    query = get_wikibase_with_out_of_date_log_first_obs_query()
    return await update_bulk_log_observations(query, first_month=True)


async def update_out_of_date_log_last_observations() -> BulkTaskResult:
    """Update Out of Date Log (Last Month) Observations"""

    query = get_wikibase_with_out_of_date_log_last_obs_query()
    return await update_bulk_log_observations(query, first_month=False)


async def update_out_of_date_property_observations() -> BulkTaskResult:
    """Update Out of Date Property Popularity Observations"""

    query = get_wikibase_with_out_of_date_property_popularity_obs_query()
    return await update_bulk_property_observations(query)


async def update_out_of_date_quantity_observations() -> BulkTaskResult:
    """Update Out of Date Quantity Observations"""

    query = get_wikibase_with_out_of_date_quantity_obs_query()
    return await update_bulk_quantity_observations(query)


async def update_out_of_date_recent_changes_observations() -> BulkTaskResult:
    """Update Out of Date Recent Changes Observations"""

    query = get_wikibase_with_out_of_date_recent_changes_obs_query()
    return await update_bulk_recent_changes_observations(query)


async def update_out_of_date_software_observations() -> BulkTaskResult:
    """Update Out of Date Software Version Observations"""

    query = get_wikibase_with_out_of_date_software_obs_query()
    return await update_bulk_software_observations(query)


async def update_out_of_date_stats_observations() -> BulkTaskResult:
    """Update Out of Date Special:Statistics Observations"""

    query = get_wikibase_with_out_of_date_stats_obs_query()
    return await update_bulk_stats_observations(query)


async def update_out_of_date_time_to_first_value_observations() -> BulkTaskResult:
    """Update Out of Date Time to First Value Observations"""

    query = get_wikibase_with_out_of_date_time_to_first_value_obs_query()
    return await update_bulk_time_to_first_value_observations(query)


async def update_out_of_date_user_observations() -> BulkTaskResult:
    """Update Out of Date User Observations"""

    query = get_wikibase_with_out_of_date_user_obs_query()
    return await update_bulk_user_observations(query)


async def update_out_of_date_cloud_instances():
    """Pull cloud instaces and update our local database"""

    logger.info("Pulling cloud instances and updating local database")
    try:
        await update_cloud_instances()
    # pylint: disable-next=bare-except
    except:
        logger.error(
            "CloudInstancesError",
            exc_info=True,
            stack_info=True,
        )
