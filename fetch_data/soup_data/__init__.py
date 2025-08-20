"""Data from Parsing Webpages with Beautiful Soup"""

from fetch_data.soup_data.create_statistics_data_observation import (
    create_special_statistics_observation,
)
from fetch_data.soup_data.software import (
    create_software_version_observation,
    get_update_extension_query,
    update_software_data,
)
from fetch_data.soup_data.time_to_first_value import (
    create_time_to_first_value_observation,
)
