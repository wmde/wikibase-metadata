"""Test create_property_popularity_observation"""

import os
from urllib.error import HTTPError
import pytest
from fetch_data import create_software_version_observation
from tests.utils import MockResponse


DATA_DIRECTORY = "tests/test_create_observation/test_create_software_version_observation/data"


@pytest.mark.asyncio
@pytest.mark.version
async def test_create_software_version_observation_success(mocker):
    """Test One-Pull Per Month, Data Returned Scenario"""

    with open(
        os.path.join(DATA_DIRECTORY, "Special_Version.html"), "rb"
    ) as version_html:

        mocker.patch(
            "fetch_data.version_data.create_software_version_data_observation.requests.get",
            side_effect=[MockResponse(200, version_html.read())],
        )
        success = await create_software_version_observation(1)
        assert success


@pytest.mark.asyncio
@pytest.mark.version
async def test_create_software_version_observation_failure(mocker):
    """Test One-Pull Per Month, Data Returned Scenario"""

    mocker.patch(
        "fetch_data.version_data.create_software_version_data_observation.requests.get",
        side_effect=[
            HTTPError(
                url="query.test.url/wiki/Special:Version",
                code=500,
                msg="Error",
                hdrs="",
                fp=None,
            )
        ],
    )
    success = await create_software_version_observation(1)
    assert success is False
