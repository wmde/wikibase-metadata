"""Fetch User Data"""

from typing import Optional
from fetch_data.user_data.user_data_url import all_users_url
from fetch_data.utils.fetch_api_data import fetch_api_data


def fetch_all_user_data(api_url: str) -> list[dict]:
    """Fetch User Data"""

    data = []

    should_query = True
    next_from: str = "!"

    while should_query:
        query_data = fetch_api_data(api_url + all_users_url(continue_from=next_from))
        data.extend(query_data["query"]["allusers"])
        print(f"\tData Length: {len(data)}")
        if "continue" in query_data:
            next_from = query_data["continue"]["aufrom"]
        else:
            should_query = False

    return data
