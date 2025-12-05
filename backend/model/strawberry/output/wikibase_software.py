"""Wikibase Instance Strawberry Model"""

from datetime import datetime
from typing import Optional
import strawberry

from model.database import WikibaseSoftwareModel
from model.enum.wikibase_software_type_enum import WikibaseSoftwareType


@strawberry.type(name="WikibaseSoftware")
class WikibaseSoftwareStrawberryModel:
    """Wikibase Software"""

    id: strawberry.ID
    software_type: WikibaseSoftwareType = strawberry.field(
        description="Wikibase Software Type"
    )
    software_name: str = strawberry.field(description="Wikibase Software Name")

    url: Optional[str] = strawberry.field(description="Reference URL")

    fetched: Optional[datetime] = strawberry.field(
        description="Date Fetched from MediaWiki"
    )

    tags: list[str] = strawberry.field(description="Tag List")

    description: Optional[str] = strawberry.field(description="Description")

    latest_version: Optional[str] = strawberry.field(description="Latest Version")

    quarterly_download_count: Optional[int] = strawberry.field(
        description="Quarterly Downloads"
    )

    public_wiki_count: Optional[int] = strawberry.field(
        description="Public Wikis Using"
    )

    mediawiki_bundled: Optional[bool] = strawberry.field(
        description="Bundled with MediaWiki"
    )

    wikibase_suite_bundled: Optional[bool] = strawberry.field(
        description="Bundled with Wikibase Suite"
    )

    archived: Optional[bool] = strawberry.field(description="Archived Extension")

    @classmethod
    def marshal(cls, model: WikibaseSoftwareModel) -> "WikibaseSoftwareStrawberryModel":
        """Coerce Database Model to Strawberry Model"""

        return cls(
            id=strawberry.ID(model.id),
            software_type=model.software_type,
            software_name=model.software_name,
            url=model.url,
            fetched=model.data_fetched,
            tags=sorted(a.tag for a in model.tags),
            description=model.description,
            latest_version=model.latest_version,
            quarterly_download_count=model.quarterly_download_count,
            public_wiki_count=model.public_wiki_count,
            mediawiki_bundled=model.mediawiki_bundled,
            wikibase_suite_bundled=(
                model.mediawiki_bundled or model.wikibase_suite_bundled
            ),
            archived=model.archived,
        )
