"""Test Aggregated Software Query"""

from datetime import datetime
import pytest
from tests.test_query.aggregation.software_version.assert_software_version_aggregate import (
    assert_software_version_aggregate,
)
from tests.test_query.aggregation.software_version.software_version_aggregate_fragment import (
    SOFTWARE_VERSION_DOUBLE_AGGREGATE_FRAGMENT,
)
from tests.test_schema import test_schema
from tests.utils import (
    assert_layered_property_count,
    assert_layered_property_value,
    assert_page_meta,
    get_mock_context,
)


AGGREGATE_SOFTWARE_QUERY = (
    """
query MyQuery($pageNumber: Int!, $pageSize: Int!, $wikibaseFilter: WikibaseFilterInput) {
  aggregateSoftwarePopularity(
    pageNumber: $pageNumber
    pageSize: $pageSize
    wikibaseFilter: $wikibaseFilter
  ) {
    ...WikibaseSoftwareVersionDoubleAggregatePageFragment
  }
}

"""
    + SOFTWARE_VERSION_DOUBLE_AGGREGATE_FRAGMENT
)


@pytest.mark.asyncio
@pytest.mark.agg
@pytest.mark.dependency(depends=["software-version-success"], scope="session")
@pytest.mark.query
@pytest.mark.version
async def test_aggregate_software_query():
    """Test Aggregated Software Query"""

    result = await test_schema.execute(
        AGGREGATE_SOFTWARE_QUERY,
        variable_values={"pageNumber": 1, "pageSize": 5},
        context_value=get_mock_context("test-auth-token"),
    )

    assert result.errors is None
    assert result.data is not None
    assert_page_meta(result.data["aggregateSoftwarePopularity"], 1, 5, 5, 1)
    assert_layered_property_count(
        result.data, ["aggregateSoftwarePopularity", "data"], 5
    )

    for index, (
        expected_software_name,
        expected_version_string,
        expected_version_semver,
        expected_version_date,
        expected_version_hash,
    ) in enumerate(
        [
            ("ICU", "60.2", (60, 2, None), None, None),
            ("Lua", "5.1.5", (5, 1, 5), None, None),
            ("MediaWiki", "1.39.8", (1, 39, 8), None, "fbca402"),
            ("MySQL", "1.35.8", (1, 35, 8), datetime(2022, 12, 13, 5, 50), "e43140f"),
            ("PHP", "7.2.24-0ubuntu0.18.04.3 (fpm-fcgi)", (7, 2, 24), None, None),
        ]
    ):

        assert_software_version_aggregate(
            result.data["aggregateSoftwarePopularity"]["data"][index],
            expected_software_name,
            expected_version_string,
            expected_version_semver,
            expected_version_date,
            expected_version_hash,
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
        ([], 5),
        (["CLOUD"], 5),
        (["OTHER"], 5),
        (["SUITE"], 0),
        (["CLOUD", "OTHER"], 5),
        (["CLOUD", "SUITE"], 0),
        (["OTHER", "SUITE"], 0),
        (["CLOUD", "OTHER", "SUITE"], 0),
    ],
)
@pytest.mark.version
async def test_aggregate_software_query_filtered(exclude: list, expected_count: int):
    """Test Aggregated Software Query"""

    result = await test_schema.execute(
        AGGREGATE_SOFTWARE_QUERY,
        variable_values={
            "pageNumber": 1,
            "pageSize": 1,
            "wikibaseFilter": {"wikibaseType": {"exclude": exclude}},
        },
        context_value=get_mock_context("test-auth-token"),
    )

    assert result.errors is None
    assert result.data is not None

    assert_layered_property_value(
        result.data,
        ["aggregateSoftwarePopularity", "meta", "totalCount"],
        expected_count,
    )
