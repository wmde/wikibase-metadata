# pylint: disable=redefined-outer-name
"""Test Update Wikibase Type"""

import pytest

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


@pytest.mark.asyncio
async def test_update_wikibase_type(wikibase_fixture):
    """Test Update to Other"""

    for wikibase_type in ["OTHER", "UNKNOWN", "SUITE", "TEST"]:
        before_updating_result = await test_schema.execute(
            WIKIBASE_QUERY, variable_values={"wikibaseId": wikibase_fixture.id}
        )

        assert before_updating_result.errors is None
        assert before_updating_result.data is not None
        assert before_updating_result.data["wikibase"]["wikibaseType"] != wikibase_type

        update_result = await test_schema.execute(
            UPDATE_WIKIBASE_TYPE_MUTATION,
            variable_values={"wikibaseId": wikibase_fixture.id, "wikibaseType": wikibase_type},
            context_value=get_mock_context("test-auth-token"),
        )
        
        assert update_result.errors is None
        assert update_result.data is not None
        assert update_result.data["updateWikibaseType"] is True

        after_updating_result = await test_schema.execute(
            WIKIBASE_QUERY, variable_values={"wikibaseId": wikibase_fixture.id}
        )

        assert after_updating_result.errors is None
        assert after_updating_result.data is not None
        assert after_updating_result.data["wikibase"]["wikibaseType"] == wikibase_type 


@pytest.mark.asyncio
async def test_update_wikibase_type_to_same(wikibase_fixture):
    """Test Update to Current Value"""


    before_updating_result = await test_schema.execute(
        WIKIBASE_QUERY, variable_values={"wikibaseId": wikibase_fixture.id}
    )

    assert before_updating_result.errors is None
    assert before_updating_result.data is not None

    assert_layered_property_value(
        before_updating_result.data, ["wikibase", "wikibaseType"], "CLOUD"
    )

    update_result = await test_schema.execute(
        UPDATE_WIKIBASE_TYPE_MUTATION,
        variable_values={"wikibaseId": wikibase_fixture.id, "wikibaseType": "CLOUD"},
        context_value=get_mock_context("test-auth-token"),
    )
    assert update_result.errors is None
    assert update_result.data is not None
    assert update_result.data["updateWikibaseType"] is True

    after_updating_result = await test_schema.execute(
        WIKIBASE_QUERY, variable_values={"wikibaseId": wikibase_fixture.id}
    )

    assert after_updating_result.errors is None
    assert after_updating_result.data is not None
    assert_layered_property_value(
        after_updating_result.data, ["wikibase", "wikibaseType"], "CLOUD"
    )
