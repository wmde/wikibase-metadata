"""Test Aggregate Created Query"""

import pytest
from tests.test_schema import test_schema
from tests.utils import assert_layered_property_count, assert_layered_property_value


WIKIBASE_LIST_QUERY = """
query MyQuery {
  aggregateCreated {
    year
    wikibaseCount
  }
}
"""


@pytest.mark.asyncio
@pytest.mark.agg
@pytest.mark.dependency(depends=["log-success-1", "log-success-2"], scope="session")
@pytest.mark.log
@pytest.mark.query
async def test_aggregate_created_query():
    """Test Aggregate Created Query"""

    result = await test_schema.execute(WIKIBASE_LIST_QUERY)

    assert result.errors is None
    assert result.data is not None
    assert_layered_property_count(result.data, ["aggregateCreated"], 1)
    assert_layered_property_value(result.data, ["aggregateCreated", 0, "year"], 2023)
    assert_layered_property_value(
        result.data, ["aggregateCreated", 0, "wikibaseCount"], 1
    )
