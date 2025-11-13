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
@pytest.mark.soup
async def test_update_out_of_date_time_to_first_value_observations_fail(mocker):
    """Test Error Returned Scenario"""

    mocker.patch(
        "fetch_data.utils.fetch_data_from_api.requests.get",
        side_effect=[MockResponse("", 404)],
    )
    result = await update_out_of_date_time_to_first_value_observations()
    assert result.failure == 1
    assert result.success == 0
    assert result.total == 1
