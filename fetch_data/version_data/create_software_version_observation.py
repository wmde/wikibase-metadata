"""Create Software Version Observation"""

from datetime import datetime
from typing import List
from bs4 import BeautifulSoup, Tag
import requests
from data import get_async_session
from fetch_data.utils import get_wikibase_from_database, parse_datetime
from model.database import (
    WikibaseModel,
    WikibaseSoftwareTypes,
    WikibaseSoftwareVersionModel,
    WikibaseSoftwareVersionObservationModel,
)


async def create_software_version_observation(wikibase_id: int) -> bool:
    """Create Software Version Observation"""

    async with get_async_session() as async_session:
        wikibase: WikibaseModel = await get_wikibase_from_database(
            async_session=async_session,
            wikibase_id=wikibase_id,
            require_special_version=True,
        )

        observation = WikibaseSoftwareVersionObservationModel()

        result = requests.get(
            wikibase.special_version_url.url,
            headers={"Cookie": "mediawikilanguage=en"},
            timeout=10,
        )
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
    """Compile Extension Version List"""

    extensions_table = soup.find(
        "table", attrs={"id": ["sv-ext", "sv-credits-specialpage"]}
    )
    return unique_versions(
        [
            get_software_version_from_row(row, WikibaseSoftwareTypes.EXTENSION)
            for row in extensions_table.find_all(
                "tr", attrs={"class": "mw-version-ext"}
            )
        ]
    )


def compile_installed_software_versions(
    soup: BeautifulSoup,
) -> List[WikibaseSoftwareVersionModel]:
    """Compile Installed Software Version List"""

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
                version_date = parse_datetime(version_strings[2])
            elif len(version_strings) == 2:
                version = version_strings[0]
                version_hash = version_strings[1]
            else:
                raise NotImplementedError(f"{version_strings}")

            software_versions.append(
                WikibaseSoftwareVersionModel(
                    software_type=WikibaseSoftwareTypes.SOFTWARE,
                    software_name=software_name,
                    version=version,
                    version_hash=version_hash,
                    version_date=version_date,
                )
            )

    return software_versions


def compile_library_versions(soup: BeautifulSoup) -> List[WikibaseSoftwareVersionModel]:
    """Compile Library Version List"""

    libraries_table = soup.find("table", attrs={"id": "sv-libraries"})

    library_versions: List[WikibaseSoftwareVersionModel] = []
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
                        software_type=WikibaseSoftwareTypes.LIBRARY,
                        software_name=software_name,
                        version=version,
                    )
                )

    return unique_versions(library_versions)


def compile_skin_versions(soup: BeautifulSoup) -> List[WikibaseSoftwareVersionModel]:
    """Compile Skin Version List"""

    installed_skin_table: Tag = soup.find(
        "table", attrs={"id": ["sv-skin", "sv-credits-skin"]}
    )
    return unique_versions(
        [
            get_software_version_from_row(row, WikibaseSoftwareTypes.SKIN)
            for row in installed_skin_table.find_all(
                "tr", attrs={"class": "mw-version-ext"}
            )
        ]
    )


def get_software_version_from_row(
    row: Tag, software_type: WikibaseSoftwareTypes
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
        software_type=software_type,
        software_name=software_name,
        version=version,
        version_hash=version_hash,
        version_date=version_date,
    )


def unique_versions(
    input_list: List[WikibaseSoftwareVersionModel],
) -> List[WikibaseSoftwareVersionModel]:
    """Unique Version List"""

    temp: dict[str, WikibaseSoftwareVersionModel] = {}
    for v in input_list:
        temp[str(v)] = v
    return temp.values()
