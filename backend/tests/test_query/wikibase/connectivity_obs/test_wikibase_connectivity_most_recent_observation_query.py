"""Test Wikibase Most Recent Connectivity Observation"""

from datetime import datetime, timezone
from freezegun import freeze_time
import pytest
from data.database_connection import get_async_session
from model.database.wikibase_model import WikibaseModel
from model.database.wikibase_observation.connectivity.connectivity_observation_model import (
    WikibaseConnectivityObservationModel,
)
from model.database.wikibase_observation.connectivity.item_relationship_count_model import (
    WikibaseConnectivityObservationItemRelationshipCountModel,
)
from model.database.wikibase_observation.connectivity.object_relationship_count_model import (
    WikibaseConnectivityObservationObjectRelationshipCountModel,
)
from tests.test_query.wikibase.connectivity_obs.assert_connectivity import (
    assert_connectivity_observation,
)
from tests.test_query.wikibase.connectivity_obs.connectivity_fragment import (
    WIKIBASE_CONNECTIVITY_OBSERVATION_FRAGMENT,
)
from tests.test_schema import test_schema
from tests.utils import assert_property_value

WIKIBASE_CONNECTIVITY_MOST_RECENT_OBSERVATION_QUERY = """
query MyQuery($wikibaseId: Int!) {
  wikibase(wikibaseId: $wikibaseId) {
    id
    connectivityObservations {
      mostRecent {
        ...WikibaseConnectivityObservationFragment
      }
    }
  }
}

""" + WIKIBASE_CONNECTIVITY_OBSERVATION_FRAGMENT


@pytest.fixture
async def wikibase_with_complex_connectivity(db_session):
    """Create a wikibase with a connectivity observation with relationship counts"""
    async with get_async_session() as session:
        wikibase = WikibaseModel(
            wikibase_name="Connectivity Most Recent Test Wikibase",
            base_url="https://connectivity-most-recent-example.com",
            sparql_endpoint_url="https://connectivity-most-recent-example.com/sparql",
        )
        wikibase.checked = True
        wikibase.reuse = True
        wikibase.test = False
        wikibase.wikibase_type = None
        session.add(wikibase)
        await session.flush()
        await session.refresh(wikibase)

        obs = WikibaseConnectivityObservationModel()
        obs.wikibase_id = wikibase.id
        obs.returned_data = True
        obs.observation_date = datetime(2024, 3, 1, tzinfo=timezone.utc)
        obs.returned_links = 6
        obs.connectivity = 2 / (3 * (3 - 1))
        obs.average_connected_distance = 4 / 3
        session.add(obs)
        await session.flush()
        await session.refresh(obs)

        item_counts = [(1, 2), (2, 1)]
        item_rc_ids = []
        for rel_count, item_count in item_counts:
            rc = WikibaseConnectivityObservationItemRelationshipCountModel()
            rc.wikibase_connectivity_observation_id = obs.id
            rc.relationship_count = rel_count
            rc.item_count = item_count
            session.add(rc)
            await session.flush()
            await session.refresh(rc)
            item_rc_ids.append(str(rc.id))

        object_counts = [(1, 2), (2, 1)]
        object_rc_ids = []
        for rel_count, object_count in object_counts:
            rc = WikibaseConnectivityObservationObjectRelationshipCountModel()
            rc.wikibase_connectivity_observation_id = obs.id
            rc.relationship_count = rel_count
            rc.object_count = object_count
            session.add(rc)
            await session.flush()
            await session.refresh(rc)
            object_rc_ids.append(str(rc.id))

        wikibase_id = wikibase.id
        obs_id = str(obs.id)

    return {
        "wikibase_id": wikibase_id,
        "obs_id": obs_id,
        "item_rc_ids": item_rc_ids,
        "object_rc_ids": object_rc_ids,
    }


@freeze_time(datetime(2024, 4, 1))
@pytest.mark.asyncio
@pytest.mark.connectivity
@pytest.mark.query
async def test_wikibase_connectivity_most_recent_observation_query(
    wikibase_with_complex_connectivity,
):  # pylint: disable=redefined-outer-name
    """Test Wikibase Most Recent Connectivity Observation"""

    data = wikibase_with_complex_connectivity
    wikibase_id = data["wikibase_id"]

    result = await test_schema.execute(
        WIKIBASE_CONNECTIVITY_MOST_RECENT_OBSERVATION_QUERY,
        variable_values={"wikibaseId": wikibase_id},
    )

    assert result.errors is None
    assert result.data is not None
    assert "wikibase" in result.data
    result_wikibase = result.data["wikibase"]
    assert_property_value(result_wikibase, "id", str(wikibase_id))
    assert "connectivityObservations" in result_wikibase
    assert "mostRecent" in result_wikibase["connectivityObservations"]
    most_recent = result_wikibase["connectivityObservations"]["mostRecent"]

    assert_connectivity_observation(
        most_recent,
        data["obs_id"],
        True,
        6,
        4,
        4 / 3,
        2 / (3 * (3 - 1)),
        [(data["item_rc_ids"][0], 1, 2), (data["item_rc_ids"][1], 2, 1)],
        [(data["object_rc_ids"][0], 1, 2), (data["object_rc_ids"][1], 2, 1)],
    )
