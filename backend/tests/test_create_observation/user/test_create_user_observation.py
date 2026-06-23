"""Test create_user_observation"""

from math import floor
import time
import pytest
from requests import ReadTimeout
from data.database_connection import get_async_session
from model.database.wikibase_model import WikibaseModel
from fetch_data import create_user_observation
from tests.test_schema import test_schema
from tests.utils.mock_request import get_mock_context

FETCH_USER_MUTATION = """mutation MyMutation($wikibaseId: Int!) {
  fetchUserData(wikibaseId: $wikibaseId)
}"""


TEST_USER_GROUPS = ["bureaucrat", "sysop", "bot", "editor", "administrator"]

TEST_USER_GROUPS_IMPLICIT = {"*", "user", "autoconfirmed"}


@pytest.fixture
async def wikibase(db_session):  # pylint: disable=unused-argument
    """Create a wikibase with script path for user observation tests"""
    async with get_async_session() as session:
        wikibase = WikibaseModel(
            wikibase_name="User Test Wikibase",
            base_url="https://user-test-example.com",
            script_path="/w",
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
@pytest.mark.user
async def test_create_user_observation_failure(wikibase, mocker):
    """Test Error Scenario"""

    time.sleep(1)

    mocker.patch(
        "fetch_data.api_data.user_data.fetch_all_user_data.fetch_api_data",
        side_effect=[ReadTimeout()],
    )
    success = await create_user_observation(wikibase)
    assert success is False


@pytest.mark.asyncio
@pytest.mark.user
async def test_create_user_observation_single_pull(wikibase, mocker):
    """Test Data, Single Pull Scenario"""

    time.sleep(1)

    users = []
    for i in range(20):
        users.append(
            {
                "groups": sorted(
                    TEST_USER_GROUPS_IMPLICIT
                    | {TEST_USER_GROUPS[i % len(TEST_USER_GROUPS)]}
                    | {TEST_USER_GROUPS[(2 * i) % len(TEST_USER_GROUPS)]}
                ),
                "implicitgroups": sorted(TEST_USER_GROUPS_IMPLICIT),
            }
        )

    mocker.patch(
        "fetch_data.api_data.user_data.fetch_all_user_data.fetch_api_data",
        side_effect=[{"query": {"allusers": users}}],
    )

    result = await test_schema.execute(
        FETCH_USER_MUTATION,
        variable_values={"wikibaseId": wikibase},
        context_value=get_mock_context("test-auth-token"),
    )

    assert result.errors is None
    assert result.data is not None
    assert result.data["fetchUserData"]


@pytest.mark.asyncio
@pytest.mark.user
async def test_create_user_observation_multiple_pull(wikibase, mocker):
    """Test Data, Multiple Pull Scenario"""

    time.sleep(1)

    users = []
    for i in range(2000):
        users.append(
            {
                "groups": sorted(
                    TEST_USER_GROUPS_IMPLICIT
                    | {TEST_USER_GROUPS[i % len(TEST_USER_GROUPS)]}
                    | {TEST_USER_GROUPS[floor(i / 9) % len(TEST_USER_GROUPS)]}
                ),
                "implicitgroups": sorted(TEST_USER_GROUPS_IMPLICIT),
            }
        )

    limit = 500
    user_chunks = []
    for i in range(0, len(users), limit):
        chunk = {"query": {"allusers": users[i : i + limit]}}
        if i + limit < len(users):
            chunk["continue"] = {"aufrom": users[i + limit]}
        user_chunks.append(chunk)

    mocker.patch(
        "fetch_data.api_data.user_data.fetch_all_user_data.fetch_api_data",
        side_effect=user_chunks,
    )
    success = await create_user_observation(wikibase)
    assert success
