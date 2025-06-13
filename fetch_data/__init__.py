"""Fetch Data"""

from fetch_data.api_data import create_log_observation, create_user_observation
from fetch_data.out_of_date import (
    get_wikibase_list_with_out_of_date_connectivity_observations,
    get_wikibase_list_with_out_of_date_log_first_observations,
    get_wikibase_list_with_out_of_date_log_last_observations,
    get_wikibase_list_with_out_of_date_property_popularity_observations,
    get_wikibase_list_with_out_of_date_quantity_observations,
    get_wikibase_list_with_out_of_date_software_observations,
    get_wikibase_list_with_out_of_date_stats_observations,
    get_wikibase_list_with_out_of_date_user_observations,
    update_out_of_date_connectivity_observations,
    update_out_of_date_log_first_observations,
    update_out_of_date_log_last_observations,
    update_out_of_date_property_observations,
    update_out_of_date_quantity_observations,
    update_out_of_date_software_observations,
    update_out_of_date_stats_observations,
    update_out_of_date_user_observations,
    update_out_of_date_cloud_instances,
)
from fetch_data.sparql_data import (
    create_connectivity_observation,
    create_property_popularity_observation,
    create_quantity_observation,
)
from fetch_data.soup_data import (
    create_software_version_observation,
    create_special_statistics_observation,
    update_software_data,
)
