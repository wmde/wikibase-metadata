"""GraphQL Mutation"""

import strawberry

from fetch_data import (
    create_connectivity_data_observation,
    create_log_observation,
    create_property_popularity_observation,
    create_quantity_data_observation,
    create_software_version_observation,
    create_user_data_observation,
)


@strawberry.type
class Mutation:
    """Mutation"""

    fetch_connectivity_data = strawberry.mutation(
        description="Fetch Connectivity Data from Specified Wikibase Instance",
        resolver=create_connectivity_data_observation,
    )

    fetch_log_data = strawberry.mutation(
        description="Fetch Log Data from Specified Wikibase Instance",
        resolver=create_log_observation,
    )

    fetch_property_popularity_data = strawberry.mutation(
        description="Fetch Property Popularity from Specified Wikibase Instance",
        resolver=create_property_popularity_observation,
    )

    fetch_quantity_data = strawberry.mutation(
        description="Fetch Quantity Data from Specified Wikibase Instance",
        resolver=create_quantity_data_observation,
    )

    fetch_user_data = strawberry.mutation(
        description="Fetch User Data from Specified Wikibase Instance",
        resolver=create_user_data_observation,
    )

    fetch_version_data = strawberry.mutation(
        description="Scrape data from Special:Version page",
        resolver=create_software_version_observation,
    )
