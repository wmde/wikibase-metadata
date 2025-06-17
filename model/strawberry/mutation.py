"""Mutation"""

import strawberry

from resolvers import add_wikibase
from fetch_data import (
    create_connectivity_observation,
    create_log_observation,
    create_property_popularity_observation,
    create_quantity_observation,
    create_software_version_observation,
    create_special_statistics_observation,
    create_user_observation,
    update_cloud_instances,
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

    add_wikibase = strawberry.mutation(
        description="Add Wikibase", resolver=add_wikibase
    )

    fetch_connectivity_data = strawberry.mutation(
        description="Fetch Connectivity Data from Specified Wikibase Instance",
        resolver=create_connectivity_observation,
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
        resolver=create_quantity_observation,
    )

    fetch_statistics_data = strawberry.mutation(
        description="Fetch Special:Statistics Data",
        resolver=create_special_statistics_observation,
    )

    fetch_user_data = strawberry.mutation(
        description="Fetch User Data from Specified Wikibase Instance",
        resolver=create_user_observation,
    )

    fetch_version_data = strawberry.mutation(
        description="Scrape data from Special:Version page",
        resolver=create_software_version_observation,
    )

    merge_software_by_id = strawberry.mutation(
        description="Merge Software",
        resolver=merge_software_by_id,
    )

    add_wikibase_language = strawberry.mutation(
        description="Add Language to Wikibase", resolver=add_wikibase_language
    )

    remove_wikibase_language = strawberry.mutation(
        description="Remove Language from Wikibase", resolver=remove_wikibase_language
    )

    remove_wikibase_url = strawberry.mutation(
        description="Remove URL from Wikibase", resolver=remove_wikibase_url
    )

    set_extension_wbs_bundled = strawberry.mutation(
        description="Set Extension Bundled with WBS", resolver=set_extension_wbs_bundled
    )

    update_wikibase_primary_language = strawberry.mutation(
        description="Update Wikibase Primary Language",
        resolver=update_wikibase_primary_language,
    )

    update_wikibase_type = strawberry.mutation(
        description="Update Wikibase Type", resolver=update_wikibase_type
    )

    upsert_wikibase_url = strawberry.mutation(
        description="Add / Update Wikibase URL", resolver=upsert_wikibase_url
    )

    update_cloud_instances = strawberry.mutation(
        description="Update the list of known Wikibase Cloud instances from API",
        resolver=update_cloud_instances
    )

