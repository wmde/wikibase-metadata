"""Test Wikibase Query"""

import pytest

from tests.test_schema import test_schema

WIKIBASE_QUERY = """
query MyQuery($wikibaseId: Int!) {
  wikibase(wikibaseId: $wikibaseId) {
    id
    title
  }
}"""


@pytest.mark.asyncio
@pytest.mark.query
async def test_wikibase_query_authorized(wikibase_fixture):
    """Test Query Wikibase Authorized"""

    result = await test_schema.execute(
        WIKIBASE_QUERY, variable_values={"wikibaseId": wikibase_fixture.id}
    )

    assert result.errors is None
    assert result.data is not None
