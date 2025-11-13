"""Test Bulk Statistics Update"""

import pytest
from tests.test_schema import test_schema
from tests.utils import get_mock_context

ALL_STATISTICS_DATA_MUTATION = """
mutation MyMutation {
  updateAllStatisticsData {
    failure
    success
    total
  }
}
"""


@pytest.mark.asyncio
@pytest.mark.dependency(
    name="statistics-fail-all",
    depends=[
        "mutate-cloud-instances",
        "update-wikibase-type-other",
        "update-wikibase-type-suite",
        "update-wikibase-type-test",
    ],
    scope="session",
)
@pytest.mark.mutation
async def test_update_all_statistics_observations_fail(mocker):
    """Test Weird Error Scenario"""

    def mockery(*args, **kwargs):
        raise RuntimeError

    mocker.patch(
        "fetch_data.soup_data.create_statistics_data_observation.requests.get",
        side_effect=mockery,
    )

    result = await test_schema.execute(
        ALL_STATISTICS_DATA_MUTATION,
        context_value=get_mock_context("test-auth-token"),
    )
    assert result.errors is None
    assert result.data is not None
    assert result.data.get("updateAllStatisticsData") is not None
    assert result.data["updateAllStatisticsData"].get("failure") == 3
    assert result.data["updateAllStatisticsData"].get("success") == 0
    assert result.data["updateAllStatisticsData"].get("total") == 3
