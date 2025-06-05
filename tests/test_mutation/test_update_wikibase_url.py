"""Test Update Wikibase URLs"""

import pytest

from tests.test_schema import test_schema
from tests.utils.assert_property_value import assert_layered_property_value


WIKIBASE_URLS_QUERY = """query MyQuery($wikibaseId: Int!) {
  wikibase(wikibaseId: $wikibaseId) {
    id
    urls {
      actionApi
      baseUrl
      indexApi
      sparqlEndpointUrl
      sparqlUrl
      specialStatisticsUrl
      specialVersionUrl
    }
  }
}"""

UPSERT_WIKIBASE_URL_MUTATION = """
mutation MyMutation($url: String!, $urlType: WikibaseURLType!, $wikibaseId: Int!) {
  upsertWikibaseUrl(url: $url, urlType: $urlType, wikibaseId: $wikibaseId)
}"""


@pytest.mark.asyncio
@pytest.mark.mutation
@pytest.mark.dependency(
    name="add-wikibase-url", depends=["add-wikibase"], scope="session"
)
async def test_add_wikibase_url():
    """Add Wikibase URL"""

    before_adding_result = await test_schema.execute(
        WIKIBASE_URLS_QUERY, variable_values={"wikibaseId": 1}
    )
    assert before_adding_result.errors is None
    assert before_adding_result.data is not None
    assert_layered_property_value(
        before_adding_result.data, ["wikibase", "id"], expected_value="1"
    )
    assert_layered_property_value(
        before_adding_result.data,
        ["wikibase", "urls", "baseUrl"],
        expected_value="example.com",
    )
    assert_layered_property_value(
        before_adding_result.data,
        ["wikibase", "urls", "actionApi"],
        expected_value=None,
    )

    add_result = await test_schema.execute(
        UPSERT_WIKIBASE_URL_MUTATION,
        variable_values={
            "wikibaseId": 1,
            "url": "https://example.com/w/api.php",
            "urlType": "ACTION_QUERY_URL",
        },
    )
    assert add_result.errors is None
    assert add_result.data is not None
    assert add_result.data["upsertWikibaseUrl"] is True

    after_adding_result = await test_schema.execute(
        WIKIBASE_URLS_QUERY, variable_values={"wikibaseId": 1}
    )
    assert after_adding_result.errors is None
    assert after_adding_result.data is not None
    assert_layered_property_value(
        after_adding_result.data, ["wikibase", "id"], expected_value="1"
    )
    assert_layered_property_value(
        after_adding_result.data,
        ["wikibase", "urls", "baseUrl"],
        expected_value="example.com",
    )
    assert_layered_property_value(
        after_adding_result.data,
        ["wikibase", "urls", "actionApi"],
        expected_value="https://example.com/w/api.php",
    )


@pytest.mark.asyncio
@pytest.mark.mutation
@pytest.mark.dependency(
    name="update-wikibase-url", depends=["add-wikibase"], scope="session"
)
async def test_update_wikibase_url():
    """Update Wikibase URL"""

    before_updating_result = await test_schema.execute(
        WIKIBASE_URLS_QUERY, variable_values={"wikibaseId": 1}
    )
    assert before_updating_result.errors is None
    assert before_updating_result.data is not None
    assert_layered_property_value(
        before_updating_result.data, ["wikibase", "id"], expected_value="1"
    )
    assert_layered_property_value(
        before_updating_result.data,
        ["wikibase", "urls", "baseUrl"],
        expected_value="example.com",
    )
    assert_layered_property_value(
        before_updating_result.data,
        ["wikibase", "urls", "sparqlEndpointUrl"],
        expected_value="query.example.com/sparql-wrong",
    )

    update_result = await test_schema.execute(
        UPSERT_WIKIBASE_URL_MUTATION,
        variable_values={
            "wikibaseId": 1,
            "url": "https://query.example.com/sparql",
            "urlType": "SPARQL_ENDPOINT_URL",
        },
    )
    assert update_result.errors is None
    assert update_result.data is not None
    assert update_result.data["upsertWikibaseUrl"] is True

    after_updating_result = await test_schema.execute(
        WIKIBASE_URLS_QUERY, variable_values={"wikibaseId": 1}
    )
    assert after_updating_result.errors is None
    assert after_updating_result.data is not None
    assert_layered_property_value(
        after_updating_result.data, ["wikibase", "id"], expected_value="1"
    )
    assert_layered_property_value(
        after_updating_result.data,
        ["wikibase", "urls", "baseUrl"],
        expected_value="example.com",
    )
    assert_layered_property_value(
        after_updating_result.data,
        ["wikibase", "urls", "sparqlEndpointUrl"],
        expected_value="https://query.example.com/sparql",
    )
