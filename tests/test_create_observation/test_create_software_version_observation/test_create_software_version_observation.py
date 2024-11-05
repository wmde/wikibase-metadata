"""Test create_property_popularity_observation"""

import os
import time
from urllib.error import HTTPError
import pytest
from fetch_data import create_software_version_observation
from tests.test_create_observation.test_create_software_version_observation.test_constants import (
    DATA_DIRECTORY,
)
from tests.utils import MockResponse


@pytest.mark.asyncio
@pytest.mark.dependency(
    name="software-version-success", depends=["add-wikibase"], scope="session"
)
@pytest.mark.soup
@pytest.mark.version
async def test_create_software_version_observation_success(mocker):
    """Test Data Returned Scenario"""

    time.sleep(1)

    with open(
        os.path.join(DATA_DIRECTORY, "Special_Version.html"), "rb"
    ) as version_html:

        mocker.patch(
            "fetch_data.soup_data.create_software_version_data_observation.requests.get",
            side_effect=[MockResponse(200, version_html.read())],
        )
        success = await create_software_version_observation(1)
        assert success


@pytest.mark.asyncio
@pytest.mark.dependency(
    name="software-version-failure", depends=["software-version-success"]
)
@pytest.mark.soup
@pytest.mark.version
async def test_create_software_version_observation_failure(mocker):
    """Test Failure Scenario"""

    time.sleep(1)

    mocker.patch(
        "fetch_data.soup_data.create_software_version_data_observation.requests.get",
        side_effect=[
            HTTPError(
                url="example.com/wiki/Special:Version",
                code=500,
                msg="Error",
                hdrs="",
                fp=None,
            )
        ],
    )
    success = await create_software_version_observation(1)
    assert success is False
