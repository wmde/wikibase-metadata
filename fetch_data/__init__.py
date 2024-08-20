"""Fetch Data"""

from fetch_data.api_data import create_log_observation, create_user_observation
from fetch_data.sparql_data import (
    create_connectivity_observation,
    create_property_popularity_observation,
    create_quantity_observation,
)
from fetch_data.soup_data import create_software_version_observation
