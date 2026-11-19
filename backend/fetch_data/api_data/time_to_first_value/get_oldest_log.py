"""Oldest Log"""

from datetime import datetime

from fetch_data.api_data.constant import WIKIBASE_API_TIMESTAMP_FORMAT
from fetch_data.api_data.log_data.fetch_log_data import get_log_param_string
from fetch_data.utils import fetch_api_data
from model.database import WikibaseModel


async def get_oldest_log_date(wikibase: WikibaseModel) -> datetime:
    """Fetch Date of Oldest Log"""

    oldest_log = await fetch_api_data(
        wikibase.action_api_url()
        + get_log_param_string(limit=1, oldest=True, prop=["timestamp"])
    )
    return datetime.strptime(
        oldest_log["query"]["logevents"][0]["timestamp"], WIKIBASE_API_TIMESTAMP_FORMAT
    )
