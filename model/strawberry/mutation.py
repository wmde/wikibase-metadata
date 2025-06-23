"""Mutation"""

from typing import Optional
import strawberry
from strawberry import Info

from model.enum import WikibaseType, WikibaseURLType
from model.strawberry.input import WikibaseInput
from model.strawberry.output import WikibaseStrawberryModel
from resolvers import add_wikibase, authenticate
from fetch_data import (
    create_connectivity_observation,
    create_log_observation,
    create_property_popularity_observation,
    create_quantity_observation,
    create_software_version_observation,
    create_special_statistics_observation,
    create_user_observation,
)
from update_data import (
    add_wikibase_language,
    merge_software_by_id,
    remove_wikibase_language,
    remove_wikibase_url,
    set_extension_wbs_bundled,
    update_wikibase_primary_language,
    update_wikibase_type,
    upsert_wikibase_url,
)


@strawberry.type
class Mutation:
    """Mutation"""

    @strawberry.mutation(description="Add Wikibase")
    async def add_wikibase(
        self, wikibase_input: WikibaseInput, info: Info
    ) -> WikibaseStrawberryModel:
        """Add Wikibase"""

        authenticate(info)
        return await add_wikibase(wikibase_input)

    @strawberry.mutation(
        description="Fetch Connectivity Data from Specified Wikibase Instance"
    )
    async def fetch_connectivity_data(self, wikibase_id: int, info: Info) -> bool:
        """Fetch Connectivity Data from Specified Wikibase Instance"""

        authenticate(info)
        return await create_connectivity_observation(wikibase_id)

    @strawberry.mutation(description="Fetch Log Data from Specified Wikibase Instance")
    async def fetch_log_data(
        self, wikibase_id: int, first_month: bool, info: Info
    ) -> bool:
        """Fetch Log Data from Specified Wikibase Instance"""

        authenticate(info)
        return await create_log_observation(wikibase_id, first_month)

    @strawberry.mutation(
        description="Fetch Property Popularity from Specified Wikibase Instance"
    )
    async def fetch_property_popularity_data(
        self, wikibase_id: int, info: Info
    ) -> bool:
        """Fetch Property Popularity from Specified Wikibase Instance"""

        authenticate(info)
        return await create_property_popularity_observation(wikibase_id)

    @strawberry.mutation(
        description="Fetch Quantity Data from Specified Wikibase Instance"
    )
    async def fetch_quantity_data(self, wikibase_id: int, info: Info) -> bool:
        """Fetch Quantity Data from Specified Wikibase Instance"""

        authenticate(info)
        return await create_quantity_observation(wikibase_id)

    @strawberry.mutation(description="Fetch Special:Statistics Data")
    async def fetch_statistics_data(self, wikibase_id: int, info: Info) -> bool:
        """Fetch Special:Statistics Data"""

        authenticate(info)
        return await create_special_statistics_observation(wikibase_id)

    @strawberry.mutation(description="Fetch User Data from Specified Wikibase Instance")
    async def fetch_user_data(self, wikibase_id: int, info: Info) -> bool:
        """Fetch User Data from Specified Wikibase Instance"""

        authenticate(info)
        return await create_user_observation(wikibase_id)

    @strawberry.mutation(description="Scrape data from Special:Version page")
    async def fetch_version_data(self, wikibase_id: int, info: Info) -> bool:
        """Scrape data from Special:Version page"""

        authenticate(info)
        return await create_software_version_observation(wikibase_id, info)

    @strawberry.mutation(description="Merge Software")
    async def merge_software_by_id(
        self, base_id: int, additional_id: int, info: Info
    ) -> bool:
        """Merge Software"""

        authenticate(info)
        return await merge_software_by_id(base_id, additional_id)

    @strawberry.mutation(description="Add Language to Wikibase")
    async def add_wikibase_language(
        self, wikibase_id: int, language: str, info: Info
    ) -> bool:
        """Add Language to Wikibase"""

        authenticate(info)
        return await add_wikibase_language(wikibase_id, language)

    @strawberry.mutation(description="Remove Language from Wikibase")
    async def remove_wikibase_language(
        self, wikibase_id: int, language: str, info: Info
    ) -> bool:
        """Remove Language from Wikibase"""

        authenticate(info)
        return await remove_wikibase_language(wikibase_id, language)

    @strawberry.mutation(description="Remove URL from Wikibase")
    async def remove_wikibase_url(
        self, wikibase_id: int, url_type: WikibaseURLType, info: Info
    ) -> bool:
        """Remove URL from Wikibase"""

        authenticate(info)
        return await remove_wikibase_url(wikibase_id, url_type)

    @strawberry.mutation(description="Set Extension Bundled with WBS")
    async def set_extension_wbs_bundled(
        self, extension_id: int, bundled: bool, info: Info
    ) -> bool:
        """Set Extension Bundled with WBS"""

        authenticate(info)
        return await set_extension_wbs_bundled(extension_id, bundled)

    @strawberry.mutation(description="Update Wikibase Primary Language")
    async def update_wikibase_primary_language(
        self, wikibase_id: int, language: str, info: Info
    ) -> bool:
        """Update Wikibase Primary Language"""

        authenticate(info)
        return await update_wikibase_primary_language(wikibase_id, language)

    @strawberry.mutation(description="Update Wikibase Type")
    async def update_wikibase_type(
        self, wikibase_id: int, wikibase_type: Optional[WikibaseType], info: Info
    ) -> bool:
        """Update Wikibase Type"""

        authenticate(info)
        return await update_wikibase_type(wikibase_id, wikibase_type)

    @strawberry.mutation(description="Add / Update Wikibase URL")
    async def upsert_wikibase_url(
        self, wikibase_id: int, url: str, url_type: WikibaseURLType, info: Info
    ) -> bool:
        """Add / Update Wikibase URL"""

        authenticate(info)
        return await upsert_wikibase_url(wikibase_id, url, url_type)
