"""Wikibase Software Version Strawberry Model"""

from datetime import datetime
from typing import Optional
import strawberry

from model.database import WikibaseSoftwareVersionModel
from model.strawberry.output.wikibase_software import WikibaseSoftwareStrawberryModel


@strawberry.type
class WikibaseSoftwareVersionStrawberryModel:
    """Wikibase Software Version"""

    id: strawberry.ID
    software: WikibaseSoftwareStrawberryModel = strawberry.field(description="Software")
    software_name: str = strawberry.field(
        description="Software Name", deprecation_reason="Use software/softwareName"
    )
    version: Optional[str] = strawberry.field(description="Software Version")
    version_date: Optional[datetime] = strawberry.field(
        description="Software Version Release Date"
    )
    version_hash: Optional[str] = strawberry.field(
        description="Software Version Commit Hash"
    )

    @classmethod
    def marshal(
        cls, model: WikibaseSoftwareVersionModel
    ) -> "WikibaseSoftwareVersionStrawberryModel":
        """Coerce Database Model to Strawberry Model"""

        return cls(
            id=strawberry.ID(model.id),
            software=WikibaseSoftwareStrawberryModel.marshal(model.software),
            software_name=model.software.software_name,
            version=model.version,
            version_date=model.version_date,
            version_hash=model.version_hash,
        )
