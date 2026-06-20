"""Test create_special_statistics_observation"""

import os
import time
import pytest
from data.database_connection import get_async_session
from model.database.wikibase_model import WikibaseModel
from fetch_data import create_special_statistics_observation
from tests.test_schema import test_schema
from tests.utils import get_mock_context, MockResponse

FETCH_STATISTICS_MUTATION = """mutation MyMutation($wikibaseId: Int!) {
  fetchStatisticsData(wikibaseId: $wikibaseId)
}"""


DATA_DIRECTORY = "tests/test_create_observation/statistics/data"


@pytest.fixture
async def wikibase_with_article_path_stats(db_session): # pylint: disable=unused-argument
    """Create a wikibase with article path for statistics tests"""
    async with get_async_session() as session:
        wikibase = WikibaseModel(
            wikibase_name="Statistics Test Wikibase",
            base_url="https://statistics-test-example.com",
            article_path="/wiki",
        )
        wikibase.checked = True
        wikibase.reuse = True
        wikibase.test = False
        wikibase.wikibase_type = None
        session.add(wikibase)
        await session.flush()
        await session.refresh(wikibase)
        wikibase_id = wikibase.id
    return wikibase_id


@pytest.mark.asyncio
@pytest.mark.soup
@pytest.mark.statistics
async def test_create_statistics_observation_success(
    wikibase_with_article_path_stats, mocker
):
    """Test Data Returned Scenario"""

    with open(
        os.path.join(DATA_DIRECTORY, "Special_Statistics.html"), "rb"
    ) as version_html:

        mocker.patch(
            "fetch_data.soup_data.create_statistics_data_observation.requests.get",
            side_effect=[MockResponse("", 200, version_html.read())],
        )

    result = await test_schema.execute(
        FETCH_STATISTICS_MUTATION,
        variable_values={"wikibaseId": wikibase_with_article_path_stats},
        context_value=get_mock_context("test-auth-token"),
    )

    assert result.errors is None
    assert result.data is not None
    assert result.data["fetchStatisticsData"]


@pytest.mark.asyncio
@pytest.mark.soup
@pytest.mark.statistics
async def test_create_statistics_observation_failure(
    wikibase_with_article_path_stats, mocker
):
    """Test Failure Scenario"""

    time.sleep(1)

    mocker.patch(
        "fetch_data.soup_data.create_statistics_data_observation.requests.get",
        side_effect=[MockResponse("", 500)],
    )
    success = await create_special_statistics_observation(
        wikibase_with_article_path_stats
    )
    assert success is False
