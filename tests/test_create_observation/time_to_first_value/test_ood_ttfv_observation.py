"""Test update_out_of_date_time_to_first_value_observations"""

import pytest
from fetch_data import update_out_of_date_time_to_first_value_observations
from tests.utils import MockResponse


@pytest.mark.asyncio
@pytest.mark.dependency(
    name="ttfv-fail-ood",
    depends=["add-wikibase", "add-wikibase-script-path"],
    scope="session",
)
async def test_update_out_of_date_time_to_first_value_observations_fail(mocker):
    """Test Error Returned Scenario"""

    mocker.patch(
        "fetch_data.api_data.time_to_first_value.create_time_to_first_value_observation.requests.get",
        side_effect=[MockResponse("", 404)],
    )
    assert await update_out_of_date_time_to_first_value_observations() == 1
