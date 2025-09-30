"""
Testing whether running a mutation without valid authorization results in errors
"""

import pytest

from tests.test_schema import test_schema
from tests.utils import MockRequest


ADD_WIKIBASE_LANGUAGE_MUTATION = """
mutation MyMutation($wikibaseId: Int!) {
  addWikibaseLanguage(language: "French", wikibaseId: $wikibaseId)
}"""


@pytest.mark.asyncio
@pytest.mark.query
@pytest.mark.dependency(depends=["add-wikibase"], scope="session")
async def test_wikibase_mutation_unauthorized():
    """Test Query Wikibase Unauthorized"""

    result = await test_schema.execute(
        ADD_WIKIBASE_LANGUAGE_MUTATION,
        variable_values={"wikibaseId": 1},
        context_value={"request": MockRequest(headers={})},
    )

    assert result.errors is not None
    assert result.errors[0].message == "Authorization header missing"

    result = await test_schema.execute(
        ADD_WIKIBASE_LANGUAGE_MUTATION,
        variable_values={"wikibaseId": 1},
        context_value={
            "request": MockRequest(headers={"authorization": "wrong-header-value"})
        },
    )

    assert result.errors is not None
    assert result.errors[0].message == "Invalid authorization header, expected 'bearer'"

    result = await test_schema.execute(
        ADD_WIKIBASE_LANGUAGE_MUTATION,
        variable_values={"wikibaseId": 1},
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
        variable_values={"wikibaseId": 1},
        context_value={
            "request": MockRequest(headers={"authorization": "bearer: wrong-token"})
        },
    )

    assert result.errors is not None
    assert result.errors[0].message == "Authorization Failed"
