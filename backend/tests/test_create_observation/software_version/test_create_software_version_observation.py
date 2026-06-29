"""Test create_software_version_observation"""

import os
import time

import pytest

from data import get_async_session
from fetch_data import create_software_version_observation
from model.database import WikibaseModel
from tests.mock_info import MockBackgroundClassList, MockInfo
from tests.test_create_observation.software_version.test_constants import (
    DATA_DIRECTORY,
)
from tests.test_schema import test_schema
from tests.utils import MockRequest, MockResponse

FETCH_SOFTWARE_MUTATION = """mutation MyMutation($wikibaseId: Int!) {
  fetchVersionData(wikibaseId: $wikibaseId)
}"""


@pytest.fixture
async def wikibase_with_article_path(db_session):  # pylint: disable=unused-argument
    """Create a wikibase with article path for software version tests"""
    async with get_async_session() as session:
        wikibase = WikibaseModel(
            wikibase_name="Software Version Test Wikibase",
            base_url="https://software-version-test-example.com",
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
@pytest.mark.mutation
@pytest.mark.soup
@pytest.mark.version
async def test_create_software_version_observation_success(
    wikibase_with_article_path, mocker
):  # pylint: disable=redefined-outer-name
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
        variable_values={"wikibaseId": wikibase_with_article_path},
        context_value=test_context,
    )

    assert result.errors is None
    assert result.data is not None
    assert result.data["fetchVersionData"]

    assert len(test_context["background_tasks"].tasks) == 1


@pytest.mark.asyncio
@pytest.mark.mutation
@pytest.mark.soup
@pytest.mark.version
async def test_create_software_version_observation_success_ii(
    wikibase_with_article_path, mocker
):  # pylint: disable=redefined-outer-name
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
        variable_values={"wikibaseId": wikibase_with_article_path},
        context_value=test_context,
    )

    assert result.errors is None
    assert result.data is not None
    assert result.data["fetchVersionData"]

    assert len(test_context["background_tasks"].tasks) == 1


@pytest.mark.asyncio
@pytest.mark.soup
@pytest.mark.version
async def test_create_software_version_observation_failure(
    wikibase_with_article_path, mocker
):  # pylint: disable=redefined-outer-name
    """Test Failure Scenario"""

    time.sleep(1)

    mocker.patch(
        "fetch_data.soup_data.software.create_software_version_data_observation.requests.get",
        side_effect=[MockResponse("", 500)],
    )
    mock_info = MockInfo(context={"background_tasks": MockBackgroundClassList()})
    success = await create_software_version_observation(
        wikibase_with_article_path, mock_info
    )
    assert success is False
    assert len(mock_info.context["background_tasks"].tasks) == 1
