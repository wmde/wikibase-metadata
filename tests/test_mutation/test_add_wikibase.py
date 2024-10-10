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
@pytest.mark.dependency(name="add-wikibase")
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
                    "baseUrl": "example.com",
                    "actionApiUrl": "example.com/w/api.php",
                    "indexApiUrl": "example.com/w/index.php",
                    "sparqlEndpointUrl": "query.example.com/sparql",
                    "sparqlQueryUrl": "query.example.com",
                    "specialStatisticsUrl": "example.com/wiki/Special:Statistics",
                    "specialVersionUrl": "example.com/wiki/Special:Version",
                },
            }
        },
    )

    assert result.errors is None
    assert result.data is not None
    assert_layered_property_value(result.data, ["addWikibase", "id"], "1")
