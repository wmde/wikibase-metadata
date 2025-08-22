"""Test Aggregate External Identifiers Query"""

import pytest
from tests.test_schema import test_schema
from tests.utils import assert_layered_property_value, get_mock_context


AGGREGATED_EXTERNAL_IDENTIFIERS_QUERY = """
query MyQuery($wikibaseFilter: WikibaseFilterInput) {
  aggregateExternalIdentifiers(wikibaseFilter: $wikibaseFilter) {
    totalExternalIdentifierProperties
    totalExternalIdentifierStatements
    wikibaseCount
  }
}
"""


@pytest.mark.asyncio
@pytest.mark.agg
@pytest.mark.dependency(depends=["quantity-success"], scope="session")
@pytest.mark.quantity
@pytest.mark.query
async def test_aggregate_external_identifiers_query():
    """Test Aggregate External Identifiers Query"""

    result = await test_schema.execute(
        AGGREGATED_EXTERNAL_IDENTIFIERS_QUERY,
        context_value=get_mock_context("test-auth-token"),
    )

    assert result.errors is None
    assert result.data is not None

    assert_layered_property_value(
        result.data, ["aggregateExternalIdentifiers", "totalExternalIdentifierProperties"], 16
    )
    assert_layered_property_value(
        result.data, ["aggregateExternalIdentifiers", "totalExternalIdentifierStatements"], 32
    )
    assert_layered_property_value(
        result.data, ["aggregateExternalIdentifiers", "wikibaseCount"], 1
    )

