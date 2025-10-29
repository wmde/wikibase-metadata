"""Insert/Update Wikibase-Related Mutations"""

from typing import Optional
import strawberry
from strawberry import Info

from fetch_data import update_cloud_instances
from model.enum import WikibaseType, WikibaseURLType
from model.strawberry.input import WikibaseInput
from model.strawberry.output import WikibaseStrawberryModel
from resolvers import (
    add_wikibase,
    add_wikibase_language,
    authenticate,
    remove_wikibase_language,
    remove_wikibase_url,
    update_wikibase_primary_language,
    update_wikibase_type,
    upsert_wikibase_url,
)


@strawberry.type
class UpsertWikibaseMutation:
    """Insert/Update Wikibase-Related Mutations"""

    @strawberry.mutation(description="Add Wikibase")
    async def add_wikibase(
        self, wikibase_input: WikibaseInput
    ) -> WikibaseStrawberryModel:
        """Add Wikibase"""

        return await add_wikibase(wikibase_input)

    @strawberry.mutation(description="Add Language to Wikibase")
    async def add_wikibase_language(
        self, info: Info, wikibase_id: int, language: str
    ) -> bool:
        """Add Language to Wikibase"""

        authenticate(info)
        return await add_wikibase_language(wikibase_id, language)

    @strawberry.mutation(description="Remove Language from Wikibase")
    async def remove_wikibase_language(
        self, info: Info, wikibase_id: int, language: str
    ) -> bool:
        """Remove Language from Wikibase"""

        authenticate(info)
        return await remove_wikibase_language(wikibase_id, language)

    @strawberry.mutation(description="Remove URL from Wikibase")
    async def remove_wikibase_url(
        self, info: Info, wikibase_id: int, url_type: WikibaseURLType
    ) -> bool:
        """Remove URL from Wikibase"""

        authenticate(info)
        return await remove_wikibase_url(wikibase_id, url_type)

    @strawberry.mutation(
        description="Update the list of known Wikibase Cloud instances from API"
    )
    async def update_cloud_instances(self, info: Info) -> bool:
        """Update the list of known Wikibase Cloud instances from API"""

        authenticate(info)
        return await update_cloud_instances()

    @strawberry.mutation(description="Update Wikibase Primary Language")
    async def update_wikibase_primary_language(
        self, info: Info, wikibase_id: int, language: str
    ) -> bool:
        """Update Wikibase Primary Language"""

        authenticate(info)
        return await update_wikibase_primary_language(wikibase_id, language)

    @strawberry.mutation(description="Update Wikibase Type")
    async def update_wikibase_type(
        self, info: Info, wikibase_id: int, wikibase_type: Optional[WikibaseType]
    ) -> bool:
        """Update Wikibase Type"""

        authenticate(info)
        return await update_wikibase_type(wikibase_id, wikibase_type)

    @strawberry.mutation(description="Add / Update Wikibase URL")
    async def upsert_wikibase_url(
        self, info: Info, wikibase_id: int, url: str, url_type: WikibaseURLType
    ) -> bool:
        """Add / Update Wikibase URL"""

        authenticate(info)
        return await upsert_wikibase_url(wikibase_id, url, url_type)
