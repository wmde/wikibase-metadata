"""Test create_user_observation"""

import pytest
from requests import ReadTimeout
from fetch_data import create_user_observation


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
    """Test No-Data Scenario"""

    mocker.patch(
        "fetch_data.user_data.fetch_all_user_data.fetch_api_data",
        side_effect=[ReadTimeout()],
    )
    success = await create_user_observation(1)
    assert success is False
