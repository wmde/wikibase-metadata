"""Test Query Cloud Instances"""

import pytest

from tests.test_schema import test_schema
from tests.test_upsert_cloud_instances.constant import WIKIBASE_LIST_QUERY
from tests.utils import get_mock_context



@pytest.mark.dependency(
    name="query-cloud-instances", depends=["transform-cloud-instances"], scope="session"
)
@pytest.mark.asyncio
async def test_query_cloud_instance():
    """
    test whether querying the wikibase list via graphql returns a cloud instance
    """
    result = await test_schema.execute(
        WIKIBASE_LIST_QUERY, context_value=get_mock_context("test-auth-token")
    )
    assert result.errors is None
    assert result.data is not None
    data = result.data
    assert "wikibaseList" in data
    wikibase_list = data["wikibaseList"]
    assert "data" in wikibase_list
    wikibase_list_data = wikibase_list["data"]

    found = [
        wikibase
        for wikibase in wikibase_list_data
        if wikibase["urls"]["baseUrl"] == "https://tcdict.wikibase.cloud"
    ]
    assert len(found) == 1
    for f in found:
        assert f['wikibaseType'] == 'CLOUD'
