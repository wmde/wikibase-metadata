"""Test update_out_of_date_software_observations"""

import pytest
from fetch_data import update_out_of_date_software_observations
from tests.utils import MockResponse


@pytest.mark.asyncio
@pytest.mark.dependency(
    name="software-version-fail-ood", depends=["add-wikibase"], scope="session"
)
@pytest.mark.soup
@pytest.mark.version
async def test_update_out_of_date_software_observations_fail(mocker):
    """Test Data Returned Scenario"""

    mocker.patch(
        "fetch_data.soup_data.software.create_software_version_data_observation.requests.get",
        side_effect=[MockResponse("", 404)],
    )
    await update_out_of_date_software_observations()
