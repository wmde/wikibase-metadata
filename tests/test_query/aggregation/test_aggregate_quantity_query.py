"""Test Aggregate Quantity Query"""

import pytest
from tests.test_schema import test_schema
from tests.utils import assert_layered_property_value, get_mock_context


AGGREGATED_QUANTITY_QUERY = """
query MyQuery($wikibaseFilter: WikibaseFilterInput) {
  aggregateQuantity(wikibaseFilter: $wikibaseFilter) {
    totalItems
    totalLexemes
    totalProperties
    totalTriples
    totalExternalIdentifierProperties
    totalExternalIdentifierStatements
    totalUrlProperties
    totalUrlStatements
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

    result = await test_schema.execute(
        AGGREGATED_QUANTITY_QUERY, context_value=get_mock_context("test-auth-token")
    )

    assert result.errors is None
    assert result.data is not None

    assert_layered_property_value(result.data, ["aggregateQuantity", "totalItems"], 2)
    assert_layered_property_value(result.data, ["aggregateQuantity", "totalLexemes"], 4)
    assert_layered_property_value(
        result.data, ["aggregateQuantity", "totalProperties"], 1
    )
    assert_layered_property_value(result.data, ["aggregateQuantity", "totalTriples"], 8)
    assert_layered_property_value(
        result.data, ["aggregateQuantity", "totalExternalIdentifierProperties"], 16
    )
    assert_layered_property_value(
        result.data, ["aggregateQuantity", "totalExternalIdentifierStatements"], 32
    )
    assert_layered_property_value(
        result.data, ["aggregateQuantity", "totalUrlProperties"], 64
    )
    assert_layered_property_value(
        result.data, ["aggregateQuantity", "totalUrlStatements"], 128
    )
    assert_layered_property_value(
        result.data, ["aggregateQuantity", "wikibaseCount"], 1
    )


@pytest.mark.asyncio
@pytest.mark.agg
@pytest.mark.query
@pytest.mark.dependency(
    depends=["update-wikibase-type", "update-wikibase-type-ii"], scope="session"
)
@pytest.mark.parametrize(
    ["exclude", "expected_count"],
    [
        ([], 1),
        (["CLOUD"], 1),
        (["OTHER"], 1),
        (["SUITE"], 0),
        (["CLOUD", "OTHER"], 1),
        (["CLOUD", "SUITE"], 0),
        (["OTHER", "SUITE"], 0),
        (["CLOUD", "OTHER", "SUITE"], 0),
    ],
)
@pytest.mark.user
async def test_aggregate_quantity_query_filtered(exclude: list, expected_count: int):
    """Test Aggregate Quantity Query"""

    result = await test_schema.execute(
        AGGREGATED_QUANTITY_QUERY,
        variable_values={"wikibaseFilter": {"wikibaseType": {"exclude": exclude}}},
        context_value=get_mock_context("test-auth-token"),
    )

    assert result.errors is None
    assert result.data is not None

    assert_layered_property_value(
        result.data, ["aggregateQuantity", "wikibaseCount"], expected_count
    )
