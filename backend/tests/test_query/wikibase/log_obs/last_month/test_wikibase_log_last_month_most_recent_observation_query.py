"""Test Wikibase Most Recent Log Observation"""

from datetime import datetime, timezone
from freezegun import freeze_time
import pytest
from data.database_connection import get_async_session
from model.database.wikibase_model import WikibaseModel
from model.database.wikibase_observation.log.wikibase_log_month_observation_model import (
    WikibaseLogMonthObservationModel,
)
from tests.test_query.wikibase.log_obs.log_fragment import (
    WIKIBASE_LOG_OBSERVATION_FRAGMENT,
)
from tests.test_schema import test_schema
from tests.utils import (
    assert_layered_property_count,
    assert_property_value,
    DATETIME_FORMAT,
)

WIKIBASE_LOG_MOST_RECENT_OBSERVATION_QUERY = """
query MyQuery($wikibaseId: Int!) {
  wikibase(wikibaseId: $wikibaseId) {
    id
    logObservations {
      lastMonth {
        mostRecent {
          ...WikibaseLogMonthFragment
        }
      }
    }
  }
}

""" + WIKIBASE_LOG_OBSERVATION_FRAGMENT


@pytest.fixture
async def wikibase_with_log_observation(db_session): # pylint: disable=unused-argument
    """Create a wikibase with a last-month log observation"""
    async with get_async_session() as session:
        wikibase = WikibaseModel(
            wikibase_name="Log Last Month Test Wikibase",
            base_url="https://log-last-month-example.com",
        )
        wikibase.checked = True
        wikibase.reuse = True
        wikibase.test = False
        wikibase.wikibase_type = None
        session.add(wikibase)
        await session.flush()
        await session.refresh(wikibase)

        observation = WikibaseLogMonthObservationModel(
            wikibase_id=wikibase.id, first_month=False
        )
        observation.returned_data = True
        observation.observation_date = datetime(2024, 3, 3, tzinfo=timezone.utc)
        observation.first_log_date = None
        observation.last_log_date = None
        observation.log_count = 0
        observation.user_count = 0
        observation.active_user_count = 0
        observation.human_user_count = 0
        observation.active_human_user_count = 0
        session.add(observation)
        await session.flush()
        await session.refresh(observation)

        wikibase_id = wikibase.id
        observation_id = str(observation.id)
    return wikibase_id, observation_id


@freeze_time(datetime(2024, 4, 1))
@pytest.mark.asyncio
@pytest.mark.log
@pytest.mark.query
async def test_wikibase_log_last_month_most_recent_observation_query(
    wikibase_with_log_observation,
):
    """Test Wikibase Most Recent Log Observation"""

    wikibase_id, observation_id = wikibase_with_log_observation

    result = await test_schema.execute(
        WIKIBASE_LOG_MOST_RECENT_OBSERVATION_QUERY,
        variable_values={"wikibaseId": wikibase_id},
    )

    assert result.errors is None
    assert result.data is not None
    assert "wikibase" in result.data
    result_wikibase = result.data["wikibase"]
    assert_property_value(result_wikibase, "id", str(wikibase_id))
    assert "logObservations" in result_wikibase
    assert "lastMonth" in result_wikibase["logObservations"]
    assert "mostRecent" in result_wikibase["logObservations"]["lastMonth"]
    most_recent = result_wikibase["logObservations"]["lastMonth"]["mostRecent"]

    assert_property_value(most_recent, "id", str(observation_id))
    assert_property_value(
        most_recent, "observationDate", datetime(2024, 3, 3).strftime(DATETIME_FORMAT)
    )
    assert_property_value(most_recent, "returnedData", True)
    # assert_property_value(most_recent, "instanceAge", 160)
    assert_property_value(most_recent, "firstLog", None)
    assert_property_value(most_recent, "lastLog", None)
    assert_property_value(most_recent, "logCount", 0)
    assert_layered_property_count(most_recent, ["logTypeRecords"], 0)
    assert_property_value(most_recent, "allUsers", 0)
    assert_property_value(most_recent, "activeUsers", 0)
    assert_property_value(most_recent, "humanUsers", 0)
    assert_property_value(most_recent, "activeHumanUsers", 0)
    assert_layered_property_count(most_recent, ["userTypeRecords"], 0)
