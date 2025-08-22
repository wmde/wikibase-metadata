"""Test Aggregate URL Properties Query"""

import pytest
from tests.test_schema import test_schema
from tests.utils import assert_layered_property_value, get_mock_context


AGGREGATED_URLS_QUERY = """
query MyQuery($wikibaseFilter: WikibaseFilterInput) {
  aggregateUrls(wikibaseFilter: $wikibaseFilter) {
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
async def test_aggregate_urls_query():
    """Test Aggregate URL Properties Query"""

    result = await test_schema.execute(
        AGGREGATED_URLS_QUERY, context_value=get_mock_context("test-auth-token")
    )

    assert result.errors is None
    assert result.data is not None

    assert_layered_property_value(
        result.data, ["aggregateUrls", "totalUrlProperties"], 64
    )
    assert_layered_property_value(
        result.data, ["aggregateUrls", "totalUrlStatements"], 128
    )
    assert_layered_property_value(
        result.data, ["aggregateUrls", "wikibaseCount"], 1
    )

