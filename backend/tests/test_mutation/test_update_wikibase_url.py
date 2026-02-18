# pylint: disable=redefined-outer-name
"""Test Update Wikibase URLs"""

import pytest
import pytest_asyncio

from tests.test_schema import test_schema
from tests.utils import assert_layered_property_value, get_mock_context

WIKIBASE_URLS_QUERY = """query MyQuery($wikibaseId: Int!) {
  wikibase(wikibaseId: $wikibaseId) {
    id
    urls {
      articlePath
      baseUrl
      scriptPath
      sparqlEndpointUrl
      sparqlFrontendUrl
      specialStatisticsUrl
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

@pytest_asyncio.fixture(scope="function")
def get_wikibase_id_by_base_url():
    """Get the ID of a wikibase by its base URL"""
    async def _get_id(base_url):
        result = await test_schema.execute(
            """
            query {
              wikibaseList(pageNumber: 1, pageSize: 100) {
                data {
                  id
                  urls {
                    baseUrl
                  }
                }
              }
            }
            """
        )
        assert result.errors is None
        assert result.data is not None

        wikibases = result.data["wikibaseList"]["data"]

        for wikibase in wikibases:
            if wikibase["urls"]["baseUrl"] == base_url:
                return int(wikibase["id"])

        pytest.fail(f"No wikibase found with baseUrl: {base_url}")

    return _get_id


@pytest.mark.asyncio
@pytest.mark.mutation
@pytest.mark.dependency(
    name="add-wikibase-script-path", depends=["add-wikibase"], scope="session"
)
async def test_add_wikibase_script_path():
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
        expected_value="https://example.com",
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
        context_value=get_mock_context("test-auth-token"),
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
        expected_value="https://example.com",
    )
    assert_layered_property_value(
        after_adding_result.data,
        ["wikibase", "urls", "scriptPath"],
        expected_value="/w/",
    )


@pytest.mark.asyncio
@pytest.mark.mutation
@pytest.mark.dependency(
    name="remove-wikibase-sparql-frontend-url",
    depends=["add-wikibase"],
    scope="session",
)
async def test_remove_wikibase_sparql_frontend_url():
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
        expected_value="https://example.com",
    )
    assert_layered_property_value(
        before_removing_result.data,
        ["wikibase", "urls", "sparqlFrontendUrl"],
        expected_value="https://query.example.com",
    )

    remove_result = await test_schema.execute(
        REMOVE_WIKIBASE_URL_MUTATION,
        variable_values={
            "wikibaseId": 1,
            "urlType": "SPARQL_FRONTEND_URL",
        },
        context_value=get_mock_context("test-auth-token"),
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
        expected_value="https://example.com",
    )
    assert_layered_property_value(
        after_removing_result.data,
        ["wikibase", "urls", "sparqlFrontendUrl"],
        expected_value=None,
    )


@pytest.mark.asyncio
@pytest.mark.mutation
@pytest.mark.dependency(
    name="remove-wikibase-article-path",
    depends=["mutate-cloud-instances"],
    scope="session",
)
async def test_remove_wikibase_article_path(get_wikibase_id_by_base_url):
    """Remove Wikibase article path"""

    base_url = "https://biodiversity.wikibase.cloud"
    wikibase_id = await get_wikibase_id_by_base_url(base_url)

    before_removing_result = await test_schema.execute(
        WIKIBASE_URLS_QUERY, variable_values={"wikibaseId": wikibase_id}
    )
    assert before_removing_result.errors is None
    assert before_removing_result.data is not None

    assert_layered_property_value(
        before_removing_result.data,
        ["wikibase", "urls", "baseUrl"],
        expected_value=base_url,
    )
    assert_layered_property_value(
        before_removing_result.data,
        ["wikibase", "urls", "articlePath"],
        expected_value="/wiki",
    )
    assert_layered_property_value(
        before_removing_result.data,
        ["wikibase", "urls", "specialStatisticsUrl"],
        expected_value="https://biodiversity.wikibase.cloud/wiki/Special:Statistics",
    )

    remove_result = await test_schema.execute(
        REMOVE_WIKIBASE_URL_MUTATION,
        variable_values={
            "wikibaseId": wikibase_id,
            "urlType": "ARTICLE_PATH",
        },
        context_value=get_mock_context("test-auth-token"),
    )
    assert remove_result.errors is None
    assert remove_result.data is not None
    assert remove_result.data["removeWikibaseUrl"] is True

    after_removing_result = await test_schema.execute(
        WIKIBASE_URLS_QUERY, variable_values={"wikibaseId": wikibase_id}
    )
    assert after_removing_result.errors is None
    assert after_removing_result.data is not None
    assert_layered_property_value(
        after_removing_result.data, ["wikibase", "id"], expected_value=str(wikibase_id)
    )
    assert_layered_property_value(
        after_removing_result.data,
        ["wikibase", "urls", "baseUrl"],
        expected_value="https://biodiversity.wikibase.cloud",
    )
    assert_layered_property_value(
        after_removing_result.data,
        ["wikibase", "urls", "articlePath"],
        expected_value=None,
    )
    assert_layered_property_value(
        after_removing_result.data,
        ["wikibase", "urls", "specialStatisticsUrl"],
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
        expected_value="https://example.com",
    )
    assert_layered_property_value(
        before_updating_result.data,
        ["wikibase", "urls", "sparqlEndpointUrl"],
        expected_value="https://query.example.com/sparql-wrong",
    )

    update_result = await test_schema.execute(
        UPSERT_WIKIBASE_URL_MUTATION,
        variable_values={
            "wikibaseId": 1,
            "url": "https://query.example.com/sparql",
            "urlType": "SPARQL_ENDPOINT_URL",
        },
        context_value=get_mock_context("test-auth-token"),
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
        expected_value="https://example.com",
    )
    assert_layered_property_value(
        after_updating_result.data,
        ["wikibase", "urls", "sparqlEndpointUrl"],
        expected_value="https://query.example.com/sparql",
    )


@pytest.mark.asyncio
@pytest.mark.mutation
@pytest.mark.dependency(depends=["add-wikibase"], scope="session")
async def test_update_wikibase_article_path_fail():
    """Update Wikibase URL Fail"""

    update_result = await test_schema.execute(
        UPSERT_WIKIBASE_URL_MUTATION,
        variable_values={
            "wikibaseId": 1,
            "url": "https://example.com/wiki",
            "urlType": "ARTICLE_PATH",
        },
        context_value=get_mock_context("test-auth-token"),
    )
    assert update_result.errors is not None
    assert (
        update_result.errors[0].message
        == "WikibaseURLType.ARTICLE_PATH must not be full URL, https://example.com/wiki"
    )


@pytest.mark.asyncio
@pytest.mark.mutation
@pytest.mark.dependency(depends=["add-wikibase"], scope="session")
async def test_update_wikibase_base_url_fail():
    """Update Wikibase URL Fail"""

    update_result = await test_schema.execute(
        UPSERT_WIKIBASE_URL_MUTATION,
        variable_values={
            "wikibaseId": 1,
            "url": "localhost/wikibase",
            "urlType": "BASE_URL",
        },
        context_value=get_mock_context("test-auth-token"),
    )
    assert update_result.errors is not None
    assert (
        update_result.errors[0].message
        == "WikibaseURLType.BASE_URL must be full URL, localhost/wikibase"
    )
