"""Test Aggregate Property Popularity Query"""

import pytest
from tests.test_schema import test_schema
from tests.utils import (
    assert_layered_property_count,
    assert_layered_property_value,
    assert_page_meta,
)


AGGREGATED_PROPERTY_POPULARITY_QUERY = """
query MyQuery($pageNumber: Int!, $pageSize: Int!) {
  aggregatePropertyPopularity(pageNumber: $pageNumber, pageSize: $pageSize) {
    meta {
      pageNumber
      pageSize
      totalCount
      totalPages
    }
    data {
      id
      propertyUrl
      usageCount
      wikibaseCount
    }
  }
}
"""


@pytest.mark.asyncio
@pytest.mark.agg
@pytest.mark.dependency(depends=["property-popularity-success"], scope="session")
@pytest.mark.property
@pytest.mark.query
async def test_aggregate_property_popularity_query():
    """Test Aggregate Property Popularity Query"""

    result = await test_schema.execute(
        AGGREGATED_PROPERTY_POPULARITY_QUERY,
        variable_values={"pageNumber": 1, "pageSize": 30},
    )

    assert result.errors is None
    assert result.data is not None

    assert_page_meta(
        result.data["aggregatePropertyPopularity"],
        expected_page_number=1,
        expected_page_size=30,
        expected_total_count=2,
        expected_total_pages=1,
    )
    assert_layered_property_count(
        result.data, ["aggregatePropertyPopularity", "data"], 2
    )

    for index, (expected_id, expected_property_url, expected_usage_count) in enumerate(
        [("1", "P1", 12), ("2", "P14", 1)]
    ):
        assert_layered_property_value(
            result.data,
            ["aggregatePropertyPopularity", "data", index, "id"],
            expected_id,
        )
        assert_layered_property_value(
            result.data,
            ["aggregatePropertyPopularity", "data", index, "propertyUrl"],
            expected_property_url,
        )
        assert_layered_property_value(
            result.data,
            ["aggregatePropertyPopularity", "data", index, "usageCount"],
            expected_usage_count,
        )
        assert_layered_property_value(
            result.data,
            ["aggregatePropertyPopularity", "data", index, "wikibaseCount"],
            1,
        )
