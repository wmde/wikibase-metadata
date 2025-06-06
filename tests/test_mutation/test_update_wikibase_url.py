"""Test Update Wikibase URLs"""

import pytest

from tests.test_schema import test_schema
from tests.utils.assert_property_value import assert_layered_property_value


WIKIBASE_URLS_QUERY = """query MyQuery($wikibaseId: Int!) {
  wikibase(wikibaseId: $wikibaseId) {
    id
    urls {
      articlePath
      baseUrl
      scriptPath
      sparqlEndpointUrl
      sparqlFrontendUrl
    }
  }
}"""

UPSERT_WIKIBASE_URL_MUTATION = """
mutation MyMutation($url: String!, $urlType: WikibaseURLType!, $wikibaseId: Int!) {
  upsertWikibaseUrl(url: $url, urlType: $urlType, wikibaseId: $wikibaseId)
}"""

REMOVE_WIKIBASE_URL_MUTATION = """
mutation MyMutation($urlType: WikibaseURLType!, $wikibaseId: Int!) {
  removeWikibaseUrl(urlType: $urlType, wikibaseId: $wikibaseId)
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
        expected_value="https://example.com/",
    )
    assert_layered_property_value(
        before_adding_result.data,
        ["wikibase", "urls", "scriptPath"],
        expected_value=None,
    )

    add_result = await test_schema.execute(
        UPSERT_WIKIBASE_URL_MUTATION,
        variable_values={
            "wikibaseId": 1,
            "url": "/w/",
            "urlType": "SCRIPT_PATH",
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
        expected_value="https://example.com/",
    )
    assert_layered_property_value(
        after_adding_result.data,
        ["wikibase", "urls", "scriptPath"],
        expected_value="/w/",
    )


@pytest.mark.asyncio
@pytest.mark.mutation
@pytest.mark.dependency(
    name="remove-wikibase-url", depends=["add-wikibase"], scope="session"
)
async def test_remove_wikibase_url():
    """Remove Wikibase URL"""

    before_removing_result = await test_schema.execute(
        WIKIBASE_URLS_QUERY, variable_values={"wikibaseId": 1}
    )
    assert before_removing_result.errors is None
    assert before_removing_result.data is not None
    assert_layered_property_value(
        before_removing_result.data, ["wikibase", "id"], expected_value="1"
    )
    assert_layered_property_value(
        before_removing_result.data,
        ["wikibase", "urls", "baseUrl"],
        expected_value="https://example.com/",
    )
    assert_layered_property_value(
        before_removing_result.data,
        ["wikibase", "urls", "sparqlFrontendUrl"],
        expected_value="query.example.com",
    )

    remove_result = await test_schema.execute(
        REMOVE_WIKIBASE_URL_MUTATION,
        variable_values={
            "wikibaseId": 1,
            "urlType": "SPARQL_FRONTEND_URL",
        },
    )
    assert remove_result.errors is None
    assert remove_result.data is not None
    assert remove_result.data["removeWikibaseUrl"] is True

    after_removing_result = await test_schema.execute(
        WIKIBASE_URLS_QUERY, variable_values={"wikibaseId": 1}
    )
    assert after_removing_result.errors is None
    assert after_removing_result.data is not None
    assert_layered_property_value(
        after_removing_result.data, ["wikibase", "id"], expected_value="1"
    )
    assert_layered_property_value(
        after_removing_result.data,
        ["wikibase", "urls", "baseUrl"],
        expected_value="https://example.com/",
    )
    assert_layered_property_value(
        after_removing_result.data,
        ["wikibase", "urls", "sparqlFrontendUrl"],
        expected_value=None,
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
        expected_value="https://example.com/",
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
        expected_value="https://example.com/",
    )
    assert_layered_property_value(
        after_updating_result.data,
        ["wikibase", "urls", "sparqlEndpointUrl"],
        expected_value="https://query.example.com/sparql",
    )
