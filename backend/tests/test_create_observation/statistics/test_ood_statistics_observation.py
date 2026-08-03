"""Test update_out_of_date_stats_observations"""

import pytest

from fetch_data import update_out_of_date_stats_observations
from tests.utils import MockResponse


@pytest.mark.asyncio
@pytest.mark.soup
@pytest.mark.statistics
async def test_update_out_of_date_stats_observations_fail(
    wikibase_with_article_path, mocker
):  # pylint: disable=redefined-outer-name, unused-argument
    """Test Data Returned Scenario"""

    mocker.patch(
        "fetch_data.soup_data.create_statistics_data_observation.requests.get",
        side_effect=[MockResponse("", 404)],
    )
    result = await update_out_of_date_stats_observations()
    assert result.failure == 1
    assert result.success == 0
    assert result.total == 1
