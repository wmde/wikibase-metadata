"""Test create_software_version_observation"""

import os
import time
import pytest
from fetch_data import create_software_version_observation
from tests.test_schema import test_schema
from tests.test_create_observation.test_create_software_version_observation.test_constants import (
    DATA_DIRECTORY,
)
from tests.mock_info import MockBackgroundClassList, MockInfo
from tests.utils import MockRequest, MockResponse


FETCH_SOFTWARE_MUTATION = """mutation MyMutation($wikibaseId: Int!) {
  fetchVersionData(wikibaseId: $wikibaseId)
}"""


@pytest.mark.asyncio
@pytest.mark.dependency(
    name="software-version-success",
    depends=["software-version-fail-ood"],
    scope="session",
)
@pytest.mark.mutation
@pytest.mark.soup
@pytest.mark.version
async def test_create_software_version_observation_success(mocker):
    """Test Data Returned Scenario"""

    time.sleep(1)

    with open(
        os.path.join(DATA_DIRECTORY, "Special_Version.html"), "rb"
    ) as version_html:

        mocker.patch(
            "fetch_data.soup_data.software.create_software_version_data_observation.requests.get",
            side_effect=[MockResponse("", 200, version_html.read())],
        )

    test_context = {
        "background_tasks": MockBackgroundClassList(),
        "request": MockRequest({"authorization": "Bearer: test-auth-token"}),
    }

    result = await test_schema.execute(
        FETCH_SOFTWARE_MUTATION,
        variable_values={"wikibaseId": 1},
        context_value=test_context,
    )

    assert result.errors is None
    assert result.data is not None
    assert result.data["fetchVersionData"]

    assert len(test_context["background_tasks"].tasks) == 1


@pytest.mark.asyncio
@pytest.mark.dependency(
    name="software-version-success-ii",
    depends=["add-wikibase-ii"],
    scope="session",
)
@pytest.mark.mutation
@pytest.mark.soup
@pytest.mark.version
async def test_create_software_version_observation_success_ii(mocker):
    """Test Data Returned Scenario"""

    time.sleep(1)

    with open(
        os.path.join(DATA_DIRECTORY, "Special_Version_ii.html"), "rb"
    ) as version_html:

        mocker.patch(
            "fetch_data.soup_data.software.create_software_version_data_observation.requests.get",
            side_effect=[MockResponse("", 200, version_html.read())],
        )

    test_context = {
        "background_tasks": MockBackgroundClassList(),
        "request": MockRequest({"authorization": "Bearer: test-auth-token"}),
    }

    result = await test_schema.execute(
        FETCH_SOFTWARE_MUTATION,
        variable_values={"wikibaseId": 2},
        context_value=test_context,
    )

    assert result.errors is None
    assert result.data is not None
    assert result.data["fetchVersionData"]

    assert len(test_context["background_tasks"].tasks) == 1


@pytest.mark.asyncio
@pytest.mark.dependency(
    name="software-version-failure",
    depends=["software-version-success"],
    scope="session",
)
@pytest.mark.soup
@pytest.mark.version
async def test_create_software_version_observation_failure(mocker):
    """Test Failure Scenario"""

    time.sleep(1)

    mocker.patch(
        "fetch_data.soup_data.software.create_software_version_data_observation.requests.get",
        side_effect=[MockResponse("", 500)],
    )
    mock_info = MockInfo(context={"background_tasks": MockBackgroundClassList()})
    success = await create_software_version_observation(1, mock_info)
    assert success is False
    assert len(mock_info.context["background_tasks"].tasks) == 1
