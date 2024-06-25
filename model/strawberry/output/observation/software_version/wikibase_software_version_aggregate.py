"""Wikibase Property Popularity Aggregate Count"""

from datetime import datetime
from typing import List, Optional
import strawberry

from model.strawberry.output.observation.observation_aggregate import (
    AggregateStrawberryModel,
)
from model.strawberry.output.observation.software_version.wikibase_software_version import (
    VersionStrawberryModel,
)


@strawberry.type
class WikibaseSoftwareVersionAggregateStrawberryModel(
    VersionStrawberryModel, AggregateStrawberryModel
):
    """Wikibase Software Version Aggregate"""

    id: strawberry.ID

    def __init__(
        self,
        id: int,
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
    _versions: strawberry.Private[List[WikibaseSoftwareVersionAggregateStrawberryModel]]

    def __init__(
        self,
        id: int,
        software_name: str,
        versions: List[WikibaseSoftwareVersionAggregateStrawberryModel],
    ):
        self.id = strawberry.ID(id)
        self.software_name = software_name
        self._versions = versions

    @strawberry.field
    def wikibase_count(self) -> int:
        return sum([v.wikibase_count for v in self._versions])

    @strawberry.field
    def versions(self) -> List[WikibaseSoftwareVersionAggregateStrawberryModel]:
        return sorted(
            self._versions, key=lambda x: (x.wikibase_count, x.version or ""), reverse=True
        )
