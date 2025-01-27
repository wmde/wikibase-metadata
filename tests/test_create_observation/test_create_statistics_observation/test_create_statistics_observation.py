"""Test create_special_statistics_observation"""

import os
import time
from urllib.error import HTTPError
import pytest
from fetch_data import create_special_statistics_observation
from tests.utils import MockResponse


DATA_DIRECTORY = "tests/test_create_observation/test_create_statistics_observation/data"


@pytest.mark.asyncio
@pytest.mark.dependency(
    name="statistics-success", depends=["statistics-fail-ood"], scope="session"
)
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
        success = await create_special_statistics_observation(1)
        assert success


@pytest.mark.asyncio
@pytest.mark.dependency(
    name="statistics-failure-500", depends=["statistics-success"], scope="session"
)
@pytest.mark.soup
@pytest.mark.statistics
async def test_create_statistics_observation_fail_500(mocker):
    """Test Failure Scenario"""

    time.sleep(1)

    mocker.patch(
        "fetch_data.soup_data.create_statistics_data_observation.requests.get",
        side_effect=[
            HTTPError(
                url="example.com/wiki/Special:Statistics",
                code=500,
                msg="Error",
                hdrs="",
                fp=None,
            )
        ],
    )
    success = await create_special_statistics_observation(1)
    assert success is False


@pytest.mark.asyncio
@pytest.mark.dependency(
    name="statistics-failure-not-found",
    depends=["statistics-success", "statistics-failure-500"],
    scope="session",
)
@pytest.mark.soup
@pytest.mark.statistics
async def test_create_statistics_observation_fail_not_found(mocker):
    """Test Failure Scenario"""

    time.sleep(1)

    with open(
        os.path.join(DATA_DIRECTORY, "Special_Statistics_fail.html"), "rb"
    ) as version_html:

        mocker.patch(
            "fetch_data.soup_data.create_statistics_data_observation.requests.get",
            side_effect=[MockResponse("", 200, version_html.read())],
        )
        success = await create_special_statistics_observation(1)
        assert success
