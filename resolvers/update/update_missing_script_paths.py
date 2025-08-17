"""Fix"""

import asyncio
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import requests
from requests.exceptions import SSLError
from sqlalchemy import Select, select

from data import get_async_session
from logger import logger
from model.database import WikibaseModel, WikibaseURLModel
from model.enum import WikibaseURLType
from resolvers.update.update_wikibase_url import upsert_wikibase_url


async def update_missing_script_paths():
    """Attempt to Fetch Missing scriptPaths"""

    query = missing_script_path_query()

    async with get_async_session() as async_session:
        wikis = (await async_session.scalars(query)).all()

        logger.info(f"Missing Script Path: {len(wikis)}")

        for wikibase in wikis:
            await fetch_wikibase_script_path(wikibase)
        return len(wikis)


def missing_script_path_query() -> Select[tuple[WikibaseModel]]:
    """Query for Wikibases with Article Paths but no Script Paths"""

    article_path_subquery = (
        select(WikibaseURLModel)
        .where(WikibaseURLModel.url_type == WikibaseURLType.ARTICLE_PATH)
        .subquery()
    )
    script_path_subquery = (
        select(WikibaseURLModel)
        .where(WikibaseURLModel.url_type == WikibaseURLType.SCRIPT_PATH)
        .subquery()
    )
    query = (
        select(WikibaseModel)
        .where(WikibaseModel.checked)
        .join(
            article_path_subquery,
            onclause=WikibaseModel.id == article_path_subquery.c.wikibase_id,
            isouter=False,
        )
        .join(
            script_path_subquery,
            onclause=WikibaseModel.id == script_path_subquery.c.wikibase_id,
            isouter=True,
        )
        # pylint: disable-next=singleton-comparison
        .where(script_path_subquery.c.id == None)
    )

    return query


async def fetch_wikibase_script_path(wikibase: WikibaseModel):
    """Attempt to Fetch scriptPath from Special:Version"""

    assert wikibase.action_api_url() is None
    assert wikibase.special_version_url() is not None

    try:
        result = await asyncio.to_thread(
            requests.get,
            wikibase.special_version_url(),
            headers={"Cookie": "mediawikilanguage=en"},
            timeout=10,
        )
        soup = BeautifulSoup(result.content, "html.parser")

        entrypoints_table = soup.find(
            "table", attrs={"id": "mw-version-entrypoints-table"}
        )
        assert entrypoints_table is not None, "Could Not Find Entry Points Table"

        for row in entrypoints_table.find_all("tr"):
            if row.find("td") is not None:
                left = row.find_all("td")[0]
                right = row.find_all("td")[1]
                if "$wgScriptPath" in left.find("a").attrs.get("href"):
                    assert await upsert_wikibase_url(
                        wikibase.id, right.text, WikibaseURLType.SCRIPT_PATH
                    )

    except (HTTPError, SSLError):
        logger.warning(
            "SoftwareVersionDataError",
            exc_info=True,
            stack_info=True,
            extra={"wikibase": wikibase.id},
        )
