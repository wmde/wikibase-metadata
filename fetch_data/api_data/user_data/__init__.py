"""Fetch User Data"""

from fetch_data.api_data.user_data.create_user_data_observation import (
    create_user_observation,
)
from fetch_data.api_data.user_data.fetch_multiple_user_data import (
    get_multiple_user_data,
)
from fetch_data.api_data.user_data.fetch_single_user_data import get_single_user_data
from fetch_data.api_data.user_data.fetch_user_type import (
    get_user_type_from_wikibase,
    get_user_type_from_user_data,
)
