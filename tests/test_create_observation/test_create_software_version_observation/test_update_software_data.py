"""Test Extension Data"""

import pytest
from fetch_data.soup_data.software.update_software_data import (
    get_update_extension_query,
)


@pytest.mark.version
def test_update_software_data():
    """Test Update Software Data"""

    pass


@pytest.mark.version
def test_get_update_extension_query():
    """Test Update Extension Query"""

    query = get_update_extension_query()
    assert (
        str(query)
        == """SELECT wikibase_software.id, wikibase_software.software_type, wikibase_software.software_name, wikibase_software.url, wikibase_software.fetched, wikibase_software.description, wikibase_software.latest_version, wikibase_software.quarterly_download_count, wikibase_software.public_wiki_count, wikibase_software.mw_bundled, wikibase_software.archived 
FROM wikibase_software 
WHERE (wikibase_software.fetched IS NULL OR wikibase_software.fetched < :fetched_1) AND wikibase_software.software_type = :software_type_1 AND (wikibase_software.archived = false OR wikibase_software.archived IS NULL)
 LIMIT :param_1"""
    )
