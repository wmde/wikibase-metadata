"""Wikibase Property Popularity Aggregate Count"""

from datetime import datetime
from typing import List, Optional
import strawberry

from model.strawberry.output.observation.software_version.software_version import (
    VersionStrawberryModel,
)


@strawberry.type
class WikibaseSoftwareVersionAggregateStrawberryModel(VersionStrawberryModel):
    """Wikibase Software Version Aggregate"""

    id: strawberry.ID
    wikibase_count: int = strawberry.field(description="Number of Wikibases Used")

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

    @strawberry.field(description="Version List")
    def versions(self) -> List[WikibaseSoftwareVersionAggregateStrawberryModel]:
        """Version List"""

        return sorted(
            self.private_versions,
            key=lambda x: (x.wikibase_count, x.version or ""),
            reverse=True,
        )
