"""Fetch All User Data"""

from fetch_data.api_data.user_data.user_data_url import all_users_url
from fetch_data.utils import fetch_api_data
from logger import logger


async def get_all_user_data(api_url: str) -> list[dict]:
    """Fetch All User Data"""

    data = []

    should_query = True
    next_from: str = "!"

    while should_query:
        query_data = await fetch_api_data(
            api_url + all_users_url(continue_from=next_from)
        )
        data.extend(query_data["query"]["allusers"])
        logger.debug(f"\tData Length: {len(data)}")
        if "continue" in query_data:
            next_from = query_data["continue"]["aufrom"]
        else:
            should_query = False

    return data
