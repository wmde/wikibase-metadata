"""Test Bulk Software Version Update"""

import os

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from fetch_data import create_software_version_observation
from model.database import WikibaseModel
from tests.mock_info import MockBackgroundClassList, MockInfo
from tests.test_schema import test_schema
from tests.utils import MockResponse, get_mock_context

ALL_VERSION_DATA_MUTATION = """
mutation MyMutation {
  updateAllVersionData {
    failure
    success
    total
  }
}
"""

DATA_DIRECTORY = os.path.join(os.path.dirname(__file__), "data")


@pytest.fixture
async def three_wikibases_with_article_path(db_session):
    """Create 3 test wikibases with article path for software version tests"""
    async with AsyncSession(bind=db_session) as session:
        wikibases = []
        for i in range(3):
            wikibase = WikibaseModel(
                wikibase_name=f"Software Version Test Wikibase {i}",
                base_url=f"https://software-version-example-{i}.com",
                article_path="/wiki",
                reuse=True,
                wikibase_type=None,
            )
            wikibase.checked = True
            session.add(wikibase)
            wikibases.append(wikibase)
        await session.flush()
        for wikibase in wikibases:
            await session.refresh(wikibase)

        return [w.id for w in wikibases]


@pytest.mark.asyncio
@pytest.mark.mutation
@pytest.mark.soup
@pytest.mark.version
async def test_update_all_software_version_observations_fail(
    three_wikibases_with_article_path, mocker
):  # pylint: disable=unused-argument, redefined-outer-name
    """Test HTTP Error Scenario - all 3 wikibases fail with a genuine HTTPError"""

    mocker.patch(
        "fetch_data.soup_data.software.create_software_version_data_observation.requests.get",
        side_effect=[
            MockResponse("", 500),
            MockResponse("", 500),
            MockResponse("", 500),
        ],
    )

    result = await test_schema.execute(
        ALL_VERSION_DATA_MUTATION,
        context_value=get_mock_context("test-auth-token"),
    )
    assert result.errors is None
    assert result.data is not None
    assert result.data.get("updateAllVersionData") is not None
    assert result.data["updateAllVersionData"].get("failure") == 3
    assert result.data["updateAllVersionData"].get("success") == 0
    assert result.data["updateAllVersionData"].get("total") == 3


@pytest.mark.asyncio
@pytest.mark.mutation
@pytest.mark.soup
@pytest.mark.version
async def test_create_software_version_observation_success(
    wikibase_with_article_path, mocker
):  # pylint: disable=redefined-outer-name
    """Test Data Returned Scenario"""

    wikibase_id = wikibase_with_article_path.id

    with open(
        os.path.join(DATA_DIRECTORY, "Special_Version.html"), "rb"
    ) as version_html:
        mocker.patch(
            "fetch_data.soup_data.software.create_software_version_data_observation.requests.get",
            side_effect=[MockResponse("", 200, version_html.read())],
        )

    mock_info = MockInfo(context={"background_tasks": MockBackgroundClassList()})
    success = await create_software_version_observation(wikibase_id, mock_info)

    assert success is True
    assert len(mock_info.context["background_tasks"].tasks) == 1


@pytest.mark.asyncio
@pytest.mark.mutation
@pytest.mark.soup
@pytest.mark.version
async def test_create_software_version_observation_success_ii(
    wikibase_with_article_path, mocker
):  # pylint: disable=redefined-outer-name
    """Test Data Returned Scenario, second fixture (different Special:Version markup)"""

    wikibase_id = wikibase_with_article_path.id

    with open(
        os.path.join(DATA_DIRECTORY, "Special_Version_ii.html"), "rb"
    ) as version_html:
        mocker.patch(
            "fetch_data.soup_data.software.create_software_version_data_observation.requests.get",
            side_effect=[MockResponse("", 200, version_html.read())],
        )

    mock_info = MockInfo(context={"background_tasks": MockBackgroundClassList()})
    success = await create_software_version_observation(wikibase_id, mock_info)

    assert success is True
    assert len(mock_info.context["background_tasks"].tasks) == 1


@pytest.mark.asyncio
@pytest.mark.soup
@pytest.mark.version
async def test_create_software_version_observation_failure(
    wikibase_with_article_path, mocker
):  # pylint: disable=redefined-outer-name
    """Test Failure Scenario - genuine HTTPError via HTTP 500"""

    wikibase_id = wikibase_with_article_path.id

    mocker.patch(
        "fetch_data.soup_data.software.create_software_version_data_observation.requests.get",
        side_effect=[MockResponse("", 500)],
    )

    mock_info = MockInfo(context={"background_tasks": MockBackgroundClassList()})
    success = await create_software_version_observation(wikibase_id, mock_info)

    assert success is False
    assert len(mock_info.context["background_tasks"].tasks) == 1
