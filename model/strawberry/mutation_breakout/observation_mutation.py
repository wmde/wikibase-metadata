"""Observation-Related Mutations"""

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
    create_time_to_first_value_observation,
    create_user_observation,
    update_all_connectivity_observations,
    update_all_log_observations,
    update_all_property_observations,
    update_all_quantity_observations,
    update_all_recent_changes_observations,
    update_all_software_observations,
    update_all_stats_observations,
    update_all_time_to_first_value_observations,
    update_all_user_observations,
)
from fetch_data.bulk.update_bulk import BulkTaskResult
from resolvers import authenticate


@strawberry.type
class ObservationMutation:
    """Observation-Related Mutations"""

    @strawberry.mutation(
        description="Fetch Connectivity Data from Specified Wikibase Instance"
    )
    async def fetch_connectivity_data(self, info: Info, wikibase_id: int) -> bool:
        """Fetch Connectivity Data from Specified Wikibase Instance"""

        authenticate(info)
        return await create_connectivity_observation(wikibase_id)

    @strawberry.mutation(
        description="Fetch Connectivity Data from All Wikibase Instances"
    )
    async def update_all_connectivity_data(self, info: Info) -> BulkTaskResult:
        """Fetch Connectivity Data from All Wikibase Instances"""

        authenticate(info)
        return await update_all_connectivity_observations()

    @strawberry.mutation(description="Fetch Log Data from Specified Wikibase Instance")
    async def fetch_log_data(
        self, info: Info, wikibase_id: int, first_month: bool
    ) -> bool:
        """Fetch Log Data from Specified Wikibase Instance"""

        authenticate(info)
        return await create_log_observation(wikibase_id, first_month)

    @strawberry.mutation(description="Fetch Log Data from All Wikibase Instances")
    async def update_all_log_data(
        self, info: Info, first_month: bool
    ) -> BulkTaskResult:
        """Fetch Log Data from All Wikibase Instances"""

        authenticate(info)
        return await update_all_log_observations(first_month)

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
        description="Fetch Property Popularity from All Wikibase Instances"
    )
    async def update_all_property_popularity_data(self, info: Info) -> BulkTaskResult:
        """Fetch Property Popularity from All Wikibase Instances"""

        authenticate(info)
        return await update_all_property_observations()

    @strawberry.mutation(
        description="Fetch Quantity Data from Specified Wikibase Instance"
    )
    async def fetch_quantity_data(self, info: Info, wikibase_id: int) -> bool:
        """Fetch Quantity Data from Specified Wikibase Instance"""

        authenticate(info)
        return await create_quantity_observation(wikibase_id)

    @strawberry.mutation(description="Fetch Quantity Data from All Wikibase Instances")
    async def update_all_quantity_data(self, info: Info) -> BulkTaskResult:
        """Fetch Quantity Data from All Wikibase Instances"""

        authenticate(info)
        return await update_all_quantity_observations()

    @strawberry.mutation(
        description="Fetch Recent Changes Data from Specified Wikibase Instance"
    )
    async def fetch_recent_changes_data(self, info: Info, wikibase_id: int) -> bool:
        """Fetch Recent Changes Data from Specified Wikibase Instance"""

        authenticate(info)
        return await create_recent_changes_observation(wikibase_id)

    @strawberry.mutation(
        description="Fetch Recent Changes Data from All Wikibase Instances"
    )
    async def update_all_recent_changes_data(self, info: Info) -> BulkTaskResult:
        """Fetch Recent Changes Data from All Wikibase Instances"""

        authenticate(info)
        return await update_all_recent_changes_observations()

    @strawberry.mutation(description="Fetch Special:Statistics Data")
    async def fetch_statistics_data(self, info: Info, wikibase_id: int) -> bool:
        """Fetch Special:Statistics Data"""

        authenticate(info)
        return await create_special_statistics_observation(wikibase_id)

    @strawberry.mutation(
        description="Fetch Special:Statistics Data for All Wikibase Instances"
    )
    async def update_all_statistics_data(self, info: Info) -> BulkTaskResult:
        """Fetch Special:Statistics Data for All Wikibase Instances"""

        authenticate(info)
        return await update_all_stats_observations()

    @strawberry.mutation(
        description="Fetch Time to First Value Data from Specified Wikibase Instance"
    )
    async def fetch_time_to_first_value_data(
        self, info: Info, wikibase_id: int
    ) -> bool:
        """Fetch Time to First Value Data from Specified Wikibase Instance"""

        authenticate(info)
        return await create_time_to_first_value_observation(wikibase_id)

    @strawberry.mutation(
        description="Fetch Time to First Value Data from All Wikibase Instances"
    )
    async def update_all_time_to_first_value_data(self, info: Info) -> BulkTaskResult:
        """Fetch Time to First Value Data from All Wikibase Instances"""

        authenticate(info)
        return await update_all_time_to_first_value_observations()

    @strawberry.mutation(description="Fetch User Data from Specified Wikibase Instance")
    async def fetch_user_data(self, info: Info, wikibase_id: int) -> bool:
        """Fetch User Data from Specified Wikibase Instance"""

        authenticate(info)
        return await create_user_observation(wikibase_id)

    @strawberry.mutation(description="Fetch User Data from All Wikibase Instances")
    async def update_all_user_data(self, info: Info) -> BulkTaskResult:
        """Fetch User Data from All Wikibase Instances"""

        authenticate(info)
        return await update_all_user_observations()

    @strawberry.mutation(description="Scrape data from Special:Version page")
    async def fetch_version_data(self, info: Info, wikibase_id: int) -> bool:
        """Scrape data from Special:Version page"""

        authenticate(info)
        return await create_software_version_observation(wikibase_id, info)

    @strawberry.mutation(
        description="Scrape data from Special:Version page for All Wikibase Instances"
    )
    async def update_all_version_data(self, info: Info) -> BulkTaskResult:
        """Scrape data from Special:Version page All Wikibase Instances"""

        authenticate(info)
        return await update_all_software_observations()
