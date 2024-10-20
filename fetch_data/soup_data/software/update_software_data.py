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

    carry_on = True
    while carry_on:

        async with get_async_session() as async_session:
            os.makedirs("dump", exist_ok=True)

            unfound_extensions: Iterable[WikibaseSoftwareModel] = (
                await async_session.scalars(get_update_extension_query())
            ).all()
            carry_on = len(unfound_extensions) > 0

            for ext in unfound_extensions:
                if ext.url is None:
                    ext.url = (
                        f"https://www.mediawiki.org/wiki/Extension:{ext.software_name}"
                    )

                await compile_data_from_url(async_session, ext)
                await async_session.flush()
            await async_session.commit()


async def compile_data_from_url(
    async_session: AsyncSession,
    ext: WikibaseSoftwareModel,
    override_url: Optional[str] = None,
    archived: bool = False,
):
    """Compile Software Data from URL"""

    with requests.get(
        override_url or ext.url, timeout=10, allow_redirects=True
    ) as response:

        ext.data_fetched = datetime.now(timezone.utc)
        print(f"{response.url}: {response.status_code}")

        if response.status_code == 200:

            if override_url is None and response.url != ext.url:
                ext.url = response.url

            soup = BeautifulSoup(response.content, features="html.parser")

            page_archived = (
                soup.find("b", string="This extension has been archived.") is not None
            )
            ext.archived = archived or page_archived
            if page_archived:
                permanent_link_tag = soup.find(
                    "a",
                    string="To see the page before archival, click here.",
                )
                return await compile_data_from_url(
                    async_session,
                    ext,
                    override_url=f"https://www.mediawiki.org{permanent_link_tag['href']}",
                    archived=True,
                )

            ext.tags = await compile_tag_list(async_session, soup)
            ext.description = compile_description(soup)
            ext.latest_version = compile_latest_version(soup)
            ext.quarterly_download_count = compile_quarterly_count(soup)
            ext.public_wiki_count = compile_wiki_count(soup)
            ext.mediawiki_bundled = compile_bundled(soup)


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
                or_(
                    # pylint: disable=singleton-comparison
                    WikibaseSoftwareModel.archived == False,
                    WikibaseSoftwareModel.archived == None,
                ),
            )
        )
        .limit(1)
    )


async def compile_tag_list(
    async_session: AsyncSession, soup: BeautifulSoup
) -> List[WikibaseSoftwareTagModel]:
    """Compile Tag List"""

    type_title_tag = soup.find(
        "a", attrs={"href": "/wiki/Special:MyLanguage/Template:Extension#type"}
    )
    if type_title_tag is None:
        return []

    type_tag = type_title_tag.find_parent("td").find_next_sibling("td")
    assert type_tag is not None

    tag_list: list[str] = []
    if len(list(type_tag.children)) == 1:
        tag_list = [
            s.strip()
            for t_string in type_tag.stripped_strings
            for s in t_string.split(",")
        ]
    else:
        tag_list = [
            stripped
            for t in type_tag.find_all("a")
            if t.string is not None
            for s in t.string.split(",")
            if (stripped := (s).strip()) != ""
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


def compile_description(soup: BeautifulSoup) -> Optional[str]:
    """Compile Description"""

    description_title_tag = soup.find(
        "a", attrs={"href": "/wiki/Special:MyLanguage/Template:Extension#description"}
    )
    if description_title_tag is None:
        return None

    description_tag = description_title_tag.find_parent("td").find_next_sibling("td")
    assert description_tag is not None
    return "".join(description_tag.strings).strip()


def compile_latest_version(soup: BeautifulSoup) -> Optional[str]:
    """Compile Latest Version"""

    version_title_tag = soup.find(
        "a", attrs={"href": "/wiki/Special:MyLanguage/Template:Extension#version"}
    )
    if version_title_tag is None:
        return None

    version_tag = version_title_tag.find_parent("td").find_next_sibling("td")
    assert version_tag is not None, f"{version_title_tag.prettify()}"
    return "".join(version_tag.strings).strip()


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
