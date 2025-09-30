"""Test Aggregate Property Popularity Query"""

import pytest
from tests.test_schema import test_schema
from tests.utils import (
    assert_layered_property_count,
    assert_layered_property_value,
    assert_page_meta,
    get_mock_context,
)


AGGREGATED_PROPERTY_POPULARITY_QUERY = """
query MyQuery($pageNumber: Int!, $pageSize: Int!, $wikibaseFilter: WikibaseFilterInput) {
  aggregatePropertyPopularity(
    pageNumber: $pageNumber
    pageSize: $pageSize
    wikibaseFilter: $wikibaseFilter
  ) {
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

    assert_page_meta(result.data["aggregatePropertyPopularity"], 1, 30, 2, 1)

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


@pytest.mark.asyncio
@pytest.mark.agg
@pytest.mark.query
@pytest.mark.dependency(
    depends=["update-wikibase-type-other", "update-wikibase-type-suite"],
    scope="session",
)
@pytest.mark.parametrize(
    ["exclude", "expected_count"],
    [
        ([], 2),
        (["CLOUD"], 2),
        (["OTHER"], 2),
        (["SUITE"], 0),
        (["CLOUD", "OTHER"], 2),
        (["CLOUD", "SUITE"], 0),
        (["OTHER", "SUITE"], 0),
        (["CLOUD", "OTHER", "SUITE"], 0),
    ],
)
@pytest.mark.user
async def test_aggregate_property_popularity_query_filtered(
    exclude: list, expected_count: int
):
    """Test Aggregate Property Popularity Query"""

    result = await test_schema.execute(
        AGGREGATED_PROPERTY_POPULARITY_QUERY,
        variable_values={
            "pageNumber": 1,
            "pageSize": 1,
            "wikibaseFilter": {"wikibaseType": {"exclude": exclude}},
        },
    )

    assert result.errors is None
    assert result.data is not None

    assert_layered_property_value(
        result.data,
        ["aggregatePropertyPopularity", "meta", "totalCount"],
        expected_count,
    )
