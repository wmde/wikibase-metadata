"""Test create_property_popularity_observation"""

import os
import pytest
from fetch_data.version_data.create_software_version_data_observation import (
    create_software_version_observation,
)


class MockResponse:
    status_code: int
    content: bytes

    def __init__(self, status_code: int, content: bytes):
        self.content = content
        self.status_code = status_code


DATA_DIRECTORY = "tests/test_create_software_version_observation/data"


@pytest.mark.asyncio
@pytest.mark.version
async def test_create_software_version_observation(mocker):
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
