"""Test Update Missing Script Paths"""

import pytest

from data import get_async_session
from model.database import WikibaseModel
from resolvers import update_missing_script_paths
from tests.test_schema import test_schema
from tests.test_update_missing_urls.constant import DATA_DIRECTORY, WIKIBASE_URLS_QUERY
from tests.utils import MockResponse, assert_layered_property_value


@pytest.fixture
async def wikibase(db_session):  # pylint: disable=unused-argument
    """Create a wikibase with article path for software version tests"""
    async with get_async_session() as session:
        test_wikibase = WikibaseModel(
            wikibase_name="Software Version Test Wikibase",
            base_url="https://example.com",
            article_path="/wiki",
        )
        test_wikibase.checked = True
        test_wikibase.reuse = True
        test_wikibase.test = False
        session.add(test_wikibase)
        await session.flush()
        await session.refresh(test_wikibase)
        wikibase_id = test_wikibase.id
    return wikibase_id


@pytest.mark.asyncio
async def test_update_missing_script_paths(
    wikibase, mocker
):  # pylint: disable=redefined-outer-name
    """Test update_missing_script_paths"""

    with open(f"{DATA_DIRECTORY}/Special_Version.html", mode="rb") as data:
        mocker.patch("requests.get", side_effect=[MockResponse("", 200, data.read())])

    before_adding_result = await test_schema.execute(
        WIKIBASE_URLS_QUERY, variable_values={"wikibaseId": wikibase}
    )
    assert before_adding_result.errors is None
    assert before_adding_result.data is not None
    assert_layered_property_value(
        before_adding_result.data, ["wikibase", "id"], expected_value=str(wikibase)
    )
    assert_layered_property_value(
        before_adding_result.data,
        ["wikibase", "urls", "scriptPath"],
        expected_value=None,
    )

    result = await update_missing_script_paths()
    assert result == 1

    after_adding_result = await test_schema.execute(
        WIKIBASE_URLS_QUERY, variable_values={"wikibaseId": wikibase}
    )
    assert after_adding_result.errors is None
    assert after_adding_result.data is not None
    assert_layered_property_value(
        after_adding_result.data, ["wikibase", "id"], expected_value=str(wikibase)
    )
    assert_layered_property_value(
        after_adding_result.data,
        ["wikibase", "urls", "scriptPath"],
        expected_value="/mockwiki",
    )
