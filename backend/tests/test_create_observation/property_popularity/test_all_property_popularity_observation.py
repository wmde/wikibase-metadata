"""Test Bulk Property Popularity Update"""

import pytest

from data import get_async_session
from model.database import WikibaseModel
from tests.test_schema import test_schema
from tests.utils import get_mock_context

ALL_PROPERTY_POPULARITY_DATA_MUTATION = """
mutation MyMutation {
  updateAllPropertyPopularityData {
    failure
    success
    total
  }
}
"""


@pytest.fixture
async def three_wikibases_with_sparql(db_session):  # pylint: disable=unused-argument
    """Create 3 test wikibases with sparql endpoint for property popularity tests"""
    async with get_async_session() as session:
        for i in range(3):
            wikibase = WikibaseModel(
                wikibase_name=f"Property Test Wikibase {i}",
                base_url=f"https://property-example-{i}.com",
                sparql_endpoint_url=f"https://property-example-{i}.com/sparql",
            )
            wikibase.checked = True
            wikibase.reuse = True
            wikibase.test = False
            wikibase.wikibase_type = None
            session.add(wikibase)
        await session.flush()


@pytest.mark.asyncio
@pytest.mark.mutation
async def test_update_all_property_popularity_observations_fail(
    three_wikibases_with_sparql, mocker
):
    """Test Weird Error Scenario"""

    def mockery(*args, **kwargs):
        raise RuntimeError

    mocker.patch(
        "fetch_data.sparql_data.create_property_popularity_data_observation.get_sparql_results",
        side_effect=mockery,
    )

    result = await test_schema.execute(
        ALL_PROPERTY_POPULARITY_DATA_MUTATION,
        context_value=get_mock_context("test-auth-token"),
    )
    assert result.errors is None
    assert result.data is not None
    assert result.data.get("updateAllPropertyPopularityData") is not None
    assert result.data["updateAllPropertyPopularityData"].get("failure") == 3
    assert result.data["updateAllPropertyPopularityData"].get("success") == 0
    assert result.data["updateAllPropertyPopularityData"].get("total") == 3
