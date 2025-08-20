"""Mutation"""

from typing import Optional
import strawberry
from strawberry import Info

from fetch_data import (
    create_connectivity_observation,
    create_log_observation,
    create_property_popularity_observation,
    create_quantity_observation,
    create_recent_changes_observation,
    create_software_version_observation,
    create_special_statistics_observation,
    create_user_observation,
    update_cloud_instances,
)
from model.enum import WikibaseType, WikibaseURLType
from model.strawberry.input import WikibaseInput
from model.strawberry.output import WikibaseStrawberryModel
from resolvers import (
    add_wikibase,
    add_wikibase_language,
    authenticate,
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
        self, wikibase_input: WikibaseInput
    ) -> WikibaseStrawberryModel:
        """Add Wikibase"""

        return await add_wikibase(wikibase_input)

    @strawberry.mutation(
        description="Fetch Connectivity Data from Specified Wikibase Instance"
    )
    async def fetch_connectivity_data(self, info: Info, wikibase_id: int) -> bool:
        """Fetch Connectivity Data from Specified Wikibase Instance"""

        authenticate(info)
        return await create_connectivity_observation(wikibase_id)

    @strawberry.mutation(description="Fetch Log Data from Specified Wikibase Instance")
    async def fetch_log_data(
        self, info: Info, wikibase_id: int, first_month: bool
    ) -> bool:
        """Fetch Log Data from Specified Wikibase Instance"""

        authenticate(info)
        return await create_log_observation(wikibase_id, first_month)

    @strawberry.mutation(
        description="Fetch Property Popularity from Specified Wikibase Instance"
    )
    async def fetch_property_popularity_data(
        self, info: Info, wikibase_id: int
    ) -> bool:
        """Fetch Property Popularity from Specified Wikibase Instance"""

        authenticate(info)
        return await create_property_popularity_observation(wikibase_id)

    @strawberry.mutation(
        description="Fetch Quantity Data from Specified Wikibase Instance"
    )
    async def fetch_quantity_data(self, info: Info, wikibase_id: int) -> bool:
        """Fetch Quantity Data from Specified Wikibase Instance"""

        authenticate(info)
        return await create_quantity_observation(wikibase_id)

    @strawberry.mutation(
        description="Fetch Recent Changes Data from Specified Wikibase Instance"
    )
    async def fetch_recent_changes_data(self, info: Info, wikibase_id: int) -> bool:
        """Fetch Recent Changes Data from Specified Wikibase Instance"""

        authenticate(info)
        return await create_recent_changes_observation(wikibase_id)

    @strawberry.mutation(description="Fetch Special:Statistics Data")
    async def fetch_statistics_data(self, info: Info, wikibase_id: int) -> bool:
        """Fetch Special:Statistics Data"""

        authenticate(info)
        return await create_special_statistics_observation(wikibase_id)

    @strawberry.mutation(description="Fetch User Data from Specified Wikibase Instance")
    async def fetch_user_data(self, info: Info, wikibase_id: int) -> bool:
        """Fetch User Data from Specified Wikibase Instance"""

        authenticate(info)
        return await create_user_observation(wikibase_id)

    @strawberry.mutation(description="Scrape data from Special:Version page")
    async def fetch_version_data(self, info: Info, wikibase_id: int) -> bool:
        """Scrape data from Special:Version page"""

        authenticate(info)
        return await create_software_version_observation(wikibase_id, info)

    @strawberry.mutation(description="Merge Software")
    async def merge_software_by_id(
        self, info: Info, base_id: int, additional_id: int
    ) -> bool:
        """Merge Software"""

        authenticate(info)
        return await merge_software_by_id(base_id, additional_id)

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

    @strawberry.mutation(description="Set Extension Bundled with WBS")
    async def set_extension_wbs_bundled(
        self, info: Info, extension_id: int, bundled: bool = True
    ) -> bool:
        """Set Extension Bundled with WBS"""

        authenticate(info)
        return await set_extension_wbs_bundled(extension_id, bundled)

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
