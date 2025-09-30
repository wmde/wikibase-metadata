"""Test Update Missing SPARQL Urls"""

import pytest

from resolvers.update import update_missing_sparql_urls
from tests.test_schema import test_schema
from tests.test_update_missing_urls.constant import DATA_DIRECTORY, WIKIBASE_URLS_QUERY
from tests.utils import MockResponse, assert_layered_property_value, get_mock_context


@pytest.mark.asyncio
@pytest.mark.dependency(
    name="update-missing-wikibase-sparql",
    depends=[
        "add-wikibase-ii",
        "update-missing-wikibase-script-path",
        "software-version-success-ii",
    ],
    scope="session",
)
async def test_update_missing_sparql_urls(mocker):
    """Test update_missing_sparql_urls"""

    with open(f"{DATA_DIRECTORY}/manifest.json", mode="rb") as data:
        mocker.patch("requests.get", side_effect=[MockResponse("", 200, data.read())])

    before_adding_result = await test_schema.execute(
        WIKIBASE_URLS_QUERY, variable_values={"wikibaseId": 2}
    )
    assert before_adding_result.errors is None
    assert before_adding_result.data is not None
    assert_layered_property_value(
        before_adding_result.data, ["wikibase", "id"], expected_value="2"
    )
    assert_layered_property_value(
        before_adding_result.data,
        ["wikibase", "urls", "scriptPath"],
        expected_value="/mockwiki",
    )
    assert_layered_property_value(
        before_adding_result.data,
        ["wikibase", "urls", "sparqlEndpointUrl"],
        expected_value=None,
    )
    assert_layered_property_value(
        before_adding_result.data,
        ["wikibase", "urls", "sparqlFrontendUrl"],
        expected_value=None,
    )

    result = await update_missing_sparql_urls()
    assert result == 1

    after_adding_result = await test_schema.execute(
        WIKIBASE_URLS_QUERY, variable_values={"wikibaseId": 2}
    )
    assert after_adding_result.errors is None
    assert after_adding_result.data is not None
    assert_layered_property_value(
        after_adding_result.data, ["wikibase", "id"], expected_value="2"
    )
    assert_layered_property_value(
        after_adding_result.data,
        ["wikibase", "urls", "sparqlEndpointUrl"],
        expected_value="https://mock-wikibase.com/query/sparql",
    )
    assert_layered_property_value(
        after_adding_result.data,
        ["wikibase", "urls", "sparqlFrontendUrl"],
        expected_value="https://mock-wikibase.com/query",
    )
