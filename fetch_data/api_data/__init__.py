"""Data from api.php"""

from fetch_data.api_data.log_data import create_log_observation
from fetch_data.api_data.user_data import (
    create_user_observation,
    get_multiple_user_data,
    get_single_user_data,
    get_user_type_from_wikibase,
    get_user_type_from_user_data,
)
