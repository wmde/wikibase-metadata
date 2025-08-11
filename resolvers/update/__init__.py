"""Update Data"""

from resolvers.update.merge_software import merge_software_by_id
from resolvers.update.set_extension_wbs_bundled import set_extension_wbs_bundled
from resolvers.update.update_wikibase_language import (
    add_wikibase_language,
    remove_wikibase_language,
    update_wikibase_primary_language,
)
from resolvers.update.update_wikibase_type import update_wikibase_type
from resolvers.update.update_wikibase_url import (
    remove_wikibase_url,
    upsert_wikibase_url,
)
