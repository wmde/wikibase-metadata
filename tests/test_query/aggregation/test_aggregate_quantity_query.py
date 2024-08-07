"""Test Aggregate Quantity Query"""

import pytest
from tests.test_schema import test_schema
from tests.utils import assert_layered_property_value


AGGREGATED_QUANTITY_QUERY = """
query MyQuery {
  aggregateQuantity {
    totalItems
    totalLexemes
    totalProperties
    totalTriples
    wikibaseCount
  }
}
"""


@pytest.mark.asyncio
@pytest.mark.agg
@pytest.mark.dependency(depends=["quantity-success"], scope="session")
@pytest.mark.quantity
@pytest.mark.query
async def test_aggregate_quantity_query():
    """Test Aggregate Quantity Query"""

    result = await test_schema.execute(AGGREGATED_QUANTITY_QUERY)

    assert result.errors is None
    assert result.data is not None

    assert_layered_property_value(result.data, ["aggregateQuantity", "totalItems"], 2)
    assert_layered_property_value(result.data, ["aggregateQuantity", "totalLexemes"], 4)
    assert_layered_property_value(
        result.data, ["aggregateQuantity", "totalProperties"], 1
    )
    assert_layered_property_value(result.data, ["aggregateQuantity", "totalTriples"], 8)
    assert_layered_property_value(
        result.data, ["aggregateQuantity", "wikibaseCount"], 1
    )
