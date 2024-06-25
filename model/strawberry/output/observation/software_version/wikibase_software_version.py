"""Wikibase Software Version"""

from datetime import datetime
from typing import Optional
import strawberry

from model.database import WikibaseSoftwareVersionModel


@strawberry.type
class VersionStrawberryModel:
    """Version"""

    version: str = strawberry.field(description="Software Version")
    version_date: Optional[datetime] = strawberry.field(
        description="Software Version Release Date"
    )
    version_hash: Optional[str] = strawberry.field(
        description="Software Version Commit Hash"
    )


@strawberry.type
class WikibaseSoftwareVersionStrawberryModel(VersionStrawberryModel):
    """Wikibase Software Version"""

    id: strawberry.ID
    software_name: str = strawberry.field(description="Software Name")

    @classmethod
    def marshal(
        cls, model: WikibaseSoftwareVersionModel
    ) -> "WikibaseSoftwareVersionStrawberryModel":
        """Coerce Database Model to Strawberry Model"""

        return cls(
            id=strawberry.ID(model.id),
            software_name=model.software_name,
            version=model.version,
            version_date=model.version_date,
            version_hash=model.version_hash,
        )
