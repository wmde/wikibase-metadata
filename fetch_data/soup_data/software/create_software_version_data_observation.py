"""Create Software Version Observation"""

from collections.abc import Iterable
from datetime import datetime
from urllib.error import HTTPError
from bs4 import BeautifulSoup, Tag
import requests
from requests.exceptions import SSLError
from sqlalchemy.ext.asyncio import AsyncSession
import strawberry
from data import get_async_session
from fetch_data.soup_data.software.get_software_model import (
    get_or_create_software_model,
)
from fetch_data.soup_data.software.get_update_software_data import update_software_data
from fetch_data.utils import get_wikibase_from_database, parse_datetime
from model.database import (
    WikibaseModel,
    WikibaseSoftwareVersionModel,
    WikibaseSoftwareVersionObservationModel,
)
from model.enum import WikibaseSoftwareType


async def create_software_version_observation(
    wikibase_id: int, info: strawberry.Info
) -> bool:
    """Create Software Version Observation"""

    info.context["background_tasks"].add_task(update_software_data)

    async with get_async_session() as async_session:
        wikibase: WikibaseModel = await get_wikibase_from_database(
            async_session=async_session,
            wikibase_id=wikibase_id,
            include_observations=True,
            require_special_version=True,
        )

        observation = WikibaseSoftwareVersionObservationModel()

        try:
            result = requests.get(
                wikibase.special_version_url.url,
                headers={"Cookie": "mediawikilanguage=en"},
                timeout=10,
            )
            soup = BeautifulSoup(result.content, "html.parser")

            observation.returned_data = True

            # Refers only to the "Installed Software" list in the Special:Version page
            # Does not include skins, extensions, or libraries, which are compiled below
            installed_software_versions = await compile_installed_software_versions(
                async_session, soup
            )
            observation.software_versions.extend(installed_software_versions)

            skin_versions = await compile_skin_versions(async_session, soup)
            observation.software_versions.extend(skin_versions)

            extensions_versions = await compile_extension_versions(async_session, soup)
            observation.software_versions.extend(extensions_versions)

            library_versions = await compile_library_versions(async_session, soup)
            observation.software_versions.extend(library_versions)
        except (HTTPError, SSLError):
            observation.returned_data = False

        wikibase.software_version_observations.append(observation)

        await async_session.commit()
        return observation.returned_data


async def compile_extension_versions(
    async_session: AsyncSession, soup: BeautifulSoup
) -> list[WikibaseSoftwareVersionModel]:
    """Compile Extension Version List"""

    extensions_table = soup.find(
        "table", attrs={"id": ["sv-ext", "sv-credits-specialpage"]}
    )
    return unique_versions(
        [
            await get_software_version_from_row(
                async_session, row, WikibaseSoftwareType.EXTENSION
            )
            for row in extensions_table.find_all(
                "tr", attrs={"class": "mw-version-ext"}
            )
        ]
    )


async def compile_installed_software_versions(
    async_session: AsyncSession, soup: BeautifulSoup
) -> list[WikibaseSoftwareVersionModel]:
    """Compile Installed Software Version List"""

    installed_software_table: Tag = soup.find("table", attrs={"id": "sv-software"})

    software_versions: list[WikibaseSoftwareVersionModel] = []
    row: Tag
    for row in installed_software_table.find_all("tr"):
        if row.find("td"):
            software_name = row.find_all("td")[0].string
            version: str
            version_hash: str | None = None
            version_date: datetime | None = None
            if row.find_all("td")[1].string is not None:
                version = row.find_all("td")[1].string
            elif (
                len(
                    version_strings := [
                        s for s in row.find_all("td")[1].strings if len(s.strip()) > 0
                    ]
                )
                == 3
            ):
                version = version_strings[0].strip()
                version_hash = version_strings[1].strip()
                version_date = parse_datetime(version_strings[2].strip())
            elif len(version_strings) == 2:
                version = version_strings[0].strip()
                version_hash = version_strings[1].strip()
            else:
                raise NotImplementedError(f"{version_strings}")

            software_versions.append(
                WikibaseSoftwareVersionModel(
                    software=await get_or_create_software_model(
                        async_session, WikibaseSoftwareType.SOFTWARE, software_name
                    ),
                    version=version,
                    version_hash=version_hash,
                    version_date=version_date,
                )
            )

    return software_versions


async def compile_library_versions(
    async_session: AsyncSession, soup: BeautifulSoup
) -> list[WikibaseSoftwareVersionModel]:
    """Compile Library Version List"""

    libraries_table = soup.find("table", attrs={"id": "sv-libraries"})

    library_versions: list[WikibaseSoftwareVersionModel] = []
    row: Tag
    for row in libraries_table.find_all("tr"):
        if row.find("td"):
            software_name = row.find(
                "a", attrs={"class": "mw-version-library-name"}
            ).string
            if software_name is not None:
                version = row.find_all("td")[1].string
                library_versions.append(
                    WikibaseSoftwareVersionModel(
                        software=await get_or_create_software_model(
                            async_session, WikibaseSoftwareType.LIBRARY, software_name
                        ),
                        version=version,
                    )
                )

    return unique_versions(library_versions)


async def compile_skin_versions(
    async_session: AsyncSession, soup: BeautifulSoup
) -> list[WikibaseSoftwareVersionModel]:
    """Compile Skin Version List"""

    installed_skin_table: Tag = soup.find(
        "table", attrs={"id": ["sv-skin", "sv-credits-skin"]}
    )
    return unique_versions(
        [
            await get_software_version_from_row(
                async_session, row, WikibaseSoftwareType.SKIN
            )
            for row in installed_skin_table.find_all(
                "tr", attrs={"class": "mw-version-ext"}
            )
        ]
    )


async def get_software_version_from_row(
    async_session: AsyncSession, row: Tag, software_type: WikibaseSoftwareType
) -> WikibaseSoftwareVersionModel:
    """Parse Software Version from Table Row"""

    software_name = (
        row.find("a", attrs={"class": "mw-version-ext-name"}) or row.find_all("td")[0]
    ).string
    assert software_name is not None, f"Could Not Find Software Name: {row.prettify()}"

    version: str | None = None
    if (
        version_tag := row.find("span", attrs={"class": "mw-version-ext-version"})
    ).string is not None:
        version = version_tag.string
    elif (
        version_tag.find("a", attrs={"href": "https://www.mediawiki.org/wiki/MLEB"})
        is not None
    ):
        version = [s.strip() for s in version_tag.strings][0]
    else:
        raise NotImplementedError()

    assert version is not None, f"Could Not Find Version: {row.prettify()}"

    version_hash: str | None = None
    if (
        hash_tag := row.find(
            ["a", "span"], attrs={"class": "mw-version-ext-vcs-version"}
        )
    ) is not None:
        version_hash = hash_tag.string

    version_date: datetime | None = None
    if (
        date_tag := row.find("span", attrs={"class": "mw-version-ext-vcs-timestamp"})
    ) is not None:
        version_date = parse_datetime(date_tag.string)

    return WikibaseSoftwareVersionModel(
        software=await get_or_create_software_model(
            async_session, software_type, software_name
        ),
        version=version,
        version_hash=version_hash,
        version_date=version_date,
    )


def unique_versions(
    input_list: Iterable[WikibaseSoftwareVersionModel],
) -> list[WikibaseSoftwareVersionModel]:
    """Unique Version List"""

    temp: dict[str, WikibaseSoftwareVersionModel] = {}
    for v in input_list:
        temp[str(v)] = v
    return temp.values()
