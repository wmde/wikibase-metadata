"""Wikibase Software Version Aggregate Strawberry Models"""

from datetime import datetime
import re
from typing import List, Optional
import strawberry

from model.strawberry.output.semver import Semver
from model.strawberry.scalars import BigInt


@strawberry.type
class WikibaseSoftwareVersionAggregateStrawberryModel:
    """Wikibase Software Version Aggregate"""

    version: Optional[str] = strawberry.field(description="Software Version")
    version_date: Optional[datetime] = strawberry.field(description="Software Version")
    version_hash: Optional[str] = strawberry.field(description="Software Version")
    wikibase_count: int = strawberry.field(
        description="Number of Wikibases Used", graphql_type=BigInt
    )

    semver_version: strawberry.Private[Optional[Semver]]

    def __init__(
        self,
        version: Optional[str],
        version_date: Optional[datetime],
        version_hash: Optional[str],
        wikibase_count: int,
    ):
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
                temp[key] = WikibaseSoftwarePatchVersionAggregateStrawberryModel(
                    version=str(
                        Semver(
                            v.semver_version.major,
                            v.semver_version.minor,
                            v.semver_version.patch,
                        )
                    ),
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
                    version=str(Semver(v.semver_version.major, v.semver_version.minor)),
                    private_versions=[],
                )
            temp[key].private_versions.append(v)
        return sorted(temp.values(), key=lambda x: x.wikibase_count(), reverse=True)


@strawberry.type
class WikibaseSoftwareVersionDoubleAggregateStrawberryModel:
    """Wikibase Software Version Aggregate"""

    software_name: str = strawberry.field(description="Software Name")
    private_versions: strawberry.Private[
        List[WikibaseSoftwareVersionAggregateStrawberryModel]
    ]

    def __init__(
        self,
        software_name: str,
        versions: List[WikibaseSoftwareVersionAggregateStrawberryModel],
    ):
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
            Optional[int], WikibaseSoftwareMajorVersionAggregateStrawberryModel
        ] = {}
        for v in self.private_versions:
            key = None if v.semver_version is None else v.semver_version.major
            if key not in temp:
                temp[key] = WikibaseSoftwareMajorVersionAggregateStrawberryModel(
                    version=key, private_versions=[]
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
