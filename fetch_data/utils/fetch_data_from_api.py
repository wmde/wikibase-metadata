"""Fetch API Data"""

import asyncio
import json
import requests

from logger import logger


class APIError(Exception):
    """API Returned Error"""


async def fetch_api_data(url: str) -> dict:
    """Fetch API Data"""

    logger.debug(f"Querying {url}")
    result = await asyncio.to_thread(requests.get, url, timeout=300)
    result.raise_for_status()
    query_data = json.loads(result.content)
    if "error" in query_data:
        raise APIError(f"API Returned Error: {query_data['error']}")
    return query_data
