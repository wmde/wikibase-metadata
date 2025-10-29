"""Test Update Missing Script Paths"""

import pytest

from resolvers.update import update_missing_script_paths
from tests.test_schema import test_schema
from tests.test_update_missing_urls.constant import DATA_DIRECTORY, WIKIBASE_URLS_QUERY
from tests.utils import MockResponse
from tests.utils.assert_property_value import assert_layered_property_value


@pytest.mark.asyncio
@pytest.mark.dependency(
    name="update-missing-wikibase-script-path",
    depends=["add-wikibase-ii"],
    scope="session",
)
async def test_update_missing_script_paths(mocker):
    """Test update_missing_script_paths"""

    with open(f"{DATA_DIRECTORY}/Special_Version.html", mode="rb") as data:
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
        expected_value=None,
    )

    result = await update_missing_script_paths()
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
        ["wikibase", "urls", "scriptPath"],
        expected_value="/mockwiki",
    )
