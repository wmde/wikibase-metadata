"""Test Recent Changes Observation Query"""

from datetime import datetime, timezone

import pytest

from data import get_async_session
from model.database import WikibaseModel, WikibaseRecentChangesObservationModel
from tests.test_schema import test_schema
from tests.utils import DATETIME_FORMAT, assert_layered_property_value

WIKIBASE_QUERY = """
query MyQuery($wikibaseId: Int!) {
  wikibase(wikibaseId: $wikibaseId) {
    id
    recentChangesObservations {
      mostRecent {
        id
        observationDate
        returnedData
        humanChangeCount
        humanChangeUserCount
        humanChangeActiveUserCount
        botChangeCount
        botChangeUserCount
        botChangeActiveUserCount
        firstChangeDate
        lastChangeDate
      }
    }
  }
}
"""


@pytest.fixture
async def wikibase_with_recent_changes_observation(
    db_session,
):  # pylint: disable=unused-argument
    """Create a wikibase with a recent changes observation"""
    async with get_async_session() as session:
        wikibase = WikibaseModel(
            wikibase_name="Recent Changes Test Wikibase",
            base_url="https://recent-changes-query-example.com",
        )
        wikibase.checked = True
        wikibase.reuse = True
        wikibase.test = False
        wikibase.wikibase_type = None
        session.add(wikibase)
        await session.flush()
        await session.refresh(wikibase)

        observation = WikibaseRecentChangesObservationModel()
        observation.wikibase_id = wikibase.id
        observation.returned_data = True
        observation.observation_date = datetime(2024, 3, 6)
        observation.human_change_count = 10
        observation.human_change_user_count = 5
        observation.human_change_active_user_count = 1
        observation.bot_change_count = 6
        observation.bot_change_user_count = 2
        observation.bot_change_active_user_count = 1
        # observation.first_change_date = datetime(2024, 3, 1, 12, 0, 0)
        # observation.last_change_date = datetime(2024, 3, 5, 12, 0, 0)
        observation.first_change_date = datetime(
            2024, 3, 1, 12, 0, 0, tzinfo=timezone.utc
        )
        observation.last_change_date = datetime(
            2024, 3, 5, 12, 0, 0, tzinfo=timezone.utc
        )
        observation.observation_date = datetime(2024, 3, 6, tzinfo=timezone.utc)
        session.add(observation)
        await session.flush()
        await session.refresh(wikibase)
        return wikibase


@pytest.mark.asyncio
@pytest.mark.query
async def test_wikibase_query_recent_changes_success(
    wikibase_with_recent_changes_observation,
):  # pylint: disable=redefined-outer-name
    """Test success scenario"""
    result = await test_schema.execute(
        WIKIBASE_QUERY,
        variable_values={"wikibaseId": wikibase_with_recent_changes_observation.id},
    )

    assert result.errors is None
    assert result.data is not None

    assert_layered_property_value(
        result.data,
        ["wikibase", "recentChangesObservations", "mostRecent", "humanChangeCount"],
        10,
    )

    assert_layered_property_value(
        result.data,
        ["wikibase", "recentChangesObservations", "mostRecent", "botChangeCount"],
        6,
    )

    assert_layered_property_value(
        result.data,
        ["wikibase", "recentChangesObservations", "mostRecent", "humanChangeUserCount"],
        5,
    )
    assert_layered_property_value(
        result.data,
        [
            "wikibase",
            "recentChangesObservations",
            "mostRecent",
            "humanChangeActiveUserCount",
        ],
        1,
    )

    assert_layered_property_value(
        result.data,
        ["wikibase", "recentChangesObservations", "mostRecent", "botChangeUserCount"],
        2,
    )
    assert_layered_property_value(
        result.data,
        [
            "wikibase",
            "recentChangesObservations",
            "mostRecent",
            "botChangeActiveUserCount",
        ],
        1,
    )

    assert_layered_property_value(
        result.data,
        ["wikibase", "recentChangesObservations", "mostRecent", "firstChangeDate"],
        datetime(2024, 3, 1, 12, 0, 0).strftime(DATETIME_FORMAT),
    )

    assert_layered_property_value(
        result.data,
        ["wikibase", "recentChangesObservations", "mostRecent", "lastChangeDate"],
        datetime(2024, 3, 5, 12, 0, 0).strftime(DATETIME_FORMAT),
    )
