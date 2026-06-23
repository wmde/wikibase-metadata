# pylint: disable=redefined-outer-name
"""Test Update Wikibase URLs"""

import pytest
import pytest_asyncio

from data.database_connection import get_async_session
from model.database.wikibase_model import WikibaseModel
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
        result = await test_schema.execute("""
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
            """)
        assert result.errors is None
        assert result.data is not None

        wikibases = result.data["wikibaseList"]["data"]

        for wikibase in wikibases:
            if wikibase["urls"]["baseUrl"] == base_url:
                return int(wikibase["id"])

        pytest.fail(f"No wikibase found with baseUrl: {base_url}")

    return _get_id


@pytest.fixture
async def wikibase(db_session):  # pylint: disable=unused-argument
    """Create a test wikibase without a script path"""
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
async def test_add_wikibase_script_path(
    wikibase,
):  # pylint: disable=redefined-outer-name
    """Add Wikibase URL"""

    before_adding_result = await test_schema.execute(
        WIKIBASE_URLS_QUERY, variable_values={"wikibaseId": wikibase.id}
    )
    assert before_adding_result.errors is None
    assert before_adding_result.data is not None
    assert_layered_property_value(
        before_adding_result.data, ["wikibase", "id"], expected_value=str(wikibase.id)
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
            "wikibaseId": wikibase.id,
            "url": "/w/",
            "urlType": "SCRIPT_PATH",
        },
        context_value=get_mock_context("test-auth-token"),
    )
    assert add_result.errors is None
    assert add_result.data is not None
    assert add_result.data["upsertWikibaseUrl"] is True

    after_adding_result = await test_schema.execute(
        WIKIBASE_URLS_QUERY, variable_values={"wikibaseId": wikibase.id}
    )
    assert after_adding_result.errors is None
    assert after_adding_result.data is not None
    assert_layered_property_value(
        after_adding_result.data, ["wikibase", "id"], expected_value=str(wikibase.id)
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
async def test_remove_wikibase_sparql_frontend_url(
    wikibase,
    db_session,
):  # pylint: disable=unused-argument, redefined-outer-name
    """Remove Wikibase URL"""

    before_removing_result = await test_schema.execute(
        WIKIBASE_URLS_QUERY, variable_values={"wikibaseId": wikibase.id}
    )
    assert before_removing_result.errors is None
    assert before_removing_result.data is not None
    assert_layered_property_value(
        before_removing_result.data, ["wikibase", "id"], expected_value=str(wikibase.id)
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
            "wikibaseId": wikibase.id,
            "urlType": "SPARQL_FRONTEND_URL",
        },
        context_value=get_mock_context("test-auth-token"),
    )
    assert remove_result.errors is None
    assert remove_result.data is not None
    assert remove_result.data["removeWikibaseUrl"] is True

    after_removing_result = await test_schema.execute(
        WIKIBASE_URLS_QUERY, variable_values={"wikibaseId": wikibase.id}
    )
    assert after_removing_result.errors is None
    assert after_removing_result.data is not None
    assert_layered_property_value(
        after_removing_result.data, ["wikibase", "id"], expected_value=str(wikibase.id)
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
async def test_remove_wikibase_article_path(
    wikibase,
):  # pylint: disable=redefined-outer-name
    """Remove Wikibase article path"""

    before_removing_result = await test_schema.execute(
        WIKIBASE_URLS_QUERY, variable_values={"wikibaseId": wikibase.id}
    )
    assert before_removing_result.errors is None
    assert before_removing_result.data is not None

    assert_layered_property_value(
        before_removing_result.data,
        ["wikibase", "urls", "baseUrl"],
        expected_value="https://example.com",
    )
    assert_layered_property_value(
        before_removing_result.data,
        ["wikibase", "urls", "articlePath"],
        expected_value="/wiki",
    )
    assert_layered_property_value(
        before_removing_result.data,
        ["wikibase", "urls", "specialStatisticsUrl"],
        expected_value="https://example.com/wiki/Special:Statistics",
    )

    remove_result = await test_schema.execute(
        REMOVE_WIKIBASE_URL_MUTATION,
        variable_values={
            "wikibaseId": wikibase.id,
            "urlType": "ARTICLE_PATH",
        },
        context_value=get_mock_context("test-auth-token"),
    )
    assert remove_result.errors is None
    assert remove_result.data is not None
    assert remove_result.data["removeWikibaseUrl"] is True

    after_removing_result = await test_schema.execute(
        WIKIBASE_URLS_QUERY, variable_values={"wikibaseId": wikibase.id}
    )
    assert after_removing_result.errors is None
    assert after_removing_result.data is not None
    assert_layered_property_value(
        after_removing_result.data, ["wikibase", "id"], expected_value=str(wikibase.id)
    )
    assert_layered_property_value(
        after_removing_result.data,
        ["wikibase", "urls", "baseUrl"],
        expected_value="https://example.com",
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
async def test_update_wikibase_url(wikibase):  # pylint: disable=redefined-outer-name
    """Update Wikibase URL"""

    before_updating_result = await test_schema.execute(
        WIKIBASE_URLS_QUERY, variable_values={"wikibaseId": wikibase.id}
    )
    assert before_updating_result.errors is None
    assert before_updating_result.data is not None
    assert_layered_property_value(
        before_updating_result.data, ["wikibase", "id"], expected_value=str(wikibase.id)
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
            "wikibaseId": wikibase.id,
            "url": "https://query.example.com/sparql",
            "urlType": "SPARQL_ENDPOINT_URL",
        },
        context_value=get_mock_context("test-auth-token"),
    )
    assert update_result.errors is None
    assert update_result.data is not None
    assert update_result.data["upsertWikibaseUrl"] is True

    after_updating_result = await test_schema.execute(
        WIKIBASE_URLS_QUERY, variable_values={"wikibaseId": wikibase.id}
    )
    assert after_updating_result.errors is None
    assert after_updating_result.data is not None
    assert_layered_property_value(
        after_updating_result.data, ["wikibase", "id"], expected_value=str(wikibase.id)
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
async def test_update_wikibase_article_path_fail(
    wikibase,
):  # pylint: disable=redefined-outer-name
    """Update Wikibase URL Fail"""

    update_result = await test_schema.execute(
        UPSERT_WIKIBASE_URL_MUTATION,
        variable_values={
            "wikibaseId": wikibase.id,
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
async def test_update_wikibase_base_url_fail(
    wikibase,
):  # pylint: disable=redefined-outer-name
    """Update Wikibase URL Fail"""

    update_result = await test_schema.execute(
        UPSERT_WIKIBASE_URL_MUTATION,
        variable_values={
            "wikibaseId": wikibase.id,
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
