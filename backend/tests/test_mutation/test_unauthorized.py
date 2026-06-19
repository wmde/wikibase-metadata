"""
Testing whether running a mutation without valid authorization results in errors
"""

import pytest

from data.database_connection import get_async_session
from model.database.wikibase_model import WikibaseModel
from tests.test_schema import test_schema
from tests.utils import MockRequest

ADD_WIKIBASE_LANGUAGE_MUTATION = """
mutation MyMutation($wikibaseId: Int!) {
  addWikibaseLanguage(language: "French", wikibaseId: $wikibaseId)
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
async def test_wikibase_mutation_unauthorized(wikibase):
    """Test Query Wikibase Unauthorized"""

    result = await test_schema.execute(
        ADD_WIKIBASE_LANGUAGE_MUTATION,
        variable_values={"wikibaseId": wikibase.id},
        context_value={"request": MockRequest(headers={})},
    )

    assert result.errors is not None
    assert result.errors[0].message == "Authorization header missing"

    result = await test_schema.execute(
        ADD_WIKIBASE_LANGUAGE_MUTATION,
        variable_values={"wikibaseId": wikibase.id},
        context_value={
            "request": MockRequest(headers={"authorization": "wrong-header-value"})
        },
    )

    assert result.errors is not None
    assert result.errors[0].message == "Invalid authorization header, expected 'bearer'"

    result = await test_schema.execute(
        ADD_WIKIBASE_LANGUAGE_MUTATION,
        variable_values={"wikibaseId": wikibase.id},
        context_value={
            "request": MockRequest(
                headers={"authorization": "bearer: wrong token with spaces"}
            )
        },
    )

    assert result.errors is not None
    assert (
        result.errors[0].message
        == "Invalid authorization header, expected 'bearer <token>'"
    )

    result = await test_schema.execute(
        ADD_WIKIBASE_LANGUAGE_MUTATION,
        variable_values={"wikibaseId": wikibase.id},
        context_value={
            "request": MockRequest(headers={"authorization": "bearer: wrong-token"})
        },
    )

    assert result.errors is not None
    assert result.errors[0].message == "Authorization Failed"
