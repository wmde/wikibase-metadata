"""Fetch API Data"""

import asyncio
import json
import requests

from logger import logger


class APIError(Exception):
    """API Returned Error"""


async def fetch_api_data(url: str) -> dict:
    """Fetch API Data"""

    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:142.0) Gecko/20100101 Firefox/142.0"
    }

    logger.debug(f"Querying {url}")
    result = await asyncio.to_thread(requests.get, url, headers=headers, timeout=300)
    result.raise_for_status()
    query_data = json.loads(result.content)
    if "error" in query_data:
        raise APIError(f"API Returned Error: {query_data['error']}")
    return query_data
