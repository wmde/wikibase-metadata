"""Test Wikibase Query"""

import pytest

from tests.test_schema import test_schema
from tests.utils.test_request import TestRequest


WIKIBASE_QUERY = """
query MyQuery($wikibaseId: Int!) {
  wikibase(wikibaseId: $wikibaseId) {
    id
    title
  }
}"""


@pytest.mark.asyncio
@pytest.mark.query
@pytest.mark.dependency(depends=["add-wikibase"], scope="session")
async def test_wikibase_query_unauthorized():
    """Test Query Wikibase Unauthorized"""

    result = await test_schema.execute(
        WIKIBASE_QUERY,
        variable_values={"wikibaseId": 1},
        context_value={
            "request": TestRequest(headers={"authorization": "unauthorized"})
        },
    )

    assert result.errors is not None
    assert result.errors[0].message == "Authorisation Failed"


@pytest.mark.asyncio
@pytest.mark.query
@pytest.mark.dependency(depends=["add-wikibase"], scope="session")
async def test_wikibase_query_authorized():
    """Test Query Wikibase Authorized"""

    result = await test_schema.execute(
        WIKIBASE_QUERY,
        variable_values={"wikibaseId": 1},
        context_value={
            "request": TestRequest(headers={"authorization": "test-auth-token"})
        },
    )

    assert result.errors is None
    assert result.data is not None
