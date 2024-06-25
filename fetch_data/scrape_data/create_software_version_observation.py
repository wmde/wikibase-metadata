from datetime import datetime
from typing import List
from bs4 import BeautifulSoup, Tag
import requests
from data.database_connection import get_async_session
from fetch_data.utils.get_wikibase import get_wikibase_from_database
from model.database.wikibase_model import WikibaseModel
from model.database.wikibase_observation.version.software_version_model import (
    WikibaseSoftwareTypes,
    WikibaseSoftwareVersionModel,
)
from model.database.wikibase_observation.version.wikibase_version_observation_model import (
    WikibaseSoftwareVersionObservationModel,
)


async def create_software_version_observation(wikibase_id: int) -> bool:
    async with get_async_session() as async_session:
        wikibase: WikibaseModel = await get_wikibase_from_database(
            async_session=async_session,
            wikibase_id=wikibase_id,
            require_special_version=True,
        )

        observation = WikibaseSoftwareVersionObservationModel()

        result = requests.get(wikibase.special_version_url)
        soup = BeautifulSoup(result.content, "html.parser")

        observation.returned_data = True

        installed_software_versions = compile_installed_software_versions(soup)
        observation.software_versions.extend(installed_software_versions)

        skin_versions = compile_skin_versions(soup)
        observation.software_versions.extend(skin_versions)

        extensions_versions = compile_extension_versions(soup)
        observation.software_versions.extend(extensions_versions)

        library_versions = compile_library_versions(soup)
        observation.software_versions.extend(library_versions)

        wikibase.software_version_observations.append(observation)

        await async_session.commit()
        return observation.returned_data


def compile_extension_versions(
    soup: BeautifulSoup,
) -> List[WikibaseSoftwareVersionModel]:
    extensions_table = soup.find(
        "table", attrs={"id": ["sv-ext", "sv-credits-specialpage"]}
    )
    return [
        get_software_version_from_row(row, WikibaseSoftwareTypes.extension)
        for row in extensions_table.find_all("tr", attrs={"class": "mw-version-ext"})
    ]


def compile_installed_software_versions(
    soup: BeautifulSoup,
) -> List[WikibaseSoftwareVersionModel]:
    installed_software_table: Tag = soup.find("table", attrs={"id": "sv-software"})

    software_versions: List[WikibaseSoftwareVersionModel] = []
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
                version = version_strings[0]
                version_hash = version_strings[1]
                version_date = datetime.strptime(version_strings[2], "%H:%M, %d %B %Y")
            else:
                raise NotImplementedError(
                    f"{[s for s in row.find_all('td')[1].strings]}"
                )

            software_versions.append(
                WikibaseSoftwareVersionModel(
                    software_type=WikibaseSoftwareTypes.software,
                    software_name=software_name,
                    version=version,
                    version_hash=version_hash,
                    version_date=version_date,
                )
            )

    return software_versions


def compile_library_versions(soup: BeautifulSoup) -> List[WikibaseSoftwareVersionModel]:
    libraries_table = soup.find("table", attrs={"id": "sv-libraries"})

    library_versions: List[WikibaseSoftwareVersionModel] = []
    row: Tag
    for row in libraries_table.find_all("tr"):
        if row.find("td"):
            software_name = row.find(
                "a", attrs={"class": "mw-version-library-name"}
            ).string
            version = row.find_all("td")[1].string
            library_versions.append(
                WikibaseSoftwareVersionModel(
                    software_type=WikibaseSoftwareTypes.library,
                    software_name=software_name,
                    version=version,
                )
            )

    return library_versions


def compile_skin_versions(soup: BeautifulSoup) -> List[WikibaseSoftwareVersionModel]:
    installed_skin_table: Tag = soup.find(
        "table", attrs={"id": ["sv-skin", "sv-credits-skin"]}
    )
    return [
        get_software_version_from_row(row, WikibaseSoftwareTypes.skin)
        for row in installed_skin_table.find_all(
            "tr", attrs={"class": "mw-version-ext"}
        )
    ]


def get_software_version_from_row(
    row: Tag, software_type: WikibaseSoftwareTypes
) -> WikibaseSoftwareVersionModel:
    software_name = row.find("a", attrs={"class": "mw-version-ext-name"}).string
    version = row.find("span", attrs={"class": "mw-version-ext-version"}).string

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
        version_date = datetime.strptime(date_tag.string, "%H:%M, %d %B %Y")

    return WikibaseSoftwareVersionModel(
        software_type=software_type,
        software_name=software_name,
        version=version,
        version_hash=version_hash,
        version_date=version_date,
    )
