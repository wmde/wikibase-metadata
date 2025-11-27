"""Test Add Wikibase"""

import pytest
from tests.test_schema import test_schema
from tests.utils import assert_layered_property_value


ADD_WIKIBASE_QUERY = """
mutation MyMutation($wikibaseInput: WikibaseInput!) {
  addWikibase(wikibaseInput: $wikibaseInput) {
    id
  }
}"""


@pytest.mark.asyncio
@pytest.mark.mutation
@pytest.mark.dependency(
    name="add-wikibase", depends=["add-test-categories"], scope="session"
)
async def test_add_wikibase_mutation():
    """Test Add Wikibase"""

    result = await test_schema.execute(
        ADD_WIKIBASE_QUERY,
        variable_values={
            "wikibaseInput": {
                "wikibaseName": "Mock Wikibase",
                "description": "Mock wikibase for testing this codebase",
                "organization": "Wikibase Mockery International",
                "country": "Germany",
                "region": "Europe",
                "category": "EXPERIMENTAL_AND_PROTOTYPE_PROJECTS",
                "urls": {
                    "baseUrl": "https://example.com/",
                    "articlePath": "/wiki",
                    # "scriptPath": "/w",  # will be set in add-wikibase-script-path test
                    "sparqlEndpointUrl": "https://query.example.com/sparql-wrong",
                    "sparqlFrontendUrl": "https://query.example.com",
                },
            }
        },
    )

    assert result.errors is None
    assert result.data is not None
    assert_layered_property_value(result.data, ["addWikibase", "id"], "1")


@pytest.mark.asyncio
@pytest.mark.mutation
@pytest.mark.dependency(name="add-wikibase-ii", depends=["add-wikibase"])
async def test_add_wikibase_ii_mutation():
    """Test Add Another Wikibase"""

    result = await test_schema.execute(
        ADD_WIKIBASE_QUERY,
        variable_values={
            "wikibaseInput": {
                "wikibaseName": "Mock Wikibase II",
                "description": "Another Mock wikibase for testing this codebase",
                "organization": "Wikibase Mockery International",
                "country": "Germany",
                "region": "Europe",
                "category": "EXPERIMENTAL_AND_PROTOTYPE_PROJECTS",
                "urls": {
                    "baseUrl": "https://mock-wikibase.com/",
                    "articlePath": "wiki",
                },
            }
        },
    )

    assert result.errors is None
    assert result.data is not None
    assert_layered_property_value(result.data, ["addWikibase", "id"], "2")
