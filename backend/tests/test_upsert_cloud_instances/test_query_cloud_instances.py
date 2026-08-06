"""Test Query Cloud Instances"""

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from model.enum import WikibaseType
from model.database import WikibaseModel
from tests.test_schema import test_schema
from tests.test_upsert_cloud_instances.constant import WIKIBASE_LIST_QUERY


@pytest.fixture
async def wikibase_fixture(db_session):
    """Create Wikibase Test Fixture"""

    async with AsyncSession(bind=db_session) as session:
        wikibase = WikibaseModel(
            wikibase_name="Test Wikibase",
            base_url="https://tcdict.wikibase.cloud",
            sparql_endpoint_url="https://tcdict.wikibase.cloud/sparql",
            reuse=True,
            wikibase_type=WikibaseType.CLOUD,
        )
        wikibase.checked = True
        session.add(wikibase)
        await session.flush()
        return wikibase


@pytest.mark.asyncio
async def test_query_cloud_instance(
    wikibase_fixture,
):  # pylint: disable=unused-argument,redefined-outer-name
    """
    test whether querying the wikibase list via graphql returns a cloud instance
    """
    result = await test_schema.execute(WIKIBASE_LIST_QUERY)
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
        assert f["wikibaseType"] == "CLOUD"
