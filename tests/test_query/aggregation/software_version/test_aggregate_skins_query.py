"""Test Aggregated Skins Query"""

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


AGGREGATE_SKINS_QUERY = (
    """
query MyQuery($pageNumber: Int!, $pageSize: Int!, $wikibaseFilter: WikibaseFilterInput) {
  aggregateSkinPopularity(
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
async def test_aggregate_skins_query_page_one():
    """Test Aggregated Skins Query"""

    result = await test_schema.execute(
        AGGREGATE_SKINS_QUERY, variable_values={"pageNumber": 1, "pageSize": 5}
    )

    assert result.errors is None
    assert result.data is not None
    assert_page_meta(result.data["aggregateSkinPopularity"], 1, 5, 3, 1)
    assert_layered_property_count(result.data, ["aggregateSkinPopularity", "data"], 3)

    for index, (
        expected_software_name,
        expected_version_string,
        expected_version_semver,
    ) in enumerate(
        [
            ("MonoBook", None, (None, None, None)),
            ("Timeless", "0.8.9", (0, 8, 9)),
            ("Vector", None, (None, None, None)),
        ]
    ):

        assert_software_version_aggregate(
            result.data["aggregateSkinPopularity"]["data"][index],
            expected_software_name,
            1,
            expected_version_string,
            expected_version_semver,
            None,
            None,
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
        ([], 3),
        (["CLOUD"], 3),
        (["OTHER"], 3),
        (["SUITE"], 0),
        (["CLOUD", "OTHER"], 3),
        (["CLOUD", "SUITE"], 0),
        (["OTHER", "SUITE"], 0),
        (["CLOUD", "OTHER", "SUITE"], 0),
    ],
)
@pytest.mark.user
async def test_aggregate_users_query_filtered(exclude: list, expected_count: int):
    """Test Aggregate Users Query"""

    result = await test_schema.execute(
        AGGREGATE_SKINS_QUERY,
        variable_values={
            "pageNumber": 1,
            "pageSize": 1,
            "wikibaseFilter": {"wikibaseType": {"exclude": exclude}},
        },
    )

    assert result.errors is None
    assert result.data is not None

    assert_layered_property_value(
        result.data, ["aggregateSkinPopularity", "meta", "totalCount"], expected_count
    )
