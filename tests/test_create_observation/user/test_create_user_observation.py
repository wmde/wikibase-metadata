"""Test create_user_observation"""

from math import floor
import time
import pytest
from requests import ReadTimeout
from fetch_data import create_user_observation
from tests.test_schema import test_schema
from tests.utils.mock_request import get_mock_context


FETCH_USER_MUTATION = """mutation MyMutation($wikibaseId: Int!) {
  fetchUserData(wikibaseId: $wikibaseId)
}"""


TEST_USER_GROUPS = ["bureaucrat", "sysop", "bot", "editor", "administrator"]

TEST_USER_GROUPS_IMPLICIT = {"*", "user", "autoconfirmed"}


@pytest.mark.asyncio
@pytest.mark.dependency(
    name="user-failure", depends=["user-empty-ood"], scope="session"
)
@pytest.mark.user
async def test_create_user_observation_failure(mocker):
    """Test Error Scenario"""

    time.sleep(1)

    mocker.patch(
        "fetch_data.api_data.user_data.fetch_all_user_data.fetch_api_data",
        side_effect=[ReadTimeout()],
    )
    success = await create_user_observation(1)
    assert success is False


@pytest.mark.asyncio
@pytest.mark.dependency(name="user-20", depends=["user-failure"], scope="session")
@pytest.mark.mutation
@pytest.mark.user
async def test_create_user_observation_single_pull(mocker):
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
        variable_values={"wikibaseId": 1},
        context_value=get_mock_context("test-auth-token"),
    )

    assert result.errors is None
    assert result.data is not None
    assert result.data["fetchUserData"]


@pytest.mark.asyncio
@pytest.mark.dependency(name="user-2000", depends=["user-20"], scope="session")
@pytest.mark.user
async def test_create_user_observation_multiple_pull(mocker):
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
    success = await create_user_observation(1)
    assert success
