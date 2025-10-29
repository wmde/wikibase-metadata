"""Resolvers"""

from resolvers.add import add_wikibase
from resolvers.authentication import authenticate
from resolvers.get_aggregate import (
    get_aggregate_created,
    get_aggregate_external_identifier,
    get_aggregate_property_popularity,
    get_aggregate_quantity,
    get_aggregate_recent_changes,
    get_aggregate_statistics,
    get_aggregate_users,
    get_aggregate_version,
    get_language_list,
)
from resolvers.get_software_list import get_software_list
from resolvers.get_wikibase import get_wikibase
from resolvers.get_wikibase_list import get_wikibase_page
from resolvers.update import (
    add_wikibase_language,
    merge_software_by_id,
    remove_wikibase_language,
    remove_wikibase_url,
    set_extension_wbs_bundled,
    update_wikibase_primary_language,
    update_wikibase_type,
    upsert_wikibase_url,
)
