"""Test Wikibase Most Recent Log Observation"""

from datetime import datetime
from freezegun import freeze_time
import pytest
from tests.test_query.wikibase.log_obs.log_fragment import (
    WIKIBASE_LOG_OBSERVATION_FRAGMENT,
)
from tests.test_schema import test_schema
from tests.utils import (
    assert_layered_property_count,
    assert_property_value,
    DATETIME_FORMAT,
    get_mock_context,
)


WIKIBASE_LOG_MOST_RECENT_OBSERVATION_QUERY = (
    """
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

"""
    + WIKIBASE_LOG_OBSERVATION_FRAGMENT
)


@freeze_time(datetime(2024, 4, 1))
@pytest.mark.asyncio
@pytest.mark.dependency(
    depends=["log-last-success-1", "log-last-success-2"], scope="session"
)
@pytest.mark.log
@pytest.mark.query
async def test_wikibase_log_last_month_most_recent_observation_query():
    """Test Wikibase Most Recent Log Observation"""

    result = await test_schema.execute(
        WIKIBASE_LOG_MOST_RECENT_OBSERVATION_QUERY, variable_values={"wikibaseId": 1}
    )

    assert result.errors is None
    assert result.data is not None
    assert "wikibase" in result.data
    result_wikibase = result.data["wikibase"]
    assert_property_value(result_wikibase, "id", "1")
    assert "logObservations" in result_wikibase
    assert "lastMonth" in result_wikibase["logObservations"]
    assert "mostRecent" in result_wikibase["logObservations"]["lastMonth"]
    most_recent = result_wikibase["logObservations"]["lastMonth"]["mostRecent"]

    assert_property_value(most_recent, "id", "7")
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
