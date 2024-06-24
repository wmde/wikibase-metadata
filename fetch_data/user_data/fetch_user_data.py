"""Fetch User Data"""

import json
import requests
from fetch_data.user_data.user_data_url import users_url


def fetch_user_data(api_url: str) -> list[dict]:
    """Fetch User Data"""

    data = []

    should_query = True
    next_from = None

    while should_query:
        url = users_url(api_url, continue_from=next_from)
        print(f"Querying {url}")
        result = requests.get(url, timeout=10)
        query_data = json.loads(result.content)
        if "error" in query_data:
            raise ValueError(f"API Returned Error: {query_data['error']}")
        data.extend(query_data["query"]["allusers"])
        print(f"\tData Length: {len(data)}")
        if "continue" in query_data:
            next_from = query_data["continue"]["aufrom"]
        else:
            should_query = False

    return data
