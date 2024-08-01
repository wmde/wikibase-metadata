"""Test create_user_observation"""

import pytest
from requests import ReadTimeout
from fetch_data import create_user_observation


TEST_USER_GROUPS = [
    "private",
    "bureaucrat",
    "interface-admin",
    "sysop",
    "bot",
    "data",
    "push-subscription-manager",
    "suppress",
    "editor",
    "administrator",
    "translationadmin",
    "contributor",
    "checkuser",
]

TEST_USER_GROUPS_IMPLICIT = {"*", "user", "autoconfirmed"}


@pytest.mark.asyncio
@pytest.mark.user
async def test_create_user_observation_empty(mocker):
    """Test No-Data Scenario"""

    mocker.patch(
        "fetch_data.user_data.fetch_all_user_data.fetch_api_data",
        side_effect=[{"query": {"allusers": []}}],
    )
    success = await create_user_observation(1)
    assert success


@pytest.mark.asyncio
@pytest.mark.user
async def test_create_user_observation_failure(mocker):
    """Test Error Scenario"""

    mocker.patch(
        "fetch_data.user_data.fetch_all_user_data.fetch_api_data",
        side_effect=[ReadTimeout()],
    )
    success = await create_user_observation(1)
    assert success is False


@pytest.mark.asyncio
@pytest.mark.user
async def test_create_user_observation_single_pull(mocker):
    """Test Data, Single Pull Scenario"""

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
        "fetch_data.user_data.fetch_all_user_data.fetch_api_data",
        side_effect=[{"query": {"allusers": users}}],
    )
    success = await create_user_observation(1)
    assert success


@pytest.mark.asyncio
@pytest.mark.user
async def test_create_user_observation_multiple_pull(mocker):
    """Test Data, Multiple Pull Scenario"""

    users = []
    for i in range(2000):
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

    limit = 500
    user_chunks = []
    for i in range(0, len(users), limit):
        chunk = {"query": {"allusers": users[i : i + limit]}}
        if i + limit < len(users):
            chunk["continue"] = {"aufrom": users[i + limit]}
        user_chunks.append(chunk)

    mocker.patch(
        "fetch_data.user_data.fetch_all_user_data.fetch_api_data",
        side_effect=user_chunks,
    )
    success = await create_user_observation(1)
    assert success
