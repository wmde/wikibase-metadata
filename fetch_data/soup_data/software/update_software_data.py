"""Update Software Data"""

from datetime import datetime, timedelta, timezone
import os
import re
from typing import Iterable, List, Optional
from bs4 import BeautifulSoup
import requests
from sqlalchemy import Select, and_, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from data import get_async_session
from model.database import WikibaseSoftwareModel
from model.database.wikibase_software.software_tag_model import WikibaseSoftwareTagModel
from model.enum import WikibaseSoftwareType


async def update_software_data():
    """Fetch Software Info"""

    async with get_async_session() as async_session:
        os.makedirs("dump", exist_ok=True)

        unfound_extensions: Iterable[WikibaseSoftwareModel] = (
            await async_session.scalars(get_update_extension_query())
        ).all()
        for ext in unfound_extensions:
            if ext.url is None:
                ext.url = (
                    f"https://www.mediawiki.org/wiki/Extension:{ext.software_name}"
                )
            with requests.get(ext.url, timeout=10, allow_redirects=True) as response:
                ext.data_fetched = datetime.now(timezone.utc)
                if response.status_code == 200:
                    if response.url != ext.url:
                        ext.url = response.url

                    soup = BeautifulSoup(response.content, features="html.parser")

                    ext.tags = await compile_tag_list(async_session, soup)
                    ext.description = compile_description(soup)
                    ext.latest_version = compile_latest_version(soup)
                    ext.quarterly_download_count = compile_quarterly_count(soup)
                    ext.public_wiki_count = compile_wiki_count(soup)
                    ext.mediawiki_bundled = compile_bundled(soup)

                    await async_session.flush()
        await async_session.commit()


def get_update_extension_query() -> Select[WikibaseSoftwareModel]:
    """Update Extension List Query"""

    return (
        select(WikibaseSoftwareModel)
        .where(
            and_(
                or_(
                    # pylint: disable=singleton-comparison
                    WikibaseSoftwareModel.data_fetched == None,
                    WikibaseSoftwareModel.data_fetched
                    < (datetime.today() - timedelta(days=30)),
                ),
                WikibaseSoftwareModel.software_type == WikibaseSoftwareType.EXTENSION,
            )
        )
        .limit(5)
    )


async def compile_tag_list(
    async_session: AsyncSession, soup: BeautifulSoup
) -> List[WikibaseSoftwareTagModel]:
    """Compile Tag List"""

    type_title_tag = soup.find(
        "a", attrs={"href": "/wiki/Special:MyLanguage/Template:Extension#type"}
    )
    type_tag = type_title_tag.find_parent("td").find_next_sibling("td")
    assert type_tag is not None

    tag_list: list[str] = []
    if len(list(type_tag.children)) == 1:
        tag_list = list(type_tag.stripped_strings)
    else:
        tag_list = [
            stripped
            for t in type_tag.find_all("a")
            if (stripped := (t.string).strip()) != ""
        ]
    all_tags = await fetch_or_create_tags(async_session, tag_list)

    return all_tags


async def fetch_or_create_tags(
    async_session: AsyncSession, tag_list: List[str]
) -> List[WikibaseSoftwareTagModel]:
    """Fetch or Create Tags"""

    existing_tags = (
        await async_session.scalars(
            select(WikibaseSoftwareTagModel).where(
                WikibaseSoftwareTagModel.tag.in_(tag_list)
            )
        )
    ).all()
    existing_tag_strs = {t.tag for t in existing_tags}
    all_tags = [*existing_tags]
    for tag in tag_list:
        if tag not in existing_tag_strs:
            all_tags.append(WikibaseSoftwareTagModel(tag))
    return all_tags


def compile_description(soup: BeautifulSoup) -> str:
    """Compile Description"""

    description_title_tag = soup.find(
        "a", attrs={"href": "/wiki/Special:MyLanguage/Template:Extension#description"}
    )
    description_tag = description_title_tag.find_parent("td").find_next_sibling("td")
    assert description_tag is not None
    return "".join(description_tag.strings)


def compile_latest_version(soup: BeautifulSoup) -> Optional[str]:
    """Compile Latest Version"""

    version_title_tag = soup.find(
        "a", attrs={"href": "/wiki/Special:MyLanguage/Template:Extension#version"}
    )
    if version_title_tag is None:
        return None

    version_tag = version_title_tag.find_parent("td").find_next_sibling("td")
    assert version_tag is not None, f"{version_title_tag.prettify()}"
    return version_tag.string.strip()


def compile_quarterly_count(soup: BeautifulSoup) -> Optional[int]:
    """Compile Quarterly Download Count"""

    qd_title_tag = soup.find("b", string="Quarterly downloads")
    if qd_title_tag is None:
        return None

    qd_tag = qd_title_tag.find_parent("td").find_next_sibling("td")
    assert qd_tag is not None
    attempt = re.sub(r"^(\d+(,\d+)*) .*$", r"\1", "".join(qd_tag.strings))
    return int(attempt.replace(",", ""))


def compile_wiki_count(soup: BeautifulSoup) -> Optional[int]:
    """Compile Public Wiki Count"""

    pw_title_tag = soup.find("b", string="Public wikis using")
    if pw_title_tag is None:
        return None

    pw_tag = pw_title_tag.find_parent("td").find_next_sibling("td")
    assert pw_tag is not None
    attempt = re.sub(r"^(\d+(,\d+)*) .*$", r"\1", "".join(pw_tag.strings))
    return int(attempt.replace(",", ""))


def compile_bundled(soup: BeautifulSoup) -> Optional[bool]:
    """Compile Bundled with MediaWiki"""

    category_list_tag = soup.find("div", attrs={"id": "mw-normal-catlinks"})
    if category_list_tag is None:
        return None
    for a_tag in category_list_tag.find_all("a"):
        if re.match(
            r"^/wiki/Category:Extensions_bundled_with_MediaWiki_\d+\.\d+$",
            a_tag["href"],
        ):
            return True
    return False
