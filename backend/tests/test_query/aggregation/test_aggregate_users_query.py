"""Test Aggregate Users Query"""

from datetime import datetime, timezone

import pytest
from data.database_connection import get_async_session
from model.enum.wikibase_type_enum import WikibaseType
from model.database.wikibase_model import WikibaseModel
from model.database.wikibase_observation.user.wikibase_user_group_model import (
    WikibaseUserGroupModel,
)
from model.database.wikibase_observation.user.wikibase_user_observation_model import (
    WikibaseUserObservationModel,
)
from model.database.wikibase_observation.user.wikibase_user_observation_group_model import (
    WikibaseUserObservationGroupModel,
)
from tests.test_schema import test_schema
from tests.utils import assert_layered_property_value

AGGREGATED_USERS_QUERY = """
query MyQuery($wikibaseFilter: WikibaseFilterInput) {
  aggregateUsers(wikibaseFilter: $wikibaseFilter) {
    totalAdmin
    totalUsers
    wikibaseCount
  }
}
"""


@pytest.fixture
async def wikibase_with_user_observation(db_session):  # pylint: disable=unused-argument
    """Create a wikibase with user observation for aggregate users tests"""
    async with get_async_session() as session:
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

        sysop_group = WikibaseUserGroupModel(
            group_name="sysop",
            wikibase_default_group=True,
        )
        session.add(sysop_group)
        await session.flush()
        await session.refresh(sysop_group)

        group_obs = WikibaseUserObservationGroupModel(
            user_group=sysop_group,
            user_count=715,
            group_implicit=False,
        )
        group_obs.wikibase_user_observation_id = observation.id
        session.add(group_obs)
        await session.flush()


@pytest.mark.asyncio
@pytest.mark.agg
@pytest.mark.user
@pytest.mark.query
async def test_aggregate_users_query(
    wikibase_with_user_observation,
):  # pylint: disable=unused-argument, redefined-outer-name
    """Test Aggregate Users Query"""

    result = await test_schema.execute(AGGREGATED_USERS_QUERY)

    assert result.errors is None
    assert result.data is not None

    assert_layered_property_value(result.data, ["aggregateUsers", "totalAdmin"], 715)
    assert_layered_property_value(result.data, ["aggregateUsers", "totalUsers"], 2000)
    assert_layered_property_value(result.data, ["aggregateUsers", "wikibaseCount"], 1)


@pytest.fixture
async def wikibase_with_user_observation_suite(
    db_session,
):  # pylint: disable=unused-argument
    """Create a SUITE wikibase with a user observation and admin group"""
    async with get_async_session() as session:
        wikibase = WikibaseModel(
            wikibase_name="Aggregate Users Filtered Test Wikibase",
            base_url="https://aggregate-users-filtered-example.com",
        )
        wikibase.checked = True
        wikibase.reuse = True
        wikibase.test = False
        wikibase.wikibase_type = WikibaseType.SUITE
        session.add(wikibase)
        await session.flush()
        await session.refresh(wikibase)

        obs = WikibaseUserObservationModel()
        obs.wikibase_id = wikibase.id
        obs.returned_data = True
        obs.observation_date = datetime(2024, 3, 1, tzinfo=timezone.utc)
        obs.total_users = 10
        session.add(obs)
        await session.flush()
        await session.refresh(obs)

        sysop_group = WikibaseUserGroupModel(
            group_name="sysop",
            wikibase_default_group=True,
        )
        session.add(sysop_group)
        await session.flush()
        await session.refresh(sysop_group)

        group_obs = WikibaseUserObservationGroupModel(
            user_group=sysop_group,
            user_count=2,
            group_implicit=False,
        )
        group_obs.wikibase_user_observation_id = obs.id
        session.add(group_obs)
        await session.flush()


@pytest.mark.asyncio
@pytest.mark.agg
@pytest.mark.query
@pytest.mark.parametrize(
    ["exclude", "expected_count"],
    [
        ([], 1),
        (["CLOUD"], 1),
        (["OTHER"], 1),
        (["SUITE"], 0),
        (["CLOUD", "OTHER"], 1),
        (["CLOUD", "SUITE"], 0),
        (["OTHER", "SUITE"], 0),
        (["CLOUD", "OTHER", "SUITE"], 0),
    ],
)
@pytest.mark.user
async def test_aggregate_users_query_filtered(
    wikibase_with_user_observation_suite, exclude: list, expected_count: int
):  # pylint: disable=redefined-outer-name, unused-argument
    """Test Aggregate Users Query"""

    result = await test_schema.execute(
        AGGREGATED_USERS_QUERY,
        variable_values={"wikibaseFilter": {"wikibaseType": {"exclude": exclude}}},
    )

    assert result.errors is None
    assert result.data is not None

    assert_layered_property_value(
        result.data, ["aggregateUsers", "wikibaseCount"], expected_count
    )
