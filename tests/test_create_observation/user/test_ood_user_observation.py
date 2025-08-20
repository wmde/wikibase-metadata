"""Test update_out_of_date_user_observations"""

import pytest
from fetch_data import update_out_of_date_user_observations


@pytest.mark.asyncio
@pytest.mark.dependency(
    name="user-empty-ood",
    depends=["add-wikibase", "add-wikibase-script-path"],
    scope="session",
)
@pytest.mark.user
async def test_update_out_of_date_user_observations_empty(mocker):
    """Test No-Data Scenario"""

    mocker.patch(
        "fetch_data.api_data.user_data.fetch_all_user_data.fetch_api_data",
        side_effect=[{"query": {"allusers": []}}],
    )
    await update_out_of_date_user_observations()
