"""Test create_property_popularity_observation"""

import pytest
from fetch_data import update_out_of_date_stats_observations
from tests.utils import MockResponse


DATA_DIRECTORY = "tests/test_create_observation/test_create_statistics_observation/data"


@pytest.mark.asyncio
@pytest.mark.dependency(
    name="statistics-fail-ood", depends=["add-wikibase"], scope="session"
)
@pytest.mark.soup
@pytest.mark.statistics
async def test_update_out_of_date_stats_observations_fail(mocker):
    """Test Data Returned Scenario"""

    mocker.patch(
        "fetch_data.soup_data.create_statistics_data_observation.requests.get",
        side_effect=[MockResponse("", 404)],
    )
    await update_out_of_date_stats_observations()
