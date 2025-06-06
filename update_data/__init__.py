"""Update Data"""

from update_data.merge_software import merge_software_by_id
from update_data.set_extension_wbs_bundled import set_extension_wbs_bundled
from update_data.update_wikibase_language import (
    add_wikibase_language,
    remove_wikibase_language,
    update_wikibase_primary_language,
)
from update_data.update_wikibase_type import update_wikibase_type
from update_data.update_wikibase_url import remove_wikibase_url, upsert_wikibase_url
