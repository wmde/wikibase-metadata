"""Test Wikibase All Software Versions Observations Query"""

from datetime import datetime, timezone

import pytest
from data.database_connection import get_async_session
from model.database.wikibase_model import WikibaseModel
from model.database.wikibase_observation.version.wikibase_version_observation_model import (
    WikibaseSoftwareVersionObservationModel,
)
from tests.test_query.wikibase.software_version_obs.software_version_fragment import (
    WIKIBASE_SOFTWARE_VERSION_OBSERVATIONS_FRAGMENT,
)
from tests.test_schema import test_schema
from tests.utils import assert_layered_property_value, assert_property_value

WIKIBASE_SOFTWARE_VERSION_ALL_OBSERVATIONS_QUERY = """
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

""" + WIKIBASE_SOFTWARE_VERSION_OBSERVATIONS_FRAGMENT


@pytest.fixture
async def wikibase_with_software_version_observations(
    db_session,
):  # pylint: disable=unused-argument
    """Create a wikibase with 3 software version observations"""
    async with get_async_session() as session:
        wikibase = WikibaseModel(
            wikibase_name="Software Version All Observations Test Wikibase",
            base_url="https://software-version-all-obs-example.com",
        )
        wikibase.checked = True
        wikibase.reuse = True
        wikibase.test = False
        wikibase.wikibase_type = None
        session.add(wikibase)
        await session.flush()
        await session.refresh(wikibase)

        obs_ids = []
        for i, returned_data in enumerate([False, True, False]):
            obs = WikibaseSoftwareVersionObservationModel()
            obs.wikibase_id = wikibase.id
            obs.returned_data = returned_data
            obs.observation_date = datetime(2024, 3, i + 1, tzinfo=timezone.utc)
            session.add(obs)
            await session.flush()
            await session.refresh(obs)
            obs_ids.append(str(obs.id))

        wikibase_id = wikibase.id

    return {"wikibase_id": wikibase_id, "obs_ids": obs_ids}


@pytest.mark.asyncio
@pytest.mark.query
@pytest.mark.version
async def test_wikibase_software_version_all_observations_query(
    wikibase_with_software_version_observations,
):  # pylint: disable=redefined-outer-name
    """Test Wikibase All Software Version Observations"""

    wikibase_id = wikibase_with_software_version_observations["wikibase_id"]
    obs_ids = wikibase_with_software_version_observations["obs_ids"]

    result = await test_schema.execute(
        WIKIBASE_SOFTWARE_VERSION_ALL_OBSERVATIONS_QUERY,
        variable_values={"wikibaseId": wikibase_id},
    )

    assert result.errors is None
    assert result.data is not None
    assert "wikibase" in result.data
    result_wikibase = result.data["wikibase"]
    assert_property_value(result_wikibase, "id", str(wikibase_id))
    assert "softwareVersionObservations" in result_wikibase

    assert "allObservations" in result_wikibase["softwareVersionObservations"]
    assert (
        len(
            software_version_observation_list := result_wikibase[
                "softwareVersionObservations"
            ]["allObservations"]
        )
        == 3
    )

    assert_layered_property_value(
        software_version_observation_list, [0, "id"], str(obs_ids[0])
    )
    assert "observationDate" in software_version_observation_list[0]
    assert_layered_property_value(
        software_version_observation_list, [0, "returnedData"], False
    )

    assert_layered_property_value(
        software_version_observation_list, [1, "id"], str(obs_ids[1])
    )
    assert "observationDate" in software_version_observation_list[1]
    assert_layered_property_value(
        software_version_observation_list, [1, "returnedData"], True
    )

    assert_layered_property_value(
        software_version_observation_list, [2, "id"], str(obs_ids[2])
    )
    assert "observationDate" in software_version_observation_list[2]
    assert_layered_property_value(
        software_version_observation_list, [2, "returnedData"], False
    )
