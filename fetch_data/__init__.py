"""Fetch Data"""

from fetch_data.log_data import create_log_observation
from fetch_data.sparql_data import (
    create_connectivity_observation,
    create_property_popularity_observation,
    create_quantity_observation,
)
from fetch_data.user_data import create_user_data_observation
from fetch_data.version_data import create_software_version_observation
