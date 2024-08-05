"""Test Wikibase Most Recent Log Observation"""

from datetime import datetime
from freezegun import freeze_time
import pytest
from tests.test_query.test_wikibase_log_observation_query.assert_month_type_record import (
    assert_month_type_record,
)
from tests.test_query.test_wikibase_log_observation_query.wikibase_log_observation_fragment import (
    WIKIBASE_LOG_OBSERVATION_FRAGMENT,
)
from tests.test_schema import test_schema
from tests.utils import (
    assert_layered_property_count,
    assert_layered_property_value,
    assert_property_value,
)
from tests.utils.datetime_format import DATETIME_FORMAT


WIKIBASE_LOG_MOST_RECENT_OBSERVATION_QUERY = (
    """
query MyQuery($wikibaseId: Int!) {
  wikibase(wikibaseId: $wikibaseId) {
    id
    logObservations {
      mostRecent {
        ...WikibaseLogObservationStrawberryModelFragment
      }
    }
  }
}

"""
    + WIKIBASE_LOG_OBSERVATION_FRAGMENT
)


@freeze_time("2024-04-01")
@pytest.mark.asyncio
@pytest.mark.dependency(depends_on=["log-success-1", "log-success-2"])
@pytest.mark.log
@pytest.mark.query
async def test_wikibase_log_most_recent_observation_query():
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
    assert "mostRecent" in result_wikibase["logObservations"]
    most_recent = result_wikibase["logObservations"]["mostRecent"]

    assert_property_value(most_recent, "id", "3")
    assert "observationDate" in most_recent
    assert_property_value(most_recent, "returnedData", True)
    assert_property_value(most_recent, "instanceAge", 160)
    assert_layered_property_value(
        most_recent,
        ["firstLog", "date"],
        datetime(2023, 10, 24).strftime(DATETIME_FORMAT),
    )
    assert_layered_property_value(most_recent, ["firstMonth", "id"], "3")
    assert_layered_property_value(
        most_recent,
        ["firstMonth", "firstLogDate"],
        datetime(2023, 10, 24).strftime(DATETIME_FORMAT),
    )
    assert_layered_property_value(
        most_recent,
        ["firstMonth", "lastLogDate"],
        datetime(2023, 11, 23).strftime(DATETIME_FORMAT),
    )
    assert_layered_property_value(most_recent, ["firstMonth", "logCount"], 31)
    assert_layered_property_value(most_recent, ["firstMonth", "allUsers"], 3)
    assert_layered_property_value(most_recent, ["firstMonth", "humanUsers"], 1)
    assert_layered_property_count(most_recent, ["firstMonth", "logTypeRecords"], 1)
    assert_month_type_record(
        most_recent["firstMonth"]["logTypeRecords"][0],
        expected_id="3",
        expected_log_type="THANK",
        expected_first_log_date=datetime(2023, 10, 24),
        expected_last_log_date=datetime(2023, 11, 23),
        expected_log_count=31,
        expected_user_count=3,
        expected_human_count=1,
    )
    assert_layered_property_count(most_recent, ["firstMonth", "userTypeRecords"], 3)
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
            most_recent["firstMonth"]["userTypeRecords"][index],
            expected_id=expected_id,
            expected_user_type=expected_user_type,
            expected_first_log_date=expected_first_log_date,
            expected_last_log_date=expected_last_log_date,
            expected_log_count=expected_log_count,
            expected_user_count=expected_user_count,
        )

    assert_layered_property_value(
        most_recent, ["lastLog", "date"], datetime(2024, 1, 1).strftime(DATETIME_FORMAT)
    )
    assert_layered_property_value(most_recent, ["lastLog", "userType"], "USER")
    assert_property_value(most_recent, "lastMonth", None)
