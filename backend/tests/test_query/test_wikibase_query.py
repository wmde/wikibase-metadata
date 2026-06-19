"""Test Wikibase Query"""

import pytest

from data.database_connection import get_async_session
from model.database.wikibase_model import WikibaseModel
from tests.test_schema import test_schema

WIKIBASE_QUERY = """
query MyQuery($wikibaseId: Int!) {
  wikibase(wikibaseId: $wikibaseId) {
    id
    title
  }
}"""

@pytest.fixture
async def wikibase(db_session):  # pylint: disable=unused-argument
    """Create a test wikibase"""
    async with get_async_session() as session:
        wikibase = WikibaseModel(
            wikibase_name="Test Wikibase",
            base_url="https://example.com",
            sparql_frontend_url="https://query.example.com",
            sparql_endpoint_url="https://query.example.com/sparql-wrong",
            article_path="/wiki",
        )
        wikibase.checked = True
        session.add(wikibase)
        await session.flush()
        return wikibase

@pytest.mark.asyncio
@pytest.mark.query
async def test_wikibase_query_authorized(wikibase):
    """Test Query Wikibase Authorized"""

    result = await test_schema.execute(
        WIKIBASE_QUERY, variable_values={"wikibaseId": wikibase.id}
    )

    assert result.errors is None
    assert result.data is not None
