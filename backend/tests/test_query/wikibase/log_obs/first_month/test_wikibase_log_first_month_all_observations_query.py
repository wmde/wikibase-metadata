"""Test Wikibase All Log Observations Query"""

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
)
from datetime import timezone
from model.database import WikibaseModel, WikibaseLogMonthObservationModel, WikibaseLogMonthLogTypeObservationModel, WikibaseLogMonthUserTypeObservationModel
from model.enum import WikibaseLogType, WikibaseUserType
from data.database_connection import get_async_session

WIKIBASE_LOG_ALL_OBSERVATIONS_QUERY = """
query MyQuery($wikibaseId: Int!) {
  wikibase(wikibaseId: $wikibaseId) {
    id
    logObservations {
      firstMonth {
        allObservations {
          ...WikibaseLogMonthFragment
        }
      }
    }
  }
}

""" + WIKIBASE_LOG_OBSERVATION_FRAGMENT


@freeze_time(datetime(2024, 4, 1))
@pytest.mark.asyncio
@pytest.mark.log
@pytest.mark.query
async def test_wikibase_log_first_month_all_observations_query(wikibase_with_first_month_log_observations):
    """Test Wikibase All Log Observations Query"""

    data = wikibase_with_first_month_log_observations
    wikibase_id = data["wikibase_id"]
    observation_ids = data["obs"]
    log_type_ids = data["log_type"]
    user_type_ids = data["user_type"]

    result = await test_schema.execute(
        WIKIBASE_LOG_ALL_OBSERVATIONS_QUERY, variable_values={"wikibaseId": wikibase_id}
    )

    assert result.errors is None
    assert result.data is not None
    assert "wikibase" in result.data
    result_wikibase = result.data["wikibase"]
    assert_property_value(result_wikibase, "id", str(wikibase_id))
    assert "logObservations" in result_wikibase
    assert "firstMonth" in result_wikibase["logObservations"]
    assert "allObservations" in result_wikibase["logObservations"]["firstMonth"]

    log_observation_list = result_wikibase["logObservations"]["firstMonth"]["allObservations"]
    assert len(log_observation_list) == 3

    assert_layered_property_value(log_observation_list, [0, "id"], observation_ids[0])
    assert_layered_property_value(
        log_observation_list, [0, "observationDate"], datetime(2024, 2, 1).strftime(DATETIME_FORMAT)
    )
    assert_layered_property_value(log_observation_list, [0, "returnedData"], True)
    assert_layered_property_value(
        log_observation_list, [0, "firstLog", "date"], datetime(2024, 1, 1).strftime(DATETIME_FORMAT)
    )
    assert_layered_property_value(
        log_observation_list, [0, "lastLog", "date"], datetime(2024, 1, 1).strftime(DATETIME_FORMAT)
    )
    assert_layered_property_value(log_observation_list, [0, "lastLog", "userType"], None)
    assert_layered_property_value(log_observation_list, [0, "logCount"], 1)
    assert_layered_property_value(log_observation_list, [0, "allUsers"], 0)
    assert_layered_property_value(log_observation_list, [0, "activeUsers"], 0)
    assert_layered_property_value(log_observation_list, [0, "humanUsers"], 0)
    assert_layered_property_value(log_observation_list, [0, "activeHumanUsers"], 0)

    assert_layered_property_count(log_observation_list, [0, "logTypeRecords"], 1)
    assert_month_type_record(
        log_observation_list[0]["logTypeRecords"][0],
        expected_id=log_type_ids[0],
        expected_log_type="THANK",
        expected_first_log_date=datetime(2024, 1, 1),
        expected_last_log_date=datetime(2024, 1, 1),
        expected_log_count=1,
        expected_user_count=0,
        expected_active_user_count=0,
        expected_human_count=0,
        expected_active_human_count=0,
    )
    assert_layered_property_count(log_observation_list, [0, "userTypeRecords"], 0)

    assert_layered_property_value(log_observation_list, [1, "id"], observation_ids[1])
    assert_layered_property_value(
        log_observation_list, [1, "observationDate"], datetime(2024, 3, 1).strftime(DATETIME_FORMAT)
    )
    assert_layered_property_value(log_observation_list, [1, "returnedData"], True)
    assert_layered_property_value(
        log_observation_list, [1, "firstLog", "date"], datetime(2023, 10, 24).strftime(DATETIME_FORMAT)
    )
    assert_layered_property_value(
        log_observation_list, [1, "lastLog", "date"], datetime(2023, 11, 23).strftime(DATETIME_FORMAT)
    )
    assert_layered_property_value(log_observation_list, [1, "lastLog", "userType"], "USER")
    assert_layered_property_value(log_observation_list, [1, "logCount"], 31)
    assert_layered_property_value(log_observation_list, [1, "allUsers"], 3)
    assert_layered_property_value(log_observation_list, [1, "activeUsers"], 3)
    assert_layered_property_value(log_observation_list, [1, "humanUsers"], 1)
    assert_layered_property_value(log_observation_list, [1, "activeHumanUsers"], 1)

    assert_layered_property_count(log_observation_list, [1, "logTypeRecords"], 1)
    assert_month_type_record(
        log_observation_list[1]["logTypeRecords"][0],
        expected_id=log_type_ids[1],
        expected_log_type="THANK",
        expected_first_log_date=datetime(2023, 10, 24),
        expected_last_log_date=datetime(2023, 11, 23),
        expected_log_count=31,
        expected_user_count=3,
        expected_active_user_count=3,
        expected_human_count=1,
        expected_active_human_count=1,
    )

    assert_layered_property_count(log_observation_list, [1, "userTypeRecords"], 3)
    for index, (
        expected_id,
        expected_user_type,
        expected_first_log_date,
        expected_last_log_date,
        expected_log_count,
        expected_user_count,
        expected_active_user_count,
    ) in enumerate(
        [
            (user_type_ids[0], "BOT", datetime(2023, 10, 26), datetime(2023, 11, 21), 10, 1, 1),
            (user_type_ids[1], "MISSING", datetime(2023, 10, 25), datetime(2023, 11, 22), 10, 1, 1),
            (user_type_ids[2], "USER", datetime(2023, 10, 24), datetime(2023, 11, 23), 11, 1, 1),
        ]
    ):
        assert_month_type_record(
            log_observation_list[1]["userTypeRecords"][index],
            expected_id=expected_id,
            expected_user_type=expected_user_type,
            expected_first_log_date=expected_first_log_date,
            expected_last_log_date=expected_last_log_date,
            expected_log_count=expected_log_count,
            expected_user_count=expected_user_count,
            expected_active_user_count=expected_active_user_count,
        )

    assert_layered_property_value(log_observation_list, [2, "id"], observation_ids[2])
    assert_layered_property_value(
        log_observation_list, [2, "observationDate"], datetime(2024, 3, 2).strftime(DATETIME_FORMAT)
    )
    assert_layered_property_value(log_observation_list, [2, "returnedData"], False)