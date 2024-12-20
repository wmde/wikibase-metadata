"""Fetch API Data"""

import asyncio
import json
import requests

from logger import logger


async def fetch_api_data(url: str) -> dict:
    """Fetch API Data"""

    logger.debug(f"Querying {url}")
    result = await asyncio.to_thread(requests.get, url, timeout=10)
    query_data = json.loads(result.content)
    if "error" in query_data:
        raise ValueError(f"API Returned Error: {query_data['error']}")
    return query_data
