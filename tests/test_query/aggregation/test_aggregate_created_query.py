"""Test Aggregate Created Query"""

import pytest
from tests.test_schema import test_schema
from tests.utils import (
    assert_layered_property_count,
    assert_layered_property_value,
    get_mock_context,
)


AGGREGATED_CREATED_QUERY = """
query MyQuery($wikibaseFilter: WikibaseFilterInput) {
  aggregateCreated(wikibaseFilter: $wikibaseFilter) {
    year
    wikibaseCount
  }
}
"""


@pytest.mark.asyncio
@pytest.mark.agg
@pytest.mark.dependency(depends=["log-first-success-1"], scope="session")
@pytest.mark.log
@pytest.mark.query
async def test_aggregate_created_query():
    """Test Aggregate Created Query"""

    result = await test_schema.execute(
        AGGREGATED_CREATED_QUERY, context_value=get_mock_context("test-auth-token")
    )

    assert result.errors is None
    assert result.data is not None
    assert_layered_property_count(result.data, ["aggregateCreated"], 1)
    assert_layered_property_value(result.data, ["aggregateCreated", 0, "year"], 2023)
    assert_layered_property_value(
        result.data, ["aggregateCreated", 0, "wikibaseCount"], 1
    )


@pytest.mark.asyncio
@pytest.mark.agg
@pytest.mark.query
@pytest.mark.dependency(
    depends=["update-wikibase-type-other", "update-wikibase-type-suite"],
    scope="session",
)
@pytest.mark.parametrize(
    ["exclude", "expected_count", "expected_wikibase_count"],
    [
        ([], 1, 1),
        (["CLOUD"], 1, 1),
        (["OTHER"], 1, 1),
        (["SUITE"], 0, 0),
        (["CLOUD", "OTHER"], 1, 1),
        (["CLOUD", "SUITE"], 0, 0),
        (["OTHER", "SUITE"], 0, 0),
        (["CLOUD", "OTHER", "SUITE"], 0, 0),
    ],
)
@pytest.mark.user
async def test_aggregate_created_query_filtered(
    exclude: list, expected_count: int, expected_wikibase_count: int
):
    """Test Aggregate Created Query"""

    result = await test_schema.execute(
        AGGREGATED_CREATED_QUERY,
        variable_values={"wikibaseFilter": {"wikibaseType": {"exclude": exclude}}},
        context_value=get_mock_context("test-auth-token"),
    )

    assert result.errors is None
    assert result.data is not None

    assert_layered_property_count(result.data, ["aggregateCreated"], expected_count)
    if expected_count > 0:
        assert_layered_property_value(
            result.data,
            ["aggregateCreated", 0, "wikibaseCount"],
            expected_wikibase_count,
        )
