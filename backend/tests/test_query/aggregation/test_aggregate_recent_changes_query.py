"""Test Aggregate Recent Changes Query"""

from datetime import datetime, timezone

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from model.database import WikibaseModel, WikibaseRecentChangesObservationModel
from model.enum import WikibaseType
from tests.test_schema import test_schema
from tests.utils import assert_layered_property_value

AGGREGATED_RECENT_CHANGES_QUERY = """
query MyQuery($wikibaseFilter: WikibaseFilterInput) {
  aggregateRecentChanges(wikibaseFilter: $wikibaseFilter) {
    humanChangeCount
    humanChangeUserCount
    humanChangeActiveUserCount
    botChangeCount
    botChangeUserCount
    botChangeActiveUserCount
    wikibaseCount
  }
}
"""


@pytest.fixture
async def wikibases_with_recent_changes(db_session):  # pylint: disable=unused-argument
    """Create a wikibase and wikibase suite with a recent changes observations for aggregate tests"""
    async with AsyncSession(bind=db_session) as session:
        wikibase = WikibaseModel(
            wikibase_name="Aggregate Recent Changes Test Wikibase",
            base_url="https://aggregate-recent-changes-example.com",
            reuse=True,
            wikibase_type=WikibaseType.OTHER,
        )
        wikibase.checked = True
        wikibase.test = False
        session.add(wikibase)
        await session.flush()
        await session.refresh(wikibase)

        obs = WikibaseRecentChangesObservationModel()
        obs.wikibase_id = wikibase.id
        obs.returned_data = True
        obs.observation_date = datetime(2024, 3, 1, tzinfo=timezone.utc)
        obs.human_change_count = 10
        obs.human_change_user_count = 5
        obs.human_change_active_user_count = 1
        obs.bot_change_count = 6
        obs.bot_change_user_count = 2
        obs.bot_change_active_user_count = 1
        obs.first_change_date = datetime(2024, 3, 1, tzinfo=timezone.utc)
        obs.last_change_date = datetime(2024, 3, 5, tzinfo=timezone.utc)
        session.add(obs)

        wikibase_suite = WikibaseModel(
            wikibase_name="Aggregate Recent Changes Filtered Test Wikibase",
            base_url="https://aggregate-recent-changes-filtered-example.com",
            reuse=True,
            wikibase_type=WikibaseType.SUITE,
        )
        wikibase.checked = True
        session.add(wikibase)
        await session.flush()
        await session.refresh(wikibase_suite)

        suite_obs = WikibaseRecentChangesObservationModel()
        suite_obs.wikibase_id = wikibase_suite.id
        suite_obs.returned_data = True
        suite_obs.observation_date = datetime(2024, 3, 1, tzinfo=timezone.utc)
        suite_obs.human_change_count = 10
        suite_obs.human_change_user_count = 5
        suite_obs.human_change_active_user_count = 1
        suite_obs.bot_change_count = 6
        suite_obs.bot_change_user_count = 2
        suite_obs.bot_change_active_user_count = 1
        suite_obs.first_change_date = datetime(2024, 3, 1, tzinfo=timezone.utc)
        suite_obs.last_change_date = datetime(2024, 3, 5, tzinfo=timezone.utc)
        session.add(suite_obs)
        await session.flush()

        return obs, suite_obs


@pytest.mark.asyncio
@pytest.mark.agg
@pytest.mark.query
async def test_aggregate_recent_changes_query(
    wikibases_with_recent_changes,
):  # pylint: disable=redefined-outer-name, unused-argument
    """Test Aggregate Recent Changes Query"""

    obs, suite_obs = wikibases_with_recent_changes

    result = await test_schema.execute(AGGREGATED_RECENT_CHANGES_QUERY)

    assert result.errors is None
    assert result.data is not None

    expectedHumanChangeCount = obs.human_change_count + suite_obs.human_change_count
    assert_layered_property_value(
        result.data,
        ["aggregateRecentChanges", "humanChangeCount"],
        expectedHumanChangeCount,
    )

    expected_human_change_user_count = (
        obs.human_change_user_count + suite_obs.human_change_user_count
    )
    assert_layered_property_value(
        result.data,
        ["aggregateRecentChanges", "humanChangeUserCount"],
        expected_human_change_user_count,
    )

    expected_human_change_active_user_count = (
        obs.human_change_active_user_count + suite_obs.human_change_active_user_count
    )
    assert_layered_property_value(
        result.data,
        ["aggregateRecentChanges", "humanChangeActiveUserCount"],
        expected_human_change_active_user_count,
    )

    expected_bot_change_count = obs.bot_change_count + suite_obs.bot_change_count
    assert_layered_property_value(
        result.data,
        ["aggregateRecentChanges", "botChangeCount"],
        expected_bot_change_count,
    )

    expected_bot_change_user_count = (
        obs.bot_change_user_count + suite_obs.bot_change_user_count
    )
    assert_layered_property_value(
        result.data,
        ["aggregateRecentChanges", "botChangeUserCount"],
        expected_bot_change_user_count,
    )

    expected_bot_change_active_user_count = (
        obs.bot_change_active_user_count + suite_obs.bot_change_active_user_count
    )
    assert_layered_property_value(
        result.data,
        ["aggregateRecentChanges", "botChangeActiveUserCount"],
        expected_bot_change_active_user_count,
    )

    assert_layered_property_value(
        result.data, ["aggregateRecentChanges", "wikibaseCount"], 2
    )


@pytest.mark.asyncio
@pytest.mark.agg
@pytest.mark.query
@pytest.mark.parametrize(
    ["exclude", "expected_count"],
    [
        ([], 2),
        (["CLOUD"], 2),
        (["OTHER"], 1),
        (["SUITE"], 1),
        (["CLOUD", "OTHER"], 1),
        (["CLOUD", "SUITE"], 1),
        (["OTHER", "SUITE"], 0),
        (["CLOUD", "OTHER", "SUITE"], 0),
    ],
)
async def test_aggregate_recent_changes_query_filtered(
    wikibases_with_recent_changes, exclude: list, expected_count: int
):  # pylint: disable=redefined-outer-name, unused-argument
    """Test Aggregate Recent Changes Query with Filter"""

    result = await test_schema.execute(
        AGGREGATED_RECENT_CHANGES_QUERY,
        variable_values={"wikibaseFilter": {"wikibaseType": {"exclude": exclude}}},
    )

    assert result.errors is None
    assert result.data is not None

    assert_layered_property_value(
        result.data, ["aggregateRecentChanges", "wikibaseCount"], expected_count
    )
