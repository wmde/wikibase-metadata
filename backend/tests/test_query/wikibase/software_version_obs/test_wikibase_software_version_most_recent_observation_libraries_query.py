"""Test Wikibase Most Recent Software Version Installed Libraries Observation Query"""

from datetime import datetime, timezone

import pytest
from data.database_connection import get_async_session
from model.database.wikibase_model import WikibaseModel
from model.database.wikibase_observation.version.software_version_model import WikibaseSoftwareVersionModel
from model.database.wikibase_observation.version.wikibase_version_observation_model import WikibaseSoftwareVersionObservationModel
from model.database.wikibase_software.software_model import WikibaseSoftwareModel
from model.enum.wikibase_software_type_enum import WikibaseSoftwareType
from tests.test_query.wikibase.software_version_obs.assert_software_version import (
    assert_software_version,
)
from tests.test_query.wikibase.software_version_obs.software_version_fragment import (
    WIKIBASE_SOFTWARE_VERSION_FRAGMENT,
)
from tests.test_schema import test_schema
from tests.utils import assert_layered_property_count, assert_property_value

WIKIBASE_SOFTWARE_VERSION_MOST_RECENT_OBSERVATION_LIBRARIES_QUERY = """
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

""" + WIKIBASE_SOFTWARE_VERSION_FRAGMENT

@pytest.fixture
async def wikibase_with_libraries_observation(db_session): # pylint: disable=unused-argument
    """Create a wikibase with software version observation containing 59 libraries"""
    async with get_async_session() as session:
        library_data = [
            ("composer/installers", "1.8.0"),
            ("composer/semver", "1.5.0"),
            ("cssjanus/cssjanus", "1.3.0"),
            ("data-values/common", "0.4.3"),
            ("data-values/data-values", "2.3.0"),
            ("data-values/geo", "3.0.1"),
            ("data-values/interfaces", "0.2.5"),
            ("data-values/number", "0.10.1"),
            ("data-values/serialization", "1.2.3"),
            ("data-values/time", "1.0.1"),
            ("diff/diff", "2.3.0"),
            ("guzzlehttp/guzzle", "6.3.3"),
            ("guzzlehttp/promises", "1.3.1"),
            ("guzzlehttp/psr7", "1.6.1"),
            ("liuggio/statsd-php-client", "1.0.18"),
            ("onoi/message-reporter", "1.4.1"),
            ("oojs/oojs-ui", "0.34.1"),
            ("pear/console_getopt", "1.4.3"),
            ("pear/mail", "1.4.1"),
            ("pear/mail_mime", "1.10.2"),
            ("pear/net_smtp", "1.8.1"),
            ("pear/net_socket", "1.2.2"),
            ("pear/pear-core-minimal", "1.10.10"),
            ("pear/pear_exception", "1.0.1"),
            ("pleonasm/bloom-filter", "1.0.2"),
            ("psr/container", "1.0.0"),
            ("psr/http-message", "1.0.1"),
            ("psr/log", "1.0.2"),
            ("psr/simple-cache", "1.0.1"),
            ("ralouphie/getallheaders", "3.0.3"),
            ("serialization/serialization", "4.0.0"),
            ("wikibase/data-model", "9.2.0"),
            ("wikibase/data-model-serialization", "2.9.1"),
            ("wikibase/data-model-services", "3.15.0"),
            ("wikibase/internal-serialization", "2.10.0"),
            ("wikibase/term-store", "1.0.4"),
            ("wikimedia/assert", "0.2.2"),
            ("wikimedia/at-ease", "2.0.0"),
            ("wikimedia/base-convert", "2.0.0"),
            ("wikimedia/cdb", "1.4.1"),
            ("wikimedia/cldr-plural-rule-parser", "1.0.0"),
            ("wikimedia/composer-merge-plugin", "1.4.1"),
            ("wikimedia/html-formatter", "1.0.2"),
            ("wikimedia/ip-set", "2.1.0"),
            ("wikimedia/less.php", "1.8.0"),
            ("wikimedia/object-factory", "2.1.0"),
            ("wikimedia/password-blacklist", "0.1.4"),
            ("wikimedia/php-session-serializer", "1.0.7"),
            ("wikimedia/purtle", "1.0.7"),
            ("wikimedia/relpath", "2.1.1"),
            ("wikimedia/remex-html", "2.1.0"),
            ("wikimedia/running-stat", "1.2.1"),
            ("wikimedia/scoped-callback", "3.0.0"),
            ("wikimedia/timestamp", "3.0.0"),
            ("wikimedia/utfnormal", "2.0.0"),
            ("wikimedia/wait-condition-loop", "1.0.1"),
            ("wikimedia/wrappedstring", "3.0.1"),
            ("wikimedia/xmp-reader", "0.6.3"),
            ("zordius/lightncandy", "0.23"),
        ]

        lib_models = {}
        for name, _ in library_data:
            software = WikibaseSoftwareModel(
                software_type=WikibaseSoftwareType.LIBRARY,
                software_name=name,
            )
            session.add(software)
            await session.flush()
            await session.refresh(software)
            lib_models[name] = software

        wikibase = WikibaseModel(
            wikibase_name="Libraries Test Wikibase",
            base_url="https://libraries-test-example.com",
        )
        wikibase.checked = True
        wikibase.reuse = True
        wikibase.test = False
        wikibase.wikibase_type = None
        session.add(wikibase)
        await session.flush()
        await session.refresh(wikibase)

        obs = WikibaseSoftwareVersionObservationModel()
        obs.wikibase_id = wikibase.id
        obs.returned_data = True
        obs.observation_date = datetime(2024, 3, 1, tzinfo=timezone.utc)
        session.add(obs)
        await session.flush()
        await session.refresh(obs)

        sv_ids = {}
        for name, version in library_data:
            sv = WikibaseSoftwareVersionModel(software=lib_models[name], version=version)
            sv.wikibase_software_version_observation_id = obs.id
            session.add(sv)
            await session.flush()
            await session.refresh(sv)
            sv_ids[name] = str(sv.id)

        wikibase_id = wikibase.id
        observation_id = str(obs.id)
    return wikibase_id, observation_id, sv_ids

