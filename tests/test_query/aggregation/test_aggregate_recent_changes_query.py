"""Test Aggregate Recent Changes Query"""

import pytest
from tests.test_schema import test_schema
from tests.utils import assert_layered_property_value


AGGREGATED_RECENT_CHANGES_QUERY = """
query MyQuery($wikibaseFilter: WikibaseFilterInput) {
  aggregateRecentChanges(wikibaseFilter: $wikibaseFilter) {
    humanChangeCount
    humanChangeUserCount
    humanChangeActiveUserCount
    botChangeCount
    botChangeUserCount
    botChangeActiveUserCount
    wikibaseCount
  }
}
"""


@pytest.mark.asyncio
@pytest.mark.agg
@pytest.mark.query
@pytest.mark.dependency(depends=["recent-changes-success-ood"], scope="session")
async def test_aggregate_recent_changes_query():
    """Test Aggregate Recent Changes Query"""

    result = await test_schema.execute(AGGREGATED_RECENT_CHANGES_QUERY)

    assert result.errors is None
    assert result.data is not None

    assert_layered_property_value(
        result.data, ["aggregateRecentChanges", "humanChangeCount"], 10
    )
    assert_layered_property_value(
        result.data, ["aggregateRecentChanges", "humanChangeUserCount"], 5
    )
    assert_layered_property_value(
        result.data, ["aggregateRecentChanges", "humanChangeActiveUserCount"], 1
    )
    assert_layered_property_value(
        result.data, ["aggregateRecentChanges", "botChangeCount"], 6
    )
    assert_layered_property_value(
        result.data, ["aggregateRecentChanges", "botChangeUserCount"], 2
    )
    assert_layered_property_value(
        result.data, ["aggregateRecentChanges", "botChangeActiveUserCount"], 1
    )
    assert_layered_property_value(
        result.data, ["aggregateRecentChanges", "wikibaseCount"], 1
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
async def test_aggregate_recent_changes_query_filtered(
    exclude: list, expected_count: int
):
    """Test Aggregate Recent Changes Query with Filter"""

    result = await test_schema.execute(
        AGGREGATED_RECENT_CHANGES_QUERY,
        variable_values={"wikibaseFilter": {"wikibaseType": {"exclude": exclude}}},
    )

    assert result.errors is None
    assert result.data is not None

    assert_layered_property_value(
        result.data, ["aggregateRecentChanges", "wikibaseCount"], expected_count
    )
