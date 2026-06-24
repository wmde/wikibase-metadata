"""Test Wikibase Most Recent User Observation Query"""

from datetime import datetime, timezone

import pytest
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
from tests.utils import assert_layered_property_count, assert_property_value
from sqlalchemy.ext.asyncio import AsyncSession

WIKIBASE_USER_MOST_RECENT_OBSERVATION_QUERY = """
query MyQuery($wikibaseId: Int!) {
  wikibase(wikibaseId: $wikibaseId) {
    id
    userObservations {
      mostRecent {
        ...WikibaseUserObservationFragment
      }
    }
  }
}

""" + WIKIBASE_USER_OBSERVATION_FRAGMENT


@pytest.fixture
async def wikibase_with_user_observation(db_session):
    """Create a wikibase with user observation and 8 user groups"""
    async with AsyncSession(bind=db_session) as session:
        wikibase = WikibaseModel(
            wikibase_name="Aggregate Users Test Wikibase",
            base_url="https://aggregate-users-example.com",
            script_path="/w",
        )
        wikibase.checked = True
        wikibase.reuse = True
        wikibase.test = False
        wikibase.wikibase_type = None
        session.add(wikibase)
        await session.flush()
        await session.refresh(wikibase)

        observation = WikibaseUserObservationModel()
        observation.wikibase_id = wikibase.id
        observation.returned_data = True
        observation.observation_date = datetime(2024, 3, 1, tzinfo=timezone.utc)
        observation.total_users = 2000
        session.add(observation)
        await session.flush()
        await session.refresh(observation)

        groups_data = [
            ("*", True, True, 2000),
            ("administrator", False, False, 708),
            ("autoconfirmed", True, True, 2000),
            ("bot", False, False, 754),
            ("bureaucrat", True, False, 715),
            ("editor", False, False, 708),
            ("sysop", True, False, 715),
            ("user", True, True, 2000),
        ]

        for group_name, wikibase_default, implicit, user_count in groups_data:
            group = WikibaseUserGroupModel(
                group_name=group_name,
                wikibase_default_group=wikibase_default,
            )
            session.add(group)
            await session.flush()
            await session.refresh(group)

            group_obs = WikibaseUserObservationGroupModel(
                user_group=group,
                user_count=user_count,
                group_implicit=implicit,
            )
            group_obs.wikibase_user_observation_id = observation.id
            session.add(group_obs)
            await session.flush()

        return wikibase.id, observation.id


@pytest.mark.asyncio
@pytest.mark.query
@pytest.mark.user
async def test_wikibase_user_most_recent_observation_query(
    wikibase_with_user_observation,
):  # pylint: disable=redefined-outer-name
    """Test Wikibase Most Recent User Observation"""

    wikibase_id, obs_id = wikibase_with_user_observation

    result = await test_schema.execute(
        WIKIBASE_USER_MOST_RECENT_OBSERVATION_QUERY,
        variable_values={"wikibaseId": wikibase_id},
    )

    assert result.errors is None
    assert result.data is not None
    assert "wikibase" in result.data
    result_wikibase = result.data["wikibase"]
    assert_property_value(result_wikibase, "id", str(wikibase_id))
    assert "userObservations" in result_wikibase
    assert "mostRecent" in result_wikibase["userObservations"]
    most_recent = result_wikibase["userObservations"]["mostRecent"]

    assert_property_value(most_recent, "id", str(obs_id))
    assert "observationDate" in most_recent
    assert_property_value(most_recent, "returnedData", True)
    assert_property_value(most_recent, "totalUsers", 2000)
    assert_layered_property_count(most_recent, ["userGroups"], 8)

    for index, (
        expected_group_name,
        expected_wikibase_default,
        expected_group_implicit,
        expected_user_count,
    ) in enumerate(
        [
            ("*", True, True, 2000),
            ("autoconfirmed", True, True, 2000),
            ("user", True, True, 2000),
            ("bot", False, False, 754),
            ("bureaucrat", True, False, 715),
            ("sysop", True, False, 715),
            ("administrator", False, False, 708),
            ("editor", False, False, 708),
        ]
    ):
        assert_user_group(
            most_recent["userGroups"][index],
            expected_group_name,
            expected_wikibase_default,
            expected_group_implicit,
            expected_user_count,
        )
