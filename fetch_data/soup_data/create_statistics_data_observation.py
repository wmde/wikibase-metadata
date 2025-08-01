"""Create Special:Statistics Observation"""

import asyncio
from typing import Optional
from urllib.error import HTTPError

from bs4 import BeautifulSoup
import requests
from requests.exceptions import SSLError

from data import get_async_session
from fetch_data.utils import get_wikibase_from_database
from logger import logger
from model.database import WikibaseModel, WikibaseStatisticsObservationModel


async def create_special_statistics_observation(wikibase_id: int) -> bool:
    """Create Special:Statistics Observation"""

    logger.debug("Statistics: Attempting Observation", extra={"wikibase": wikibase_id})

    async with get_async_session() as async_session:
        wikibase: WikibaseModel = await get_wikibase_from_database(
            async_session=async_session,
            wikibase_id=wikibase_id,
            join_statistics_observations=True,
            require_article_path=True,
        )

        observation = WikibaseStatisticsObservationModel()

        try:
            result = await asyncio.to_thread(
                requests.get,
                wikibase.special_statistics_url(),
                headers={"Cookie": "mediawikilanguage=en"},
                timeout=10,
            )
            soup = BeautifulSoup(result.content, "html.parser")
            table = soup.find("table", attrs={"class": "mw-statistics-table"})

            observation.returned_data = True

            observation.content_pages = get_number_from_row(
                table, "mw-statistics-articles"
            )
            observation.total_pages = get_number_from_row(
                table, row_class="mw-statistics-pages"
            )
            observation.total_files = get_number_from_row(
                table, row_class="mw-statistics-files", optional=True
            )
            observation.total_edits = get_number_from_row(
                table, row_class="mw-statistics-edits"
            )
            observation.total_users = get_number_from_row(
                table, row_class="mw-statistics-users"
            )
            observation.active_users = get_number_from_row(
                table, row_class="mw-statistics-users-active"
            )
            observation.total_admin = get_number_from_row(
                table, row_class="statistics-group-sysop"
            )
            observation.content_page_word_count_total = get_number_from_row(
                table, row_id="mw-cirrussearch-article-words", optional=True
            )

        except (ConnectionError, HTTPError, SSLError):
            logger.warning(
                "StatisticsDataError",
                exc_info=True,
                stack_info=True,
                extra={"wikibase": wikibase.id},
            )
            observation.returned_data = False

        wikibase.statistics_observations.append(observation)

        await async_session.commit()
        return observation.returned_data


def get_number_from_row(
    soup: BeautifulSoup,
    row_class: Optional[str] = None,
    row_id: Optional[str] = None,
    optional: bool = False,
) -> int | None:
    """Get Statistic Number From Row"""

    assert (row_class or row_id) is not None, "No Identifiers Given"

    statistic_row = (
        soup.find("tr", attrs={"class": row_class})
        if row_class is not None
        else soup.find("tr", attrs={"id": row_id})
    )

    if statistic_row is None:
        assert optional, f"Could Not Find Row: {row_class}, {soup.prettify()}"
        return None

    return int(
        statistic_row.find("td", attrs={"class": "mw-statistics-numbers"})
        .string.replace(",", "")
        .replace(".", "")
        .replace("\xa0", "")
    )
