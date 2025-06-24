"""Test Update Wikibase Type"""

import pytest

from tests.test_schema import test_schema
from tests.utils import assert_layered_property_value,get_mock_context

WIKIBASE_QUERY = """
query MyQuery($wikibaseId: Int!) {
  wikibase(wikibaseId: $wikibaseId) {
    id
    title
    wikibaseType
  }
}"""


UPDATE_WIKIBASE_TYPE_QUERY = """
mutation MyMutation($wikibaseId: Int!, $wikibaseType: WikibaseType!) {
  updateWikibaseType(wikibaseId: $wikibaseId, wikibaseType: $wikibaseType)
}"""


@pytest.mark.asyncio
@pytest.mark.mutation
@pytest.mark.dependency(
    name="update-wikibase-type",
    depends=["mutate-cloud-instances"],
    scope="session",
)
async def test_update_wikibase_type():
    """Test Update to Other"""

    before_updating_result = await test_schema.execute(
        WIKIBASE_QUERY,
        variable_values={"wikibaseId": 5},
        context_value=get_mock_context("test-auth-token"),
    )

    assert before_updating_result.errors is None
    assert before_updating_result.data is not None
    assert_layered_property_value(
        before_updating_result.data, ["wikibase", "wikibaseType"], "CLOUD"
    )

    update_result = await test_schema.execute(
        UPDATE_WIKIBASE_TYPE_QUERY,
        variable_values={"wikibaseId": 5, "wikibaseType": "OTHER"},
        context_value=get_mock_context("test-auth-token"),
    )
    assert update_result.errors is None
    assert update_result.data is not None
    assert update_result.data["updateWikibaseType"] is True

    after_updating_result = await test_schema.execute(
        WIKIBASE_QUERY,
        variable_values={"wikibaseId": 5},
        context_value=get_mock_context("test-auth-token"),
    )

    assert after_updating_result.errors is None
    assert after_updating_result.data is not None
    assert_layered_property_value(
        after_updating_result.data, ["wikibase", "wikibaseType"], "OTHER"
    )


@pytest.mark.asyncio
@pytest.mark.mutation
@pytest.mark.dependency(
    depends=["mutate-cloud-instances"],
    scope="session"
)
async def test_update_wikibase_type_to_same():
    """Test Update to Current Value"""

    before_updating_result = await test_schema.execute(
        WIKIBASE_QUERY,
        variable_values={"wikibaseId": 6},
        context_value=get_mock_context("test-auth-token"),
    )

    assert before_updating_result.errors is None
    assert before_updating_result.data is not None
    assert_layered_property_value(
        before_updating_result.data, ["wikibase", "wikibaseType"], "CLOUD"
    )

    update_result = await test_schema.execute(
        UPDATE_WIKIBASE_TYPE_QUERY,
        variable_values={"wikibaseId": 6, "wikibaseType": "CLOUD"},
        context_value=get_mock_context("test-auth-token"),
    )
    assert update_result.errors is None
    assert update_result.data is not None
    assert update_result.data["updateWikibaseType"] is True

    after_updating_result = await test_schema.execute(
        WIKIBASE_QUERY,
        variable_values={"wikibaseId": 6},
        context_value=get_mock_context("test-auth-token"),
    )

    assert after_updating_result.errors is None
    assert after_updating_result.data is not None
    assert_layered_property_value(
        after_updating_result.data, ["wikibase", "wikibaseType"], "CLOUD"
    )
