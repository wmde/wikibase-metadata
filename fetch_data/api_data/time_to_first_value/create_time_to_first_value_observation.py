"""Create Time to First Value Observation"""

import asyncio
from datetime import datetime
from json.decoder import JSONDecodeError
from bs4 import BeautifulSoup
import requests
from requests.exceptions import ReadTimeout, SSLError
from data import get_async_session
from fetch_data.utils import dict_to_url, get_wikibase_from_database
from logger import logger
from model.database import (
    WikibaseTimeToFirstValueObservationModel,
    WikibaseItemDateModel,
    WikibaseModel,
)


async def create_time_to_first_value_observation(wikibase_id: int) -> bool:
    """Create Time to First Value Observation"""

    async with get_async_session() as async_session:
        wikibase: WikibaseModel = await get_wikibase_from_database(
            async_session=async_session,
            wikibase_id=wikibase_id,
            include_observations=True,
            require_index_api=True,
        )

        observation = WikibaseTimeToFirstValueObservationModel(wikibase_id=wikibase.id)

        try:
            logger.info("Fetching Creation Date", extra={"wikibase": wikibase.id})

            observation.initiation_date = await get_creation_date(
                wikibase, "Project:Home"
            )

            for exponent in range(0, 7):
                returned = False
                for nudge in range(0, 5):
                    i = (10 ^ exponent) + nudge
                    if not returned:
                        try:
                            c = await get_creation_date(wikibase, f"Item:Q{i}")
                            observation.item_date_models.append(
                                WikibaseItemDateModel(item_number=i, creation_date=c)
                            )
                            returned = True
                        except:
                            pass

            observation.returned_data = True
        except (ConnectionError, JSONDecodeError, ReadTimeout, SSLError):
            logger.warning(
                "TimeToFirstValueDataError",
                exc_info=True,
                stack_info=True,
                extra={"wikibase": wikibase.id},
            )
            observation.returned_data = False

        wikibase.time_to_first_value_observations.append(observation)

        await async_session.commit()
        return observation.returned_data


async def get_creation_date(wikibase: WikibaseModel, title: str) -> datetime:
    result = await asyncio.to_thread(
        requests.get,
        wikibase.index_api_url.url
        + dict_to_url({"title": title, "action": "history", "dir": "prev"}),
    )
    result.raise_for_status()
    soup = BeautifulSoup(result.content, "html.parser")
    history = soup.find("ul", attrs={"id": "pagehistory"})
    date_links = history.find_all("a", attrs={"class": "mw-changeslist-date"})
    dates = [
        datetime.strptime(a.string, "%H:%M, %d %b %Y") for a in date_links if a.string
    ]
    return min(dates)
