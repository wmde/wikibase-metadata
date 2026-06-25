"""Test Wikibase Query"""

import pytest
from tests.test_schema import test_schema
from model.database import WikibaseModel
from data.database_connection import get_async_session

WIKIBASE_QUERY = """
query MyQuery($wikibaseId: Int!) {
  wikibase(wikibaseId: $wikibaseId) {
    id
    title
  }
}"""


@pytest.fixture
async def wikibase_fixture(db_session):  # pylint: disable=unused-argument
    """Create a test wikibase"""
    async with get_async_session() as session:
        wikibase = WikibaseModel(
            wikibase_name="Test Wikibase",
            base_url="https://wikibase-query-example.com",
        )
        session.add(wikibase)
        await session.flush()
        return wikibase


@pytest.mark.asyncio
@pytest.mark.query
async def test_wikibase_query_authorized(
    wikibase_fixture,
):  # pylint: disable=redefined-outer-name
    """Test Query Wikibase Authorized"""

    result = await test_schema.execute(
        WIKIBASE_QUERY, variable_values={"wikibaseId": wikibase_fixture.id}
    )

    assert result.errors is None
    assert result.data is not None
