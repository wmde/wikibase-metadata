"""Update All Observations"""

from fetch_data.bulk.get_wikibase_query import (
    get_connectivity_obs_wikibases_query,
    get_log_obs_wikibases_query,
    get_property_popularity_obs_wikibases_query,
    get_quantity_obs_wikibases_query,
    get_recent_changes_obs_wikibases_query,
    get_software_obs_wikibases_query,
    get_stats_obs_wikibases_query,
    get_time_to_first_value_obs_wikibases_query,
    get_user_obs_wikibases_query,
)
from fetch_data.bulk.update_bulk import (
    update_bulk_connectivity_observations,
    update_bulk_log_observations,
    update_bulk_property_observations,
    update_bulk_quantity_observations,
    update_bulk_recent_changes_observations,
    update_bulk_software_observations,
    update_bulk_stats_observations,
    update_bulk_time_to_first_value_observations,
    update_bulk_user_observations,
)
from model.strawberry.output import BulkTaskResult


async def update_all_connectivity_observations() -> BulkTaskResult:
    """Update All Connectivity Observations"""

    query = get_connectivity_obs_wikibases_query()
    return await update_bulk_connectivity_observations(query)


async def update_all_log_observations(first_month: bool) -> BulkTaskResult:
    """Update All Log Observations"""

    query = get_log_obs_wikibases_query()
    return await update_bulk_log_observations(query, first_month=first_month)


async def update_all_property_observations() -> BulkTaskResult:
    """Update All Property Popularity Observations"""

    query = get_property_popularity_obs_wikibases_query()
    return await update_bulk_property_observations(query)


async def update_all_quantity_observations() -> BulkTaskResult:
    """Update All Quantity Observations"""

    query = get_quantity_obs_wikibases_query()
    return await update_bulk_quantity_observations(query)


async def update_all_recent_changes_observations() -> BulkTaskResult:
    """Update All Recent Changes Observations"""

    query = get_recent_changes_obs_wikibases_query()
    return await update_bulk_recent_changes_observations(query)


async def update_all_software_observations() -> BulkTaskResult:
    """Update All Software Version Observations"""

    query = get_software_obs_wikibases_query()
    return await update_bulk_software_observations(query)


async def update_all_stats_observations() -> BulkTaskResult:
    """Update All Special:Statistics Observations"""

    query = get_stats_obs_wikibases_query()
    return await update_bulk_stats_observations(query)


async def update_all_time_to_first_value_observations() -> BulkTaskResult:
    """Update All Time to First Value Observations"""

    query = get_time_to_first_value_obs_wikibases_query()
    return await update_bulk_time_to_first_value_observations(query)


async def update_all_user_observations() -> BulkTaskResult:
    """Update All User Observations"""

    query = get_user_obs_wikibases_query()
    return await update_bulk_user_observations(query)
