"""Wikibase Property Popularity Aggregate Count"""

from datetime import datetime
import re
from typing import List, Optional
import strawberry

from model.strawberry.output.semver import Semver


@strawberry.type
class WikibaseSoftwareVersionAggregateStrawberryModel:
    """Wikibase Software Version Aggregate"""

    id: strawberry.ID
    version: Optional[str] = strawberry.field(description="Software Version")
    version_date: Optional[datetime] = strawberry.field(description="Software Version")
    version_hash: Optional[str] = strawberry.field(description="Software Version")
    wikibase_count: int = strawberry.field(description="Number of Wikibases Used")

    semver_version: strawberry.Private[Optional[Semver]]

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        id: int,  # pylint: disable=redefined-builtin
        version: Optional[str],
        version_date: Optional[datetime],
        version_hash: Optional[str],
        wikibase_count: int,
    ):
        self.id = strawberry.ID(id)
        self.version = version
        self.version_date = version_date
        self.version_hash = version_hash
        self.wikibase_count = wikibase_count

        self.semver_version = None
        if version is not None:
            if (semver_match := re.match(r"(\d+)\.(\d+)\.(\d+)", version)) is not None:
                self.semver_version = Semver(
                    int(semver_match.group(1)),
                    int(semver_match.group(2)),
                    int(semver_match.group(3)),
                )
            elif (semver_match := re.match(r"(\d+)\.(\d+)", version)) is not None:
                self.semver_version = Semver(
                    int(semver_match.group(1)), int(semver_match.group(2))
                )


@strawberry.type
class WikibaseSoftwareMidVersionAggregateStrawberryModel:
    """Aggregated to X Version - ABSTRACT"""

    id: strawberry.ID
    version: Optional[str] = strawberry.field(description="Software Version")

    private_versions: strawberry.Private[
        List[WikibaseSoftwareVersionAggregateStrawberryModel]
    ]

    @strawberry.field(description="Wikibase Count")
    def wikibase_count(self) -> int:
        """Wikibase Count"""

        return sum(v.wikibase_count for v in self.private_versions)


@strawberry.type
class WikibaseSoftwarePatchVersionAggregateStrawberryModel(
    WikibaseSoftwareMidVersionAggregateStrawberryModel
):
    """Aggregated to Patch Version"""

    @strawberry.field(description="Versions")
    def sub_versions(
        self,
    ) -> Optional[List[WikibaseSoftwareVersionAggregateStrawberryModel]]:
        """Sub-Patch Versions"""

        if (
            len(self.private_versions) == 1
            and (
                (only_version := self.private_versions[0]).version is None
                or only_version.version == str(only_version.semver_version)
            )
            and only_version.version_date is None
            and only_version.version_hash is None
        ):
            return None
        return sorted(
            self.private_versions, key=lambda x: x.wikibase_count, reverse=True
        )


@strawberry.type
class WikibaseSoftwareMinorVersionAggregateStrawberryModel(
    WikibaseSoftwareMidVersionAggregateStrawberryModel
):
    """Aggregated to Minor Version"""

    @strawberry.field(description="Patch Versions")
    def patch_versions(
        self,
    ) -> Optional[List[WikibaseSoftwarePatchVersionAggregateStrawberryModel]]:
        """Patch Versions"""

        if self.version is None:
            return None
        temp: dict[
            Optional[int], WikibaseSoftwarePatchVersionAggregateStrawberryModel
        ] = {}
        for v in self.private_versions:
            key = None if v.semver_version is None else v.semver_version.patch
            if key not in temp:
                temp[key] = WikibaseSoftwareMidVersionAggregateStrawberryModel(
                    id=v.id,
                    version=f"{v.semver_version.major}.{v.semver_version.minor}.{v.semver_version.patch}",
                    private_versions=[],
                )
            temp[key].private_versions.append(v)
        return sorted(temp.values(), key=lambda x: x.wikibase_count(), reverse=True)


@strawberry.type
class WikibaseSoftwareMajorVersionAggregateStrawberryModel(
    WikibaseSoftwareMidVersionAggregateStrawberryModel
):
    """Aggregated to Major Version"""

    @strawberry.field(description="Minor Versions")
    def minor_versions(
        self,
    ) -> Optional[List[WikibaseSoftwareMinorVersionAggregateStrawberryModel]]:
        """Minor Versions"""

        if self.version is None:
            return None
        temp: dict[
            Optional[str], WikibaseSoftwareMinorVersionAggregateStrawberryModel
        ] = {}
        for v in self.private_versions:
            key = None if v.semver_version is None else v.semver_version.minor
            if key not in temp:
                temp[key] = WikibaseSoftwareMinorVersionAggregateStrawberryModel(
                    id=v.id,
                    version=f"{v.semver_version.major}.{v.semver_version.minor}",
                    private_versions=[],
                )
            temp[key].private_versions.append(v)
        return sorted(temp.values(), key=lambda x: x.wikibase_count(), reverse=True)


@strawberry.type
class WikibaseSoftwareVersionDoubleAggregateStrawberryModel:
    """Wikibase Software Version Aggregate"""

    id: strawberry.ID
    software_name: str = strawberry.field(description="Software Name")
    private_versions: strawberry.Private[
        List[WikibaseSoftwareVersionAggregateStrawberryModel]
    ]

    def __init__(
        self,
        id: int,  # pylint: disable=redefined-builtin
        software_name: str,
        versions: List[WikibaseSoftwareVersionAggregateStrawberryModel],
    ):
        self.id = strawberry.ID(id)
        self.software_name = software_name
        self.private_versions = versions

    @strawberry.field(description="Wikibase Count")
    def wikibase_count(self) -> int:
        """Wikibase Count"""

        return sum(v.wikibase_count for v in self.private_versions)

    @strawberry.field(description="Major Versions")
    def major_versions(
        self,
    ) -> List[WikibaseSoftwareMajorVersionAggregateStrawberryModel]:
        """Major Versions"""

        temp: dict[
            Optional[str], WikibaseSoftwareMajorVersionAggregateStrawberryModel
        ] = {}
        for v in self.private_versions:
            key = None if v.semver_version is None else str(v.semver_version.major)
            if key not in temp:
                temp[key] = WikibaseSoftwareMajorVersionAggregateStrawberryModel(
                    id=v.id, version=key, private_versions=[]
                )
            temp[key].private_versions.append(v)
        return sorted(temp.values(), key=lambda x: x.wikibase_count(), reverse=True)

    @strawberry.field(description="Version List")
    def versions(self) -> List[WikibaseSoftwareVersionAggregateStrawberryModel]:
        """Version List"""

        return sorted(
            self.private_versions,
            key=lambda x: (x.wikibase_count, x.version or ""),
            reverse=True,
        )
