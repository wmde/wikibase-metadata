"""Test Aggregated Extensions Query"""

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
    assert_page_meta,
    get_mock_context,
)


AGGREGATE_EXTENSIONS_QUERY = (
    """
query MyQuery($pageNumber: Int!, $pageSize: Int!) {
  aggregateExtensionPopularity(pageNumber: $pageNumber, pageSize: $pageSize) {
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
async def test_aggregate_extensions_query_page_one():
    """Test Aggregated Extensions Query - 1-5"""

    result = await test_schema.execute(
        AGGREGATE_EXTENSIONS_QUERY,
        variable_values={"pageNumber": 1, "pageSize": 5},
        context_value=get_mock_context("test-auth-token"),
    )

    assert result.errors is None
    assert result.data is not None
    assert_page_meta(result.data["aggregateExtensionPopularity"], 1, 5, 11, 3)
    assert_layered_property_count(
        result.data, ["aggregateExtensionPopularity", "data"], 5
    )

    for index, (
        expected_software_name,
        expected_version_string,
        expected_version_semver,
        expected_version_date,
        expected_version_hash,
    ) in enumerate(
        [
            ("Babel", "1.11.1", (1, 11, 1), None, None),
            (
                "Google Analytics Integration",
                "3.0.1",
                (3, 0, 1),
                datetime(2019, 8, 6, 9, 12),
                "6441403",
            ),
            (
                "LabeledSectionTransclusion",
                "f621799",
                (None, None, None),
                datetime(2020, 1, 29, 14, 52),
                "f621799",
            ),
            (
                "Miraheze Magic",
                "e742444",
                (None, None, None),
                datetime(2024, 10, 17, 15, 21),
                "e742444",
            ),
            (
                "ProofreadPage",
                "cb0a218",
                (None, None, None),
                datetime(2019, 9, 30, 9, 20),
                "cb0a218",
            ),
        ]
    ):

        assert_software_version_aggregate(
            result.data["aggregateExtensionPopularity"]["data"][index],
            expected_software_name,
            expected_version_string,
            expected_version_semver,
            expected_version_date,
            expected_version_hash,
        )


@pytest.mark.asyncio
@pytest.mark.agg
@pytest.mark.dependency(depends=["software-version-success"], scope="session")
@pytest.mark.query
@pytest.mark.version
async def test_aggregate_extensions_query_page_two():
    """Test Aggregated Extensions Query - 6-10"""

    result = await test_schema.execute(
        AGGREGATE_EXTENSIONS_QUERY,
        variable_values={"pageNumber": 2, "pageSize": 5},
        context_value=get_mock_context("test-auth-token"),
    )

    assert result.errors is None
    assert result.data is not None
    assert_page_meta(result.data["aggregateExtensionPopularity"], 2, 5, 11, 3)
    assert_layered_property_count(
        result.data, ["aggregateExtensionPopularity", "data"], 5
    )

    for index, (
        expected_software_name,
        expected_version_string,
        expected_version_semver,
        expected_version_date,
        expected_version_hash,
    ) in enumerate(
        [
            ("Scribunto", None, (None, None, None), None, None),
            (
                "UniversalLanguageSelector",
                "2020-01-23",
                (None, None, None),
                datetime(2020, 3, 3, 13, 38),
                "61f1a98",
            ),
            (
                "WikibaseClient",
                "dbbcdd8",
                (None, None, None),
                datetime(2019, 12, 10, 12, 52),
                "dbbcdd8",
            ),
            (
                "WikibaseLib",
                "dbbcdd8",
                (None, None, None),
                datetime(2019, 12, 10, 12, 52),
                "dbbcdd8",
            ),
            (
                "WikibaseRepository",
                "dbbcdd8",
                (None, None, None),
                datetime(2019, 12, 10, 12, 52),
                "dbbcdd8",
            ),
        ]
    ):

        assert_software_version_aggregate(
            result.data["aggregateExtensionPopularity"]["data"][index],
            expected_software_name,
            expected_version_string,
            expected_version_semver,
            expected_version_date,
            expected_version_hash,
        )


@pytest.mark.asyncio
@pytest.mark.agg
@pytest.mark.dependency(depends=["software-version-success"], scope="session")
@pytest.mark.query
@pytest.mark.version
async def test_aggregate_extensions_query_page_three():
    """Test Aggregated Extensions Query - 11"""

    result = await test_schema.execute(
        AGGREGATE_EXTENSIONS_QUERY,
        variable_values={"pageNumber": 3, "pageSize": 5},
        context_value=get_mock_context("test-auth-token"),
    )

    assert result.errors is None
    assert result.data is not None
    assert_page_meta(result.data["aggregateExtensionPopularity"], 3, 5, 11, 3)
    assert_layered_property_count(
        result.data, ["aggregateExtensionPopularity", "data"], 1
    )

    for index, (
        expected_software_name,
        expected_version_string,
        expected_version_semver,
        expected_version_date,
        expected_version_hash,
    ) in enumerate(
        [
            (
                "WikibaseView",
                "dbbcdd8",
                (None, None, None),
                datetime(2019, 12, 10, 12, 52),
                "dbbcdd8",
            ),
        ]
    ):

        assert_software_version_aggregate(
            result.data["aggregateExtensionPopularity"]["data"][index],
            expected_software_name,
            expected_version_string,
            expected_version_semver,
            expected_version_date,
            expected_version_hash,
        )
