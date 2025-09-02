"""Fetch Data"""

from fetch_data.api_data import (
    create_log_observation,
    create_recent_changes_observation,
    create_time_to_first_value_observation,
    create_user_observation,
)
from fetch_data.bulk import (
    update_out_of_date_connectivity_observations,
    update_out_of_date_log_first_observations,
    update_out_of_date_log_last_observations,
    update_out_of_date_property_observations,
    update_out_of_date_quantity_observations,
    update_out_of_date_recent_changes_observations,
    update_out_of_date_software_observations,
    update_out_of_date_stats_observations,
    update_out_of_date_time_to_first_value_observations,
    update_out_of_date_user_observations,
    update_out_of_date_cloud_instances,
)
from fetch_data.cloud_api_data import fetch_cloud_instances, update_cloud_instances
from fetch_data.sparql_data import (
    create_connectivity_observation,
    create_property_popularity_observation,
    create_quantity_observation,
)
from fetch_data.soup_data import (
    create_software_version_observation,
    create_special_statistics_observation,
    get_update_extension_query,
    update_software_data,
)
