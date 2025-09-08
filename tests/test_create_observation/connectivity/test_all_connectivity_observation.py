"""Test Bulk Connectivity Update"""

import pytest
from tests.test_schema import test_schema
from tests.utils import get_mock_context

ALL_CONNECTIVITY_DATA_MUTATION = """
mutation MyMutation {
  updateAllConnectivityData {
    failure
    success
    total
  }
}
"""


@pytest.mark.asyncio
@pytest.mark.dependency(
    name="connectivity-fail-all",
    depends=[
        "mutate-cloud-instances",
        "update-wikibase-type-other",
        "update-wikibase-type-suite",
        "update-wikibase-type-test",
    ],
    scope="session",
)
@pytest.mark.mutation
async def test_update_all_connectivity_observations_fail(mocker):
    """Test Weird Error Scenario"""

    def mockery(*args, **kwargs):
        raise RuntimeError

    mocker.patch(
        "fetch_data.sparql_data.create_connectivity_data_observation.get_sparql_results",
        side_effect=mockery,
    )

    result = await test_schema.execute(
        ALL_CONNECTIVITY_DATA_MUTATION,
        context_value=get_mock_context("test-auth-token"),
    )
    assert result.errors is None
    assert result.data is not None
    assert result.data.get("updateAllConnectivityData") is not None
    assert result.data["updateAllConnectivityData"].get("failure") == 3
    assert result.data["updateAllConnectivityData"].get("success") == 0
    assert result.data["updateAllConnectivityData"].get("total") == 3
