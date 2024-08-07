"""Test Aggregate Quantity Query"""

import pytest
from tests.test_schema import test_schema
from tests.utils import assert_layered_property_value


AGGREGATED_USERS_QUERY = """
query MyQuery {
  aggregateUsers {
    totalAdmin
    totalUsers
    wikibaseCount
  }
}
"""


@pytest.mark.asyncio
@pytest.mark.agg
@pytest.mark.dependency(depends=["user-2000"], scope="session")
@pytest.mark.user
@pytest.mark.query
async def test_aggregate_users_query():
    """Test Aggregate Users Query"""

    result = await test_schema.execute(AGGREGATED_USERS_QUERY)

    assert result.errors is None
    assert result.data is not None

    assert_layered_property_value(result.data, ["aggregateUsers", "totalAdmin"], 715)
    assert_layered_property_value(result.data, ["aggregateUsers", "totalUsers"], 2000)
    assert_layered_property_value(result.data, ["aggregateUsers", "wikibaseCount"], 1)
