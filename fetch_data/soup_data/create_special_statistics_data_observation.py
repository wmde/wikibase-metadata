"""Create Special:Statistics Observation"""

from urllib.error import HTTPError
from bs4 import BeautifulSoup
import requests
from requests.exceptions import SSLError
from data import get_async_session
from fetch_data.utils import get_wikibase_from_database
from model.database import WikibaseModel, WikibaseStatisticsObservationModel


async def create_special_statistics_observation(wikibase_id: int) -> bool:
    """Create Special:Statistics Observation"""

    async with get_async_session() as async_session:
        wikibase: WikibaseModel = await get_wikibase_from_database(
            async_session=async_session,
            wikibase_id=wikibase_id,
            require_special_statistics=True,
        )

        observation = WikibaseStatisticsObservationModel()

        try:
            result = requests.get(
                wikibase.special_statistics_url.url,
                # headers={"Cookie": "mediawikilanguage=en"},
                timeout=10,
            )
            soup = BeautifulSoup(result.content, "html.parser")

            observation.returned_data = True

            observation.content_pages = int(
                soup.find("tr", attrs={"class": "mw-statistics-articles"})
                .find("td", attrs={"class": "mw-statistics-numbers"})
                .string.replace(",", "")
            )
            observation.total_pages = int(
                soup.find("tr", attrs={"class": "mw-statistics-pages"})
                .find("td", attrs={"class": "mw-statistics-numbers"})
                .string.replace(",", "")
            )
            observation.total_files = int(
                soup.find("tr", attrs={"class": "mw-statistics-files"})
                .find("td", attrs={"class": "mw-statistics-numbers"})
                .string.replace(",", "")
            )
            observation.total_edits = int(
                soup.find("tr", attrs={"class": "mw-statistics-edits"})
                .find("td", attrs={"class": "mw-statistics-numbers"})
                .string.replace(",", "")
            )
            observation.total_users = int(
                soup.find("tr", attrs={"class": "mw-statistics-users"})
                .find("td", attrs={"class": "mw-statistics-numbers"})
                .string.replace(",", "")
            )
            observation.active_users = int(
                soup.find("tr", attrs={"class": "mw-statistics-users-active"})
                .find("td", attrs={"class": "mw-statistics-numbers"})
                .string.replace(",", "")
            )
            observation.total_admin = int(
                soup.find("tr", attrs={"class": "statistics-group-sysop"})
                .find("td", attrs={"class": "mw-statistics-numbers"})
                .string.replace(",", "")
            )
            observation.words_in_content_pages = int(
                soup.find("tr", attrs={"id": "mw-cirrussearch-article-words"})
                .find("td", attrs={"class": "mw-statistics-numbers"})
                .string.replace(",", "")
            )

        except (HTTPError, SSLError):
            observation.returned_data = False

        wikibase.statistics_observations.append(observation)

        await async_session.commit()
        return observation.returned_data
