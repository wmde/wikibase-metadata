"""Test Wikibase All Software Versions Observations Query"""

import pytest
from tests.test_query.wikibase.software_version_obs.software_version_fragment import (
    WIKIBASE_SOFTWARE_VERSION_OBSERVATIONS_FRAGMENT,
)
from tests.test_schema import test_schema
from tests.utils import assert_layered_property_value, assert_property_value


WIKIBASE_SOFTWARE_VERSION_ALL_OBSERVATIONS_QUERY = (
    """
query MyQuery($wikibaseId: Int!) {
  wikibase(wikibaseId: $wikibaseId) {
    id
    softwareVersionObservations {
      allObservations {
        ...WikibaseSoftwareVersionObservationFragment
      }
    }
  }
}

"""
    + WIKIBASE_SOFTWARE_VERSION_OBSERVATIONS_FRAGMENT
)


@pytest.mark.asyncio
@pytest.mark.dependency(
    depends=["software-version-success", "software-version-failure"], scope="session"
)
@pytest.mark.query
@pytest.mark.version
async def test_wikibase_software_version_all_observations_query():
    """Test Wikibase All Software Version Observations"""

    result = await test_schema.execute(
        WIKIBASE_SOFTWARE_VERSION_ALL_OBSERVATIONS_QUERY,
        variable_values={"wikibaseId": 1},
    )

    assert result.errors is None
    assert result.data is not None
    assert "wikibase" in result.data
    result_wikibase = result.data["wikibase"]
    assert_property_value(result_wikibase, "id", "1")
    assert "softwareVersionObservations" in result_wikibase

    assert "allObservations" in result_wikibase["softwareVersionObservations"]
    assert (
        len(
            software_version_observation_list := result_wikibase[
                "softwareVersionObservations"
            ]["allObservations"]
        )
        == 2
    )

    assert_layered_property_value(software_version_observation_list, [0, "id"], "1")
    assert "observationDate" in software_version_observation_list[0]
    assert_layered_property_value(
        software_version_observation_list, [0, "returnedData"], True
    )

    assert_layered_property_value(software_version_observation_list, [1, "id"], "2")
    assert "observationDate" in software_version_observation_list[1]
    assert_layered_property_value(
        software_version_observation_list, [1, "returnedData"], False
    )
