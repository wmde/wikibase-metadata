"""Test Wikibase Most Recent Software Version Installed Skins Observation Query"""

import pytest
from tests.test_query.test_wikibase_software_version_observation_query.assert_software_version import (
    assert_software_version,
)
from tests.test_query.test_wikibase_software_version_observation_query.wikibase_software_version_observation_fragment import (
    WIKIBASE_SOFTWARE_VERSION_FRAGMENT,
)
from tests.test_schema import test_schema
from tests.utils import assert_layered_property_count, assert_property_value


WIKIBASE_SOFTWARE_VERSION_MOST_RECENT_OBSERVATION_SKINS_QUERY = (
    """
query MyQuery($wikibaseId: Int!) {
  wikibase(wikibaseId: $wikibaseId) {
    id
    softwareVersionObservations {
      mostRecent {
        id
        observationDate
        returnedData
        installedSkins {
          ...WikibaseSoftwareVersionStrawberryModelFragment
        }
      }
    }
  }
}

"""
    + WIKIBASE_SOFTWARE_VERSION_FRAGMENT
)


@pytest.mark.asyncio
@pytest.mark.dependency(depends_on=["software-version-success"])
@pytest.mark.query
@pytest.mark.version
async def test_wikibase_software_version_most_recent_observation_skins_query():
    """Test Wikibase Most Recent Software Version Installed Skins Observation Query"""

    result = await test_schema.execute(
        WIKIBASE_SOFTWARE_VERSION_MOST_RECENT_OBSERVATION_SKINS_QUERY,
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

    assert_layered_property_count(most_recent, ["installedSkins"], 3)
    for index, (
        expected_id,
        expected_name,
        expected_version,
        expected_version_date,
        expected_version_hash,
    ) in enumerate(
        [
            ("6", "MonoBook", None, None, None),
            ("7", "Timeless", "0.8.9", None, None),
            ("8", "Vector", None, None, None),
        ]
    ):
        assert_software_version(
            most_recent["installedSkins"][index],
            expected_id,
            expected_name,
            expected_version,
            expected_version_date,
            expected_version_hash,
        )
