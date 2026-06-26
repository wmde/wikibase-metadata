"""Test Bulk Connectivity Update"""

import pytest
from model.database.wikibase_model import WikibaseModel
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


@pytest.fixture
async def wikibase(db_session):
    """Create 3 test wikibases for connectivity tests"""
    from sqlalchemy.ext.asyncio import AsyncSession

    async with AsyncSession(bind=db_session) as session:
        for i in range(3):
            wikibase = WikibaseModel(
                wikibase_name=f"Connectivity Test Wikibase",
                base_url=f"https://connectivity-example-{i}.com",
                sparql_endpoint_url=f"https://connectivity-example-{i}.com/sparql",
            )
            wikibase.checked = True
            wikibase.reuse = True
            wikibase.test = False
            wikibase.wikibase_type = None
            session.add(wikibase)
        await session.flush()


@pytest.mark.asyncio
@pytest.mark.mutation
async def test_update_all_connectivity_observations_fail(wikibase, mocker): # pylint: disable=unused-argument
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
