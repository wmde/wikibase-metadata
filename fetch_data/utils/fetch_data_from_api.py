"""Fetch API Data"""

import json
import requests


def fetch_api_data(url: str) -> dict:
    """Fetch API Data"""

    print(f"Querying {url}")
    result = requests.get(url, timeout=10)
    query_data = json.loads(result.content)
    if "error" in query_data:
        raise ValueError(f"API Returned Error: {query_data['error']}")
    return query_data
