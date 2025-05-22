"""Test Wikibase Most Recent Software Version Installed Libraries Observation Query"""

import pytest
from tests.test_query.wikibase.software_version_obs.assert_software_version import (
    assert_software_version,
)
from tests.test_query.wikibase.software_version_obs.software_version_fragment import (
    WIKIBASE_SOFTWARE_VERSION_FRAGMENT,
)
from tests.test_schema import test_schema
from tests.utils import assert_layered_property_count, assert_property_value


WIKIBASE_SOFTWARE_VERSION_MOST_RECENT_OBSERVATION_LIBRARIES_QUERY = (
    """
query MyQuery($wikibaseId: Int!) {
  wikibase(wikibaseId: $wikibaseId) {
    id
    softwareVersionObservations {
      mostRecent {
        id
        observationDate
        returnedData
        installedLibraries {
          ...WikibaseSoftwareVersionFragment
        }
      }
    }
  }
}

"""
    + WIKIBASE_SOFTWARE_VERSION_FRAGMENT
)


@pytest.mark.asyncio
@pytest.mark.dependency(depends=["software-version-success"], scope="session")
@pytest.mark.query
@pytest.mark.version
async def test_wikibase_software_version_most_recent_observation_libraries_query():
    """Test Wikibase Most Recent Software Version Installed Libraries Observation Query"""

    result = await test_schema.execute(
        WIKIBASE_SOFTWARE_VERSION_MOST_RECENT_OBSERVATION_LIBRARIES_QUERY,
        variable_values={"wikibaseId": 1},
    )

    assert result.errors is None
    assert result.data is not None
    assert "wikibase" in result.data
    result_wikibase = result.data["wikibase"]
    assert_property_value(result_wikibase, "id", "1")
    assert "softwareVersionObservations" in result_wikibase
    assert "mostRecent" in result_wikibase["softwareVersionObservations"]
    most_recent = result_wikibase["softwareVersionObservations"]["mostRecent"]

    assert_property_value(most_recent, "id", "1")
    assert "observationDate" in most_recent
    assert_property_value(most_recent, "returnedData", True)

    assert_layered_property_count(most_recent, ["installedLibraries"], 59)
    for index, (
        expected_id,
        expected_name,
        expected_version,
        expected_version_date,
        expected_version_hash,
    ) in enumerate(
        [
            ("20", "composer/installers", "1.8.0", None, None),
            ("21", "composer/semver", "1.5.0", None, None),
            ("22", "cssjanus/cssjanus", "1.3.0", None, None),
            ("23", "data-values/common", "0.4.3", None, None),
            ("24", "data-values/data-values", "2.3.0", None, None),
            ("25", "data-values/geo", "3.0.1", None, None),
            ("26", "data-values/interfaces", "0.2.5", None, None),
            ("27", "data-values/number", "0.10.1", None, None),
            ("28", "data-values/serialization", "1.2.3", None, None),
            ("29", "data-values/time", "1.0.1", None, None),
            ("30", "diff/diff", "2.3.0", None, None),
            ("31", "guzzlehttp/guzzle", "6.3.3", None, None),
            ("32", "guzzlehttp/promises", "1.3.1", None, None),
            ("33", "guzzlehttp/psr7", "1.6.1", None, None),
            ("34", "liuggio/statsd-php-client", "1.0.18", None, None),
            ("35", "onoi/message-reporter", "1.4.1", None, None),
            ("36", "oojs/oojs-ui", "0.34.1", None, None),
            ("37", "pear/console_getopt", "1.4.3", None, None),
            ("38", "pear/mail", "1.4.1", None, None),
            ("39", "pear/mail_mime", "1.10.2", None, None),
            ("40", "pear/net_smtp", "1.8.1", None, None),
            ("41", "pear/net_socket", "1.2.2", None, None),
            ("42", "pear/pear-core-minimal", "1.10.10", None, None),
            ("43", "pear/pear_exception", "1.0.1", None, None),
            ("44", "pleonasm/bloom-filter", "1.0.2", None, None),
            ("45", "psr/container", "1.0.0", None, None),
            ("46", "psr/http-message", "1.0.1", None, None),
            ("47", "psr/log", "1.0.2", None, None),
            ("48", "psr/simple-cache", "1.0.1", None, None),
            ("49", "ralouphie/getallheaders", "3.0.3", None, None),
            ("50", "serialization/serialization", "4.0.0", None, None),
            ("51", "wikibase/data-model", "9.2.0", None, None),
            ("52", "wikibase/data-model-serialization", "2.9.1", None, None),
            ("53", "wikibase/data-model-services", "3.15.0", None, None),
            ("54", "wikibase/internal-serialization", "2.10.0", None, None),
            ("55", "wikibase/term-store", "1.0.4", None, None),
            ("56", "wikimedia/assert", "0.2.2", None, None),
            ("57", "wikimedia/at-ease", "2.0.0", None, None),
            ("58", "wikimedia/base-convert", "2.0.0", None, None),
            ("59", "wikimedia/cdb", "1.4.1", None, None),
            ("60", "wikimedia/cldr-plural-rule-parser", "1.0.0", None, None),
            ("61", "wikimedia/composer-merge-plugin", "1.4.1", None, None),
            ("62", "wikimedia/html-formatter", "1.0.2", None, None),
            ("63", "wikimedia/ip-set", "2.1.0", None, None),
            ("64", "wikimedia/less.php", "1.8.0", None, None),
            ("65", "wikimedia/object-factory", "2.1.0", None, None),
            ("66", "wikimedia/password-blacklist", "0.1.4", None, None),
            ("67", "wikimedia/php-session-serializer", "1.0.7", None, None),
            ("68", "wikimedia/purtle", "1.0.7", None, None),
            ("69", "wikimedia/relpath", "2.1.1", None, None),
            ("70", "wikimedia/remex-html", "2.1.0", None, None),
            ("71", "wikimedia/running-stat", "1.2.1", None, None),
            ("72", "wikimedia/scoped-callback", "3.0.0", None, None),
            ("73", "wikimedia/timestamp", "3.0.0", None, None),
            ("74", "wikimedia/utfnormal", "2.0.0", None, None),
            ("75", "wikimedia/wait-condition-loop", "1.0.1", None, None),
            ("76", "wikimedia/wrappedstring", "3.0.1", None, None),
            ("77", "wikimedia/xmp-reader", "0.6.3", None, None),
            ("78", "zordius/lightncandy", "0.23", None, None),
        ]
    ):
        assert_software_version(
            most_recent["installedLibraries"][index],
            expected_id,
            expected_name,
            expected_version,
            expected_version_date,
            expected_version_hash,
        )
