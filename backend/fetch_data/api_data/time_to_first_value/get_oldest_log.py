"""Oldest Log"""

from datetime import datetime

from fetch_data.api_data.constant import WIKIBASE_API_TIMESTAMP_FORMAT
from fetch_data.api_data.log_data.fetch_log_data import get_log_param_string
from fetch_data.utils import fetch_api_data


async def get_oldest_log_date(api_url: str) -> datetime:
    """Fetch Date of Oldest Log"""

    oldest_log = await fetch_api_data(
        api_url + get_log_param_string(limit=1, oldest=True, prop=["timestamp"])
    )
    return datetime.strptime(
        oldest_log["query"]["logevents"][0]["timestamp"], WIKIBASE_API_TIMESTAMP_FORMAT
    )
