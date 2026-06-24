"""Test Wikibase All User Observations Query"""

from datetime import datetime, timezone

import pytest
from data.database_connection import get_async_session
from model.database.wikibase_model import WikibaseModel
from model.database.wikibase_observation.user.wikibase_user_group_model import (
    WikibaseUserGroupModel,
)
from model.database.wikibase_observation.user.wikibase_user_observation_group_model import (
    WikibaseUserObservationGroupModel,
)
from model.database.wikibase_observation.user.wikibase_user_observation_model import (
    WikibaseUserObservationModel,
)
from tests.test_query.wikibase.user_obs.assert_user import assert_user_group
from tests.test_query.wikibase.user_obs.user_fragment import (
    WIKIBASE_USER_OBSERVATION_FRAGMENT,
)
from tests.test_schema import test_schema
from tests.utils import (
    assert_layered_property_count,
    assert_layered_property_value,
    assert_property_value,
)

WIKIBASE_USER_ALL_OBSERVATIONS_QUERY = """
query MyQuery($wikibaseId: Int!) {
  wikibase(wikibaseId: $wikibaseId) {
    id
    userObservations {
      allObservations {
        ...WikibaseUserObservationFragment
      }
    }
  }
}

""" + WIKIBASE_USER_OBSERVATION_FRAGMENT


@pytest.fixture
# pylint: disable-next=too-many-statements, too-many-locals
async def wikibase_with_two_user_observations(
    db_session,
):  # pylint: disable=unused-argument
    """Create a wikibase with two user observations, one with user groups"""
    async with get_async_session() as session:
        wikibase = WikibaseModel(
            wikibase_name="User All Observations Test Wikibase",
            base_url="https://user-all-obs-example.com",
        )
        wikibase.checked = True
        wikibase.reuse = True
        wikibase.test = False
        wikibase.wikibase_type = None
        session.add(wikibase)
        await session.flush()
        await session.refresh(wikibase)

        # observation 1: failed fetch, no data
        obs1 = WikibaseUserObservationModel()
        obs1.wikibase_id = wikibase.id
        obs1.returned_data = False
        obs1.observation_date = datetime(2024, 3, 1, tzinfo=timezone.utc)
        session.add(obs1)
        await session.flush()
        await session.refresh(obs1)

        # observation 2: success, with 2 user groups
        obs2 = WikibaseUserObservationModel()
        obs2.wikibase_id = wikibase.id
        obs2.returned_data = True
        obs2.observation_date = datetime(2024, 3, 2, tzinfo=timezone.utc)
        obs2.total_users = 20
        session.add(obs2)
        await session.flush()
        await session.refresh(obs2)

        group_all = WikibaseUserGroupModel(group_name="*", wikibase_default_group=True)
        group_sysop = WikibaseUserGroupModel(
            group_name="sysop", wikibase_default_group=True
        )
        session.add(group_all)
        session.add(group_sysop)
        await session.flush()
        await session.refresh(group_all)
        await session.refresh(group_sysop)

        og1 = WikibaseUserObservationGroupModel()
        og1.wikibase_user_observation_id = obs2.id
        og1.wikibase_user_group_id = group_all.id
        og1.user_count = 20
        og1.group_implicit = True
        session.add(og1)

        og2 = WikibaseUserObservationGroupModel()
        og2.wikibase_user_observation_id = obs2.id
        og2.wikibase_user_group_id = group_sysop.id
        og2.user_count = 5
        og2.group_implicit = False
        session.add(og2)

        await session.flush()
        await session.refresh(og1)
        await session.refresh(og2)

        wikibase_id = wikibase.id
        obs1_id = str(obs1.id)
        obs2_id = str(obs2.id)
        og1_id, og2_id = str(og1.id), str(og2.id)
        group_all_id, group_sysop_id = str(group_all.id), str(group_sysop.id)

    return {
        "wikibase_id": wikibase_id,
        "obs1_id": obs1_id,
        "obs2_id": obs2_id,
        "og1_id": og1_id,
        "og2_id": og2_id,
        "group_all_id": group_all_id,
        "group_sysop_id": group_sysop_id,
    }


@pytest.mark.asyncio
@pytest.mark.query
@pytest.mark.user
async def test_wikibase_user_all_observations_query(
    wikibase_with_two_user_observations,
):  # pylint: disable=redefined-outer-name
    """Test Wikibase All User Observations"""

    data = wikibase_with_two_user_observations

    result = await test_schema.execute(
        WIKIBASE_USER_ALL_OBSERVATIONS_QUERY,
        variable_values={"wikibaseId": data["wikibase_id"]},
    )

    assert result.errors is None
    assert result.data is not None
    assert "wikibase" in result.data
    result_wikibase = result.data["wikibase"]
    assert_property_value(result_wikibase, "id", str(data["wikibase_id"]))
    assert "userObservations" in result_wikibase

    assert "allObservations" in result_wikibase["userObservations"]
    user_observation_list = result_wikibase["userObservations"]["allObservations"]
    assert len(user_observation_list) == 2

    assert_layered_property_value(user_observation_list, [0, "id"], data["obs1_id"])
    assert "observationDate" in user_observation_list[0]
    assert_layered_property_value(user_observation_list, [0, "returnedData"], False)

    assert_layered_property_value(user_observation_list, [1, "id"], data["obs2_id"])
    assert "observationDate" in user_observation_list[1]
    assert_layered_property_value(user_observation_list, [1, "returnedData"], True)
    assert_layered_property_value(user_observation_list, [1, "totalUsers"], 20)
    assert_layered_property_count(user_observation_list, [1, "userGroups"], 2)

    for index, (
        expected_group_name,
        expected_wikibase_default,
        expected_group_implicit,
        expected_user_count,
    ) in enumerate(
        [
            ("*", True, True, 20),
            ("sysop", True, False, 5),
        ]
    ):
        assert_user_group(
            user_observation_list[1]["userGroups"][index],
            expected_group_name,
            expected_wikibase_default,
            expected_group_implicit,
            expected_user_count,
        )