@pytest.mark.asyncio
@pytest.mark.query
@pytest.mark.version
async def test_wikibase_software_version_most_recent_observation_libraries_query(wikibase_with_libraries_observation): # pylint: disable=redefined-outer-name
    """Test Wikibase Most Recent Software Version Installed Libraries Observation Query"""

    wikibase_id, obs_id, sv_ids = wikibase_with_libraries_observation
    result = await test_schema.execute(
        WIKIBASE_SOFTWARE_VERSION_MOST_RECENT_OBSERVATION_LIBRARIES_QUERY,
        variable_values={"wikibaseId": wikibase_id},
    )

    assert result.errors is None
    assert result.data is not None
    assert "wikibase" in result.data
    result_wikibase = result.data["wikibase"]
    assert_property_value(result_wikibase, "id", str(wikibase_id))
    assert "softwareVersionObservations" in result_wikibase
    assert "mostRecent" in result_wikibase["softwareVersionObservations"]
    most_recent = result_wikibase["softwareVersionObservations"]["mostRecent"]

    assert_property_value(most_recent, "id", str(obs_id))
    assert "observationDate" in most_recent
    assert_property_value(most_recent, "returnedData", True)

    assert_layered_property_count(most_recent, ["installedLibraries"], 59)
    for index, (
        expected_name,
        expected_version,
        expected_version_date,
        expected_version_hash,
    ) in enumerate(
        [
            ("composer/installers", "1.8.0", None, None),
            ("composer/semver", "1.5.0", None, None),
            ("cssjanus/cssjanus", "1.3.0", None, None),
            ("data-values/common", "0.4.3", None, None),
            ("data-values/data-values", "2.3.0", None, None),
            ("data-values/geo", "3.0.1", None, None),
            ("data-values/interfaces", "0.2.5", None, None),
            ("data-values/number", "0.10.1", None, None),
            ("data-values/serialization", "1.2.3", None, None),
            ("data-values/time", "1.0.1", None, None),
            ("diff/diff", "2.3.0", None, None),
            ("guzzlehttp/guzzle", "6.3.3", None, None),
            ("guzzlehttp/promises", "1.3.1", None, None),
            ("guzzlehttp/psr7", "1.6.1", None, None),
            ("liuggio/statsd-php-client", "1.0.18", None, None),
            ("onoi/message-reporter", "1.4.1", None, None),
            ("oojs/oojs-ui", "0.34.1", None, None),
            ("pear/console_getopt", "1.4.3", None, None),
            ("pear/mail", "1.4.1", None, None),
            ("pear/mail_mime", "1.10.2", None, None),
            ("pear/net_smtp", "1.8.1", None, None),
            ("pear/net_socket", "1.2.2", None, None),
            ("pear/pear-core-minimal", "1.10.10", None, None),
            ("pear/pear_exception", "1.0.1", None, None),
            ("pleonasm/bloom-filter", "1.0.2", None, None),
            ("psr/container", "1.0.0", None, None),
            ("psr/http-message", "1.0.1", None, None),
            ("psr/log", "1.0.2", None, None),
            ("psr/simple-cache", "1.0.1", None, None),
            ("ralouphie/getallheaders", "3.0.3", None, None),
            ("serialization/serialization", "4.0.0", None, None),
            ("wikibase/data-model", "9.2.0", None, None),
            ("wikibase/data-model-serialization", "2.9.1", None, None),
            ("wikibase/data-model-services", "3.15.0", None, None),
            ("wikibase/internal-serialization", "2.10.0", None, None),
            ("wikibase/term-store", "1.0.4", None, None),
            ("wikimedia/assert", "0.2.2", None, None),
            ("wikimedia/at-ease", "2.0.0", None, None),
            ("wikimedia/base-convert", "2.0.0", None, None),
            ("wikimedia/cdb", "1.4.1", None, None),
            ("wikimedia/cldr-plural-rule-parser", "1.0.0", None, None),
            ("wikimedia/composer-merge-plugin", "1.4.1", None, None),
            ("wikimedia/html-formatter", "1.0.2", None, None),
            ("wikimedia/ip-set", "2.1.0", None, None),
            ("wikimedia/less.php", "1.8.0", None, None),
            ("wikimedia/object-factory", "2.1.0", None, None),
            ("wikimedia/password-blacklist", "0.1.4", None, None),
            ("wikimedia/php-session-serializer", "1.0.7", None, None),
            ("wikimedia/purtle", "1.0.7", None, None),
            ("wikimedia/relpath", "2.1.1", None, None),
            ("wikimedia/remex-html", "2.1.0", None, None),
            ("wikimedia/running-stat", "1.2.1", None, None),
            ("wikimedia/scoped-callback", "3.0.0", None, None),
            ("wikimedia/timestamp", "3.0.0", None, None),
            ("wikimedia/utfnormal", "2.0.0", None, None),
            ("wikimedia/wait-condition-loop", "1.0.1", None, None),
            ("wikimedia/wrappedstring", "3.0.1", None, None),
            ("wikimedia/xmp-reader", "0.6.3", None, None),
            ("zordius/lightncandy", "0.23", None, None),
        ]
    ):
        assert_software_version(
            most_recent["installedLibraries"][index],
            expected_name,
            expected_version,
            expected_version_date,
            expected_version_hash,
        )
