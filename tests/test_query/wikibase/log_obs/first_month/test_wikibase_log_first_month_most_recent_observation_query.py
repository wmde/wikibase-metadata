"""Test Wikibase Most Recent Log Observation"""

from datetime import datetime
from freezegun import freeze_time
import pytest
from tests.test_query.wikibase.log_obs.assert_log import assert_month_type_record
from tests.test_query.wikibase.log_obs.log_fragment import (
    WIKIBASE_LOG_OBSERVATION_FRAGMENT,
)
from tests.test_schema import test_schema
from tests.utils import (
    assert_layered_property_count,
    assert_layered_property_value,
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
      firstMonth {
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
@pytest.mark.dependency(depends=["log-first-success-1"], scope="session")
@pytest.mark.log
@pytest.mark.query
async def test_wikibase_log_first_month_most_recent_observation_query():
    """Test Wikibase Most Recent Log Observation"""

    result = await test_schema.execute(
        WIKIBASE_LOG_MOST_RECENT_OBSERVATION_QUERY,
        variable_values={"wikibaseId": 1},
        context_value=get_mock_context("test-auth-token"),
    )

    assert result.errors is None
    assert result.data is not None
    assert "wikibase" in result.data
    result_wikibase = result.data["wikibase"]
    assert_property_value(result_wikibase, "id", "1")
    assert "logObservations" in result_wikibase
    assert "firstMonth" in result_wikibase["logObservations"]
    assert "mostRecent" in result_wikibase["logObservations"]["firstMonth"]
    most_recent = result_wikibase["logObservations"]["firstMonth"]["mostRecent"]

    assert_property_value(most_recent, "id", "2")
    assert_property_value(
        most_recent, "observationDate", datetime(2024, 3, 1).strftime(DATETIME_FORMAT)
    )
    assert_property_value(most_recent, "returnedData", True)
    # assert_layered_property_value(log_observation_list, [0, "instanceAge"], 100)
    assert_layered_property_value(
        most_recent,
        ["firstLog", "date"],
        datetime(2023, 10, 24).strftime(DATETIME_FORMAT),
    )
    assert_layered_property_value(
        most_recent,
        ["lastLog", "date"],
        datetime(2023, 11, 23).strftime(DATETIME_FORMAT),
    )
    assert_layered_property_value(most_recent, ["lastLog", "userType"], "USER")
    assert_property_value(most_recent, "logCount", 31)
    assert_property_value(most_recent, "allUsers", 3)
    assert_property_value(most_recent, "humanUsers", 1)

    assert_layered_property_count(most_recent, ["logTypeRecords"], 1)
    assert_month_type_record(
        most_recent["logTypeRecords"][0],
        expected_id="2",
        expected_log_type="THANK",
        expected_first_log_date=datetime(2023, 10, 24),
        expected_last_log_date=datetime(2023, 11, 23),
        expected_log_count=31,
        expected_user_count=3,
        expected_human_count=1,
    )

    assert_layered_property_count(most_recent, ["userTypeRecords"], 3)
    for index, (
        expected_id,
        expected_user_type,
        expected_first_log_date,
        expected_last_log_date,
        expected_log_count,
        expected_user_count,
    ) in enumerate(
        [
            ("1", "BOT", datetime(2023, 10, 26), datetime(2023, 11, 21), 10, 1),
            ("2", "MISSING", datetime(2023, 10, 25), datetime(2023, 11, 22), 10, 1),
            ("3", "USER", datetime(2023, 10, 24), datetime(2023, 11, 23), 11, 1),
        ]
    ):
        assert_month_type_record(
            most_recent["userTypeRecords"][index],
            expected_id=expected_id,
            expected_user_type=expected_user_type,
            expected_first_log_date=expected_first_log_date,
            expected_last_log_date=expected_last_log_date,
            expected_log_count=expected_log_count,
            expected_user_count=expected_user_count,
        )
