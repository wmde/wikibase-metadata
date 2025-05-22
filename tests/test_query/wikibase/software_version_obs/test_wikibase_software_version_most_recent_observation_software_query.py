"""Test Wikibase Most Recent Software Version Installed Software Observation Query"""

from datetime import datetime
import pytest
from tests.test_query.wikibase.software_version_obs.assert_software_version import (
    assert_software_version,
)
from tests.test_query.wikibase.software_version_obs.software_version_fragment import (
    WIKIBASE_SOFTWARE_VERSION_FRAGMENT,
)
from tests.test_schema import test_schema
from tests.utils import assert_layered_property_count, assert_property_value


WIKIBASE_SOFTWARE_VERSION_MOST_RECENT_OBSERVATION_SOFTWARE_QUERY = (
    """
query MyQuery($wikibaseId: Int!) {
  wikibase(wikibaseId: $wikibaseId) {
    id
    softwareVersionObservations {
      mostRecent {
        id
        observationDate
        returnedData
        installedSoftware {
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
async def test_wikibase_software_version_most_recent_observation_software_query():
    """Test Wikibase Most Recent Software Version Installed Software Observation Query"""

    result = await test_schema.execute(
        WIKIBASE_SOFTWARE_VERSION_MOST_RECENT_OBSERVATION_SOFTWARE_QUERY,
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

    assert_layered_property_count(most_recent, ["installedSoftware"], 5)
    for index, (
        expected_id,
        expected_name,
        expected_version,
        expected_version_date,
        expected_version_hash,
    ) in enumerate(
        [
            ("4", "ICU", "60.2", None, None),
            ("5", "Lua", "5.1.5", None, None),
            ("1", "MediaWiki", "1.39.8", None, "fbca402"),
            ("3", "MySQL", "1.35.8", datetime(2022, 12, 13, 5, 50), "e43140f"),
            ("2", "PHP", "7.2.24-0ubuntu0.18.04.3 (fpm-fcgi)", None, None),
        ]
    ):
        assert_software_version(
            most_recent["installedSoftware"][index],
            expected_id,
            expected_name,
            expected_version,
            expected_version_date,
            expected_version_hash,
        )
