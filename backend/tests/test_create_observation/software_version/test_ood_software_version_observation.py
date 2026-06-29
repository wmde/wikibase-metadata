"""Test update_out_of_date_software_observations"""

import pytest

from fetch_data import update_out_of_date_software_observations
from tests.utils import MockResponse


@pytest.mark.asyncio
@pytest.mark.soup
@pytest.mark.version
async def test_update_out_of_date_software_observations_fail(
    wikibase_without_type, mocker
):  # pylint: disable=unused-argument, redefined-outer-name
    """Test Data Returned Scenario"""

    mocker.patch(
        "fetch_data.soup_data.software.create_software_version_data_observation.requests.get",
        side_effect=[MockResponse("", 404)],
    )
    result = await update_out_of_date_software_observations()
    assert result.failure == 1
    assert result.success == 0
    assert result.total == 1
