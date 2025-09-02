"""Bulk Update Wikibases"""

from fetch_data.bulk.update_all import (
    update_all_connectivity_observations,
    update_all_log_observations,
    update_all_property_observations,
    update_all_quantity_observations,
    update_all_recent_changes_observations,
    update_all_software_observations,
    update_all_stats_observations,
    update_all_time_to_first_value_observations,
    update_all_user_observations,
)
from fetch_data.bulk.update_out_of_date import (
    update_out_of_date_cloud_instances,
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
)
