"""Test Aggregate Libraries Query"""

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


AGGREGATE_LIBRARIES_QUERY = (
    """
query MyQuery($pageNumber: Int!, $pageSize: Int!) {
  aggregateLibraryPopularity(pageNumber: $pageNumber, pageSize: $pageSize) {
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
async def test_aggregate_libraries_query_page_one():
    """Test Aggregated Libraries Query - 1-30"""

    result = await test_schema.execute(
        AGGREGATE_LIBRARIES_QUERY,
        variable_values={"pageNumber": 1, "pageSize": 30},
        context_value=get_mock_context("test-auth-token"),
    )

    assert result.errors is None
    assert result.data is not None
    assert_page_meta(result.data["aggregateLibraryPopularity"], 1, 30, 59, 2)
    assert_layered_property_count(
        result.data, ["aggregateLibraryPopularity", "data"], 30
    )

    for index, (
        expected_software_name,
        expected_version_string,
        expected_version_semver,
    ) in enumerate(
        [
            ("composer/installers", "1.8.0", (1, 8, 0)),
            ("composer/semver", "1.5.0", (1, 5, 0)),
            ("cssjanus/cssjanus", "1.3.0", (1, 3, 0)),
            ("data-values/common", "0.4.3", (0, 4, 3)),
            ("data-values/data-values", "2.3.0", (2, 3, 0)),
            ("data-values/geo", "3.0.1", (3, 0, 1)),
            ("data-values/interfaces", "0.2.5", (0, 2, 5)),
            ("data-values/number", "0.10.1", (0, 10, 1)),
            ("data-values/serialization", "1.2.3", (1, 2, 3)),
            ("data-values/time", "1.0.1", (1, 0, 1)),
            ("diff/diff", "2.3.0", (2, 3, 0)),
            ("guzzlehttp/guzzle", "6.3.3", (6, 3, 3)),
            ("guzzlehttp/promises", "1.3.1", (1, 3, 1)),
            ("guzzlehttp/psr7", "1.6.1", (1, 6, 1)),
            ("liuggio/statsd-php-client", "1.0.18", (1, 0, 18)),
            ("onoi/message-reporter", "1.4.1", (1, 4, 1)),
            ("oojs/oojs-ui", "0.34.1", (0, 34, 1)),
            ("pear/console_getopt", "1.4.3", (1, 4, 3)),
            ("pear/mail", "1.4.1", (1, 4, 1)),
            ("pear/mail_mime", "1.10.2", (1, 10, 2)),
            ("pear/net_smtp", "1.8.1", (1, 8, 1)),
            ("pear/net_socket", "1.2.2", (1, 2, 2)),
            ("pear/pear-core-minimal", "1.10.10", (1, 10, 10)),
            ("pear/pear_exception", "1.0.1", (1, 0, 1)),
            ("pleonasm/bloom-filter", "1.0.2", (1, 0, 2)),
            ("psr/container", "1.0.0", (1, 0, 0)),
            ("psr/http-message", "1.0.1", (1, 0, 1)),
            ("psr/log", "1.0.2", (1, 0, 2)),
            ("psr/simple-cache", "1.0.1", (1, 0, 1)),
            ("ralouphie/getallheaders", "3.0.3", (3, 0, 3)),
        ]
    ):

        assert_software_version_aggregate(
            result.data["aggregateLibraryPopularity"]["data"][index],
            expected_software_name,
            expected_version_string,
            expected_version_semver,
            None,
            None,
        )


@pytest.mark.asyncio
@pytest.mark.agg
@pytest.mark.dependency(depends=["software-version-success"], scope="session")
@pytest.mark.query
@pytest.mark.version
async def test_aggregate_libraries_query_page_two():
    """Test Aggregated libraries Query - 31-59"""

    result = await test_schema.execute(
        AGGREGATE_LIBRARIES_QUERY,
        variable_values={"pageNumber": 2, "pageSize": 30},
        context_value=get_mock_context("test-auth-token"),
    )

    assert result.errors is None
    assert result.data is not None
    assert_page_meta(result.data["aggregateLibraryPopularity"], 2, 30, 59, 2)
    assert_layered_property_count(
        result.data, ["aggregateLibraryPopularity", "data"], 29
    )

    for index, (
        expected_software_name,
        expected_version_string,
        expected_version_semver,
    ) in enumerate(
        [
            ("serialization/serialization", "4.0.0", (4, 0, 0)),
            ("wikibase/data-model", "9.2.0", (9, 2, 0)),
            ("wikibase/data-model-serialization", "2.9.1", (2, 9, 1)),
            ("wikibase/data-model-services", "3.15.0", (3, 15, 0)),
            ("wikibase/internal-serialization", "2.10.0", (2, 10, 0)),
            ("wikibase/term-store", "1.0.4", (1, 0, 4)),
            ("wikimedia/assert", "0.2.2", (0, 2, 2)),
            ("wikimedia/at-ease", "2.0.0", (2, 0, 0)),
            ("wikimedia/base-convert", "2.0.0", (2, 0, 0)),
            ("wikimedia/cdb", "1.4.1", (1, 4, 1)),
            ("wikimedia/cldr-plural-rule-parser", "1.0.0", (1, 0, 0)),
            ("wikimedia/composer-merge-plugin", "1.4.1", (1, 4, 1)),
            ("wikimedia/html-formatter", "1.0.2", (1, 0, 2)),
            ("wikimedia/ip-set", "2.1.0", (2, 1, 0)),
            ("wikimedia/less.php", "1.8.0", (1, 8, 0)),
            ("wikimedia/object-factory", "2.1.0", (2, 1, 0)),
            ("wikimedia/password-blacklist", "0.1.4", (0, 1, 4)),
            ("wikimedia/php-session-serializer", "1.0.7", (1, 0, 7)),
            ("wikimedia/purtle", "1.0.7", (1, 0, 7)),
            ("wikimedia/relpath", "2.1.1", (2, 1, 1)),
            ("wikimedia/remex-html", "2.1.0", (2, 1, 0)),
            ("wikimedia/running-stat", "1.2.1", (1, 2, 1)),
            ("wikimedia/scoped-callback", "3.0.0", (3, 0, 0)),
            ("wikimedia/timestamp", "3.0.0", (3, 0, 0)),
            ("wikimedia/utfnormal", "2.0.0", (2, 0, 0)),
            ("wikimedia/wait-condition-loop", "1.0.1", (1, 0, 1)),
            ("wikimedia/wrappedstring", "3.0.1", (3, 0, 1)),
            ("wikimedia/xmp-reader", "0.6.3", (0, 6, 3)),
            ("zordius/lightncandy", "0.23", (0, 23, None)),
        ]
    ):

        assert_software_version_aggregate(
            result.data["aggregateLibraryPopularity"]["data"][index],
            expected_software_name,
            expected_version_string,
            expected_version_semver,
            None,
            None,
        )
