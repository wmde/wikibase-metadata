"""Test Bulk Quantity Update"""

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from model.database import WikibaseModel
from tests.test_schema import test_schema
from tests.utils import get_mock_context

ALL_QUANTITY_DATA_MUTATION = """
mutation MyMutation {
  updateAllQuantityData {
    failure
    success
    total
  }
}
"""


@pytest.fixture
async def ten_wikibases_with_sparql(db_session):
    """Create 10 test wikibases with sparql endpoint for quantity tests"""
    async with AsyncSession(bind=db_session) as session:
        for i in range(10):
            wikibase = WikibaseModel(
                wikibase_name=f"Quantity Test Wikibase {i}",
                base_url=f"https://quantity-example-{i}.com",
                sparql_endpoint_url=f"https://quantity-example-{i}.com/sparql",
                reuse=True,
                wikibase_type=None,
            )
            wikibase.checked = True
            session.add(wikibase)
        await session.flush()


@pytest.mark.asyncio
@pytest.mark.mutation
async def test_update_all_quantity_observations_fail(ten_wikibases_with_sparql, mocker):
    """Test Weird Error Scenario"""

    def mockery(*args, **kwargs):
        raise RuntimeError

    mocker.patch(
        "fetch_data.sparql_data.create_quantity_data_observation.get_sparql_results",
        side_effect=mockery,
    )

    result = await test_schema.execute(
        ALL_QUANTITY_DATA_MUTATION,
        context_value=get_mock_context("test-auth-token"),
    )
    assert result.errors is None
    assert result.data is not None
    assert result.data.get("updateAllQuantityData") is not None
    assert result.data["updateAllQuantityData"].get("failure") == 10
    assert result.data["updateAllQuantityData"].get("success") == 0
    assert result.data["updateAllQuantityData"].get("total") == 10
