"""Test Aggregate Users Query"""

from datetime import datetime, timezone

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from model.database import (
    WikibaseModel,
    WikibaseUserGroupModel,
    WikibaseUserObservationGroupModel,
    WikibaseUserObservationModel,
)
from model.enum import WikibaseType
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
async def wikibases_with_user_observation(
    db_session,
):  # pylint: disable=unused-argument
    """Create a wikibase with user observation for aggregate users tests"""
    async with AsyncSession(bind=db_session) as session:
        wikibase = WikibaseModel(
            wikibase_name="Aggregate Users Test Wikibase",
            base_url="https://aggregate-users-example.com",
            script_path="/w",
            reuse=True,
            wikibase_type=WikibaseType.CLOUD,
        )
        wikibase.checked = True
        wikibase.test = False
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

        wikibase_suite = WikibaseModel(
            wikibase_name="Aggregate Users Filtered Test Wikibase",
            base_url="https://aggregate-users-filtered-example.com",
            reuse=True,
            wikibase_type=WikibaseType.SUITE,
        )
        wikibase_suite.checked = True
        wikibase_suite.test = False
        session.add(wikibase_suite)
        await session.flush()
        await session.refresh(wikibase_suite)

        suite_obs = WikibaseUserObservationModel()
        suite_obs.wikibase_id = wikibase_suite.id
        suite_obs.returned_data = True
        suite_obs.observation_date = datetime(2024, 3, 1, tzinfo=timezone.utc)
        suite_obs.total_users = 10
        session.add(suite_obs)
        await session.flush()
        await session.refresh(suite_obs)

        group_obs_2 = WikibaseUserObservationGroupModel(
            user_group=sysop_group,  # reuse the existing "sysop" group row
            user_count=2,
            group_implicit=False,
        )
        group_obs_2.wikibase_user_observation_id = suite_obs.id
        session.add(group_obs_2)
        await session.flush()


@pytest.mark.asyncio
@pytest.mark.agg
@pytest.mark.user
@pytest.mark.query
async def test_aggregate_users_query(
    wikibases_with_user_observation,
):  # pylint: disable=unused-argument, redefined-outer-name
    """Test Aggregate Users Query"""

    result = await test_schema.execute(AGGREGATED_USERS_QUERY)

    assert result.errors is None
    assert result.data is not None

    assert_layered_property_value(result.data, ["aggregateUsers", "totalAdmin"], 717)
    assert_layered_property_value(result.data, ["aggregateUsers", "totalUsers"], 2010)
    assert_layered_property_value(result.data, ["aggregateUsers", "wikibaseCount"], 2)


@pytest.mark.asyncio
@pytest.mark.agg
@pytest.mark.query
@pytest.mark.parametrize(
    ["exclude", "expected_count"],
    [
        ([], 2),
        (["CLOUD"], 1),
        (["OTHER"], 2),
        (["SUITE"], 1),
        (["CLOUD", "OTHER"], 1),
        (["CLOUD", "SUITE"], 0),
        (["OTHER", "SUITE"], 1),
        (["CLOUD", "OTHER", "SUITE"], 0),
    ],
)
@pytest.mark.user
async def test_aggregate_users_query_filtered(
    wikibases_with_user_observation, exclude: list, expected_count: int
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
