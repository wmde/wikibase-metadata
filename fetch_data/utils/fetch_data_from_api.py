"""Fetch API Data"""

import asyncio
import json
import requests

from logger import logger


class APIError(Exception):
    """API Returned Error"""


async def fetch_api_data(
    url: str, initial_wait: float = 8, max_retries: int = 5, multiplier: float = 2.0
) -> dict:
    """Fetch API Data with retry logic on request failures."""

    wait_time = initial_wait

    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:142.0) Gecko/20100101 Firefox/142.0"
    }

    for attempt in range(
        max_retries + 1
    ):  # pragma: no branch # we never run the full number of iterations
        try:
            logger.debug(f"Querying {url}")
            result = await asyncio.to_thread(
                requests.get, url, headers=headers, timeout=300
            )
            result.raise_for_status()
            query_data = json.loads(result.content)
            if "error" in query_data:
                raise APIError(f"API Returned Error: {query_data['error']}")
            max_retries = 0
            return query_data

        except requests.HTTPError as e:
            if e.response.status_code == 403:
                logger.error(f"403 Forbidden for {url}, giving up immediately")
                max_retries = 0
                raise APIError(f"Endpoint forbidden: {url}") from e
            elif e.response.status_code == 404:
                logger.error(f"404 Not Found for {url}, giving up immediately")
                max_retries = 0
                raise APIError(f"Endpoint not found: {url}") from e
            elif attempt >= max_retries:
                logger.error(f"All {max_retries + 1} retry attempts failed for {url}")
                raise APIError(f"Endpoint: {url}") from e

        except requests.RequestException as e:
            if attempt >= max_retries:
                logger.error(f"All {max_retries + 1} retry attempts failed for {url}")
                raise e

        finally:
            if attempt < max_retries:
                logger.warning(
                    f"Attempt {attempt + 1}/{max_retries + 1} failed: "
                    f"Retrying in {wait_time:.2f}s..."
                )
                await asyncio.sleep(wait_time)
                wait_time *= multiplier
