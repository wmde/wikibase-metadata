"""Test Wikibase All Connectivity Observations Query"""

from datetime import datetime, timezone

from freezegun import freeze_time
import pytest

from data import get_async_session
from model.database import (
    WikibaseConnectivityObservationModel,
    WikibaseConnectivityObservationItemRelationshipCountModel,
    WikibaseConnectivityObservationObjectRelationshipCountModel,
    WikibaseModel,
)
from tests.test_query.wikibase.connectivity_obs.assert_connectivity import (
    assert_connectivity_observation,
)
from tests.test_query.wikibase.connectivity_obs.connectivity_fragment import (
    WIKIBASE_CONNECTIVITY_OBSERVATION_FRAGMENT,
)
from tests.test_schema import test_schema
from tests.utils import assert_property_value

WIKIBASE_CONNECTIVITY_ALL_OBSERVATIONS_QUERY = """
query MyQuery($wikibaseId: Int!) {
  wikibase(wikibaseId: $wikibaseId) {
    id
    connectivityObservations {
      allObservations {
        ...WikibaseConnectivityObservationFragment
      }
    }
  }
}

""" + WIKIBASE_CONNECTIVITY_OBSERVATION_FRAGMENT


@pytest.fixture
# pylint: disable-next=too-many-statements
async def wikibase_with_connectivity_observations(
    db_session,
):  # pylint: disable=unused-argument
    """Create a wikibase with 3 connectivity observations: empty, simple, and failed"""
    async with get_async_session() as session:
        wikibase = WikibaseModel(
            wikibase_name="Connectivity All Observations Test Wikibase",
            base_url="https://connectivity-all-obs-example.com",
        )
        wikibase.checked = True
        wikibase.reuse = True
        wikibase.test = False
        wikibase.wikibase_type = None
        session.add(wikibase)
        await session.flush()
        await session.refresh(wikibase)

        # observation 1: empty, no links
        obs1 = WikibaseConnectivityObservationModel()
        obs1.wikibase_id = wikibase.id
        obs1.returned_data = True
        obs1.observation_date = datetime(2024, 3, 1, tzinfo=timezone.utc)
        obs1.returned_links = 0
        obs1.connectivity = None
        obs1.average_connected_distance = None
        session.add(obs1)
        await session.flush()
        await session.refresh(obs1)

        # observation 2: simple link, item_sum == object_sum == 1
        obs2 = WikibaseConnectivityObservationModel()
        obs2.wikibase_id = wikibase.id
        obs2.returned_data = True
        obs2.observation_date = datetime(2024, 3, 2, tzinfo=timezone.utc)
        obs2.returned_links = 1
        obs2.connectivity = 1 / 4
        obs2.average_connected_distance = 1.0
        session.add(obs2)
        await session.flush()
        await session.refresh(obs2)

        item_rc = WikibaseConnectivityObservationItemRelationshipCountModel()
        item_rc.wikibase_connectivity_observation_id = obs2.id
        item_rc.relationship_count = 1
        item_rc.item_count = 1
        session.add(item_rc)

        object_rc = WikibaseConnectivityObservationObjectRelationshipCountModel()
        object_rc.wikibase_connectivity_observation_id = obs2.id
        object_rc.relationship_count = 1
        object_rc.object_count = 1
        session.add(object_rc)

        await session.flush()
        await session.refresh(item_rc)
        await session.refresh(object_rc)

        # observation 3: failed, no data
        obs3 = WikibaseConnectivityObservationModel()
        obs3.wikibase_id = wikibase.id
        obs3.returned_data = False
        obs3.observation_date = datetime(2024, 3, 3, tzinfo=timezone.utc)
        session.add(obs3)
        await session.flush()
        await session.refresh(obs3)

        wikibase_id = wikibase.id
        result = {
            "wikibase_id": wikibase_id,
            "obs1_id": str(obs1.id),
            "obs2_id": str(obs2.id),
            "obs3_id": str(obs3.id),
            "item_rc_id": str(item_rc.id),
            "object_rc_id": str(object_rc.id),
        }
    return result


@freeze_time(datetime(2024, 4, 1))
@pytest.mark.asyncio
@pytest.mark.connectivity
@pytest.mark.query
async def test_wikibase_connectivity_all_observations_query(
    wikibase_with_connectivity_observations,
):  # pylint: disable=redefined-outer-name
    """Test Wikibase All Connectivity Observations Query"""

    data = wikibase_with_connectivity_observations

    result = await test_schema.execute(
        WIKIBASE_CONNECTIVITY_ALL_OBSERVATIONS_QUERY,
        variable_values={"wikibaseId": data["wikibase_id"]},
    )

    assert result.errors is None
    assert result.data is not None
    assert "wikibase" in result.data
    result_wikibase = result.data["wikibase"]
    assert_property_value(result_wikibase, "id", str(data["wikibase_id"]))
    assert "connectivityObservations" in result_wikibase

    assert "allObservations" in result_wikibase["connectivityObservations"]
    connectivity_observation_list = result_wikibase["connectivityObservations"][
        "allObservations"
    ]
    assert len(connectivity_observation_list) == 3

    assert_connectivity_observation(
        connectivity_observation_list[0],
        data["obs1_id"],
        True,
        0,
        0,
        None,
        None,
        [],
        [],
    )

    assert_connectivity_observation(
        connectivity_observation_list[1],
        data["obs2_id"],
        True,
        1,
        1,
        1.0,
        1 / 4,
        [(data["item_rc_id"], 1, 1)],
        [(data["object_rc_id"], 1, 1)],
    )

    assert_connectivity_observation(
        connectivity_observation_list[2], data["obs3_id"], False
    )
