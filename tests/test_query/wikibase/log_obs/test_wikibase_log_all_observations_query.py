"""Test Wikibase All Log Observations Query"""

from datetime import datetime
from freezegun import freeze_time
import pytest
from tests.test_query.wikibase.log_obs.assert_log import (
    assert_month_record,
    assert_month_type_record,
)
from tests.test_query.wikibase.log_obs.log_fragment import (
    WIKIBASE_LOG_OBSERVATION_FRAGMENT,
)
from tests.test_schema import test_schema
from tests.utils import (
    assert_layered_property_value,
    assert_property_value,
    DATETIME_FORMAT,
)


WIKIBASE_LOG_ALL_OBSERVATIONS_QUERY = (
    """
query MyQuery($wikibaseId: Int!) {
  wikibase(wikibaseId: $wikibaseId) {
    id
    logObservations {
      firstMonth {
        allObservations {
          ...WikibaseLogMonthStrawberryModelFragment
        }
      }
      lastMonth {
        allObservations {
          ...WikibaseLogMonthStrawberryModelFragment
        }
      }
    }
  }
}

"""
    + WIKIBASE_LOG_OBSERVATION_FRAGMENT
)


@freeze_time("2024-04-01")
@pytest.mark.asyncio
@pytest.mark.dependency(
    depends=[
        "log-first-success-1",
        "log-last-success-1",
        "log-success-2",
        "log-failure",
    ],
    scope="session",
)
@pytest.mark.log
@pytest.mark.query
async def test_wikibase_log_all_observations_query():
    """Test Wikibase All Log Observations Query"""

    result = await test_schema.execute(
        WIKIBASE_LOG_ALL_OBSERVATIONS_QUERY, variable_values={"wikibaseId": 1}
    )

    assert result.errors is None
    assert result.data is not None
    assert "wikibase" in result.data
    result_wikibase = result.data["wikibase"]
    assert_property_value(result_wikibase, "id", "1")
    assert "logObservations" in result_wikibase

    assert "allObservations" in result_wikibase["logObservations"]
    assert (
        len(
            user_observation_list := result_wikibase["logObservations"][
                "allObservations"
            ]
        )
        == 3
    )

    assert_layered_property_value(user_observation_list, [0, "id"], "1")
    assert "observationDate" in user_observation_list[0]
    assert_layered_property_value(user_observation_list, [0, "returnedData"], True)
    assert_layered_property_value(user_observation_list, [0, "instanceAge"], 100)
    assert_layered_property_value(
        user_observation_list,
        [0, "firstLog", "date"],
        datetime(2023, 12, 23).strftime(DATETIME_FORMAT),
    )
    assert_month_record(
        user_observation_list[0]["firstMonth"],
        "1",
        datetime(2023, 12, 23),
        datetime(2024, 1, 22),
        31,
        0,
        0,
        1,
        0,
    )
    assert_month_type_record(
        user_observation_list[0]["firstMonth"]["logTypeRecords"][0],
        expected_id="1",
        expected_log_type="THANK",
        expected_first_log_date=datetime(2023, 12, 23),
        expected_last_log_date=datetime(2024, 1, 22),
        expected_log_count=31,
        expected_user_count=0,
        expected_human_count=0,
    )

    assert_layered_property_value(
        user_observation_list,
        [0, "lastLog", "date"],
        datetime(2024, 3, 1).strftime(DATETIME_FORMAT),
    )
    assert_layered_property_value(
        user_observation_list, [0, "lastLog", "userType"], "NONE"
    )
    assert_month_record(
        user_observation_list[0]["lastMonth"],
        "2",
        datetime(2024, 1, 31),
        datetime(2024, 3, 1),
        31,
        0,
        0,
        1,
        0,
    )
    assert_month_type_record(
        user_observation_list[0]["lastMonth"]["logTypeRecords"][0],
        expected_id="2",
        expected_log_type="THANK",
        expected_first_log_date=datetime(2024, 1, 31),
        expected_last_log_date=datetime(2024, 3, 1),
        expected_log_count=31,
        expected_user_count=0,
        expected_human_count=0,
    )

    assert_layered_property_value(user_observation_list, [1, "id"], "2")
    assert "observationDate" in user_observation_list[1]
    assert_layered_property_value(user_observation_list, [1, "returnedData"], False)

    assert_layered_property_value(user_observation_list, [2, "id"], "3")
    assert "observationDate" in user_observation_list[2]
    assert_layered_property_value(user_observation_list, [2, "returnedData"], True)
    assert_layered_property_value(user_observation_list, [2, "instanceAge"], 160)
    assert_layered_property_value(
        user_observation_list,
        [2, "firstLog", "date"],
        datetime(2023, 10, 24).strftime(DATETIME_FORMAT),
    )
    assert_month_record(
        user_observation_list[2]["firstMonth"],
        "3",
        datetime(2023, 10, 24),
        datetime(2023, 11, 23),
        31,
        3,
        1,
        1,
        3,
    )
    assert_month_type_record(
        user_observation_list[2]["firstMonth"]["logTypeRecords"][0],
        expected_id="3",
        expected_log_type="THANK",
        expected_first_log_date=datetime(2023, 10, 24),
        expected_last_log_date=datetime(2023, 11, 23),
        expected_log_count=31,
        expected_user_count=3,
        expected_human_count=1,
    )
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
            user_observation_list[2]["firstMonth"]["userTypeRecords"][index],
            expected_id=expected_id,
            expected_user_type=expected_user_type,
            expected_first_log_date=expected_first_log_date,
            expected_last_log_date=expected_last_log_date,
            expected_log_count=expected_log_count,
            expected_user_count=expected_user_count,
        )

    assert_layered_property_value(
        user_observation_list,
        [2, "lastLog", "date"],
        datetime(2024, 1, 1).strftime(DATETIME_FORMAT),
    )
    assert_layered_property_value(
        user_observation_list, [2, "lastLog", "userType"], "USER"
    )
    assert_layered_property_value(user_observation_list, [2, "lastMonth"], None)
