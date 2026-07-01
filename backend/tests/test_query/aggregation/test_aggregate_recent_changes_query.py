"""Test Aggregate Recent Changes Query"""

from datetime import datetime, timezone

import pytest


from data import get_async_session
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
async def wikibase_with_recent_changes(db_session):  # pylint: disable=unused-argument
    """Create a wikibase with a recent changes observation for aggregate tests"""
    async with get_async_session() as session:
        wikibase = WikibaseModel(
            wikibase_name="Aggregate Recent Changes Test Wikibase",
            base_url="https://aggregate-recent-changes-example.com",
        )
        wikibase.checked = True
        wikibase.reuse = True
        wikibase.test = False
        wikibase.wikibase_type = None
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
        await session.flush()


@pytest.fixture
async def wikibase_with_recent_changes_suite(
    db_session,
):  # pylint: disable=unused-argument
    """Create a SUITE wikibase with a recent changes observation for filtered tests"""
    async with get_async_session() as session:
        wikibase = WikibaseModel(
            wikibase_name="Aggregate Recent Changes Filtered Test Wikibase",
            base_url="https://aggregate-recent-changes-filtered-example.com",
        )
        wikibase.checked = True
        wikibase.reuse = True
        wikibase.test = False
        wikibase.wikibase_type = WikibaseType.SUITE
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
        await session.flush()


@pytest.mark.asyncio
@pytest.mark.agg
@pytest.mark.query
async def test_aggregate_recent_changes_query(
    wikibase_with_recent_changes,
):  # pylint: disable=redefined-outer-name, unused-argument
    """Test Aggregate Recent Changes Query"""

    result = await test_schema.execute(AGGREGATED_RECENT_CHANGES_QUERY)

    assert result.errors is None
    assert result.data is not None

    assert_layered_property_value(
        result.data, ["aggregateRecentChanges", "humanChangeCount"], 10
    )
    assert_layered_property_value(
        result.data, ["aggregateRecentChanges", "humanChangeUserCount"], 5
    )
    assert_layered_property_value(
        result.data, ["aggregateRecentChanges", "humanChangeActiveUserCount"], 1
    )
    assert_layered_property_value(
        result.data, ["aggregateRecentChanges", "botChangeCount"], 6
    )
    assert_layered_property_value(
        result.data, ["aggregateRecentChanges", "botChangeUserCount"], 2
    )
    assert_layered_property_value(
        result.data, ["aggregateRecentChanges", "botChangeActiveUserCount"], 1
    )
    assert_layered_property_value(
        result.data, ["aggregateRecentChanges", "wikibaseCount"], 1
    )


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
async def test_aggregate_recent_changes_query_filtered(
    wikibase_with_recent_changes_suite, exclude: list, expected_count: int
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
