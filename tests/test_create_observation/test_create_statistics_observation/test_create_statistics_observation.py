"""Test create_special_statistics_observation"""

import os
import time
from urllib.error import HTTPError
import pytest
from fetch_data import create_special_statistics_observation
from tests.test_schema import test_schema
from tests.utils import get_mock_context, MockResponse


FETCH_STATISTICS_MUTATION = """mutation MyMutation($wikibaseId: Int!) {
  fetchStatisticsData(wikibaseId: $wikibaseId)
}"""


DATA_DIRECTORY = "tests/test_create_observation/test_create_statistics_observation/data"


@pytest.mark.asyncio
@pytest.mark.dependency(
    name="statistics-success", depends=["statistics-fail-ood"], scope="session"
)
@pytest.mark.mutation
@pytest.mark.soup
@pytest.mark.statistics
async def test_create_statistics_observation_success(mocker):
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
        variable_values={"wikibaseId": 1},
        context_value=get_mock_context("test-auth-token"),
    )

    assert result.errors is None
    assert result.data is not None
    assert result.data["fetchStatisticsData"]


@pytest.mark.asyncio
@pytest.mark.dependency(
    name="statistics-failure", depends=["statistics-success"], scope="session"
)
@pytest.mark.soup
@pytest.mark.statistics
async def test_create_statistics_observation_failure(mocker):
    """Test Failure Scenario"""

    time.sleep(1)

    mocker.patch(
        "fetch_data.soup_data.create_statistics_data_observation.requests.get",
        side_effect=[MockResponse("", 500)],
    )
    success = await create_special_statistics_observation(1)
    assert success is False
