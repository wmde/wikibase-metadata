# pylint: disable=redefined-outer-name
"""Test Update Wikibase Type"""

import pytest
import pytest_asyncio

from data.database_connection import get_async_session
from model.database.wikibase_model import WikibaseModel
from model.enum.wikibase_type_enum import WikibaseType
from tests.test_schema import test_schema
from tests.utils import assert_layered_property_value, get_mock_context

WIKIBASE_QUERY = """
query MyQuery($wikibaseId: Int!) {
  wikibase(wikibaseId: $wikibaseId) {
    id
    title
    wikibaseType
  }
}"""


UPDATE_WIKIBASE_TYPE_MUTATION = """
mutation MyMutation($wikibaseId: Int!, $wikibaseType: WikibaseType!) {
  updateWikibaseType(wikibaseId: $wikibaseId, wikibaseType: $wikibaseType)
}"""


@pytest_asyncio.fixture(scope="function")
def get_test_wikibase_id():
    """Get the ID of a wikibase that exists in the DB, optionally filtered by type"""

    async def _get_id(wikibase_type=None):
        result = await test_schema.execute("""
            query {
              wikibaseList(pageNumber: 1, pageSize: 100) {
                data {
                  id
                  wikibaseType
                }
              }
            }
            """)
        assert result.errors is None
        assert result.data is not None

        wikibases = result.data["wikibaseList"]["data"]

        if wikibase_type:
            for wikibase in wikibases:
                if wikibase["wikibaseType"] == wikibase_type:
                    return int(wikibase["id"])
            pytest.fail(f"No wikibase found with type: {wikibase_type}")

        return int(wikibases[0]["id"])

    return _get_id

@pytest.fixture
async def wikibase(db_session):
    """Create a wikibase with article path for software version tests"""
    async with get_async_session() as session:
        wikibase = WikibaseModel(
            wikibase_name="Software Version Test Wikibase",
            base_url="https://example.com",
            article_path="/wiki",
        )
        wikibase.checked = True
        wikibase.reuse = True
        wikibase.test = False
        wikibase.wikibase_type = WikibaseType["CLOUD"]
        session.add(wikibase)
        await session.flush()
        await session.refresh(wikibase)
        return wikibase

@pytest.mark.asyncio
async def test_update_wikibase_type(wikibase):
    """Test Update to Other"""

    wikibase_id = wikibase.id
    
    for wikibase_type in ["OTHER", "UNKNOWN", "SUITE", "TEST"]:
        before_updating_result = await test_schema.execute(
            WIKIBASE_QUERY, variable_values={"wikibaseId": wikibase_id}
        )

        assert before_updating_result.errors is None
        assert before_updating_result.data is not None
        assert before_updating_result.data["wikibase"]["wikibaseType"] != wikibase_type

        update_result = await test_schema.execute(
            UPDATE_WIKIBASE_TYPE_MUTATION,
            variable_values={"wikibaseId": wikibase_id, "wikibaseType": wikibase_type},
            context_value=get_mock_context("test-auth-token"),
        )
        
        assert update_result.errors is None
        assert update_result.data is not None
        assert update_result.data["updateWikibaseType"] is True

        after_updating_result = await test_schema.execute(
            WIKIBASE_QUERY, variable_values={"wikibaseId": wikibase_id}
        )

        assert after_updating_result.errors is None
        assert after_updating_result.data is not None
        assert after_updating_result.data["wikibase"]["wikibaseType"] == wikibase_type 


@pytest.mark.asyncio
async def test_update_wikibase_type_to_same(wikibase):
    """Test Update to Current Value"""

    # wikibase_id = await get_test_wikibase_id("CLOUD")
    wikibase_id = wikibase.id

    before_updating_result = await test_schema.execute(
        WIKIBASE_QUERY, variable_values={"wikibaseId": wikibase_id}
    )

    assert before_updating_result.errors is None
    assert before_updating_result.data is not None

    assert_layered_property_value(
        before_updating_result.data, ["wikibase", "wikibaseType"], "CLOUD"
    )

    update_result = await test_schema.execute(
        UPDATE_WIKIBASE_TYPE_MUTATION,
        variable_values={"wikibaseId": wikibase_id, "wikibaseType": "CLOUD"},
        context_value=get_mock_context("test-auth-token"),
    )
    assert update_result.errors is None
    assert update_result.data is not None
    assert update_result.data["updateWikibaseType"] is True

    after_updating_result = await test_schema.execute(
        WIKIBASE_QUERY, variable_values={"wikibaseId": wikibase_id}
    )

    assert after_updating_result.errors is None
    assert after_updating_result.data is not None
    assert_layered_property_value(
        after_updating_result.data, ["wikibase", "wikibaseType"], "CLOUD"
    )
