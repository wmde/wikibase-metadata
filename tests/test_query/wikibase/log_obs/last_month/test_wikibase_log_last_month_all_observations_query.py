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
    get_mock_context,
)


WIKIBASE_LOG_ALL_OBSERVATIONS_QUERY = (
    """
query MyQuery($wikibaseId: Int!) {
  wikibase(wikibaseId: $wikibaseId) {
    id
    logObservations {
      lastMonth {
        allObservations {
          ...WikibaseLogMonthFragment
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
        "log-last-success-ood",
        "log-last-success-1",
        "log-last-success-2",
        "log-last-failure",
    ],
    scope="session",
)
@pytest.mark.log
@pytest.mark.query
async def test_wikibase_log_last_month_all_observations_query():
    """Test Wikibase All Log Observations Query"""

    result = await test_schema.execute(
        WIKIBASE_LOG_ALL_OBSERVATIONS_QUERY,
        variable_values={"wikibaseId": 1},
        context_value=get_mock_context("test-auth-token"),
    )

    assert result.errors is None
    assert result.data is not None
    assert "wikibase" in result.data
    result_wikibase = result.data["wikibase"]
    assert_property_value(result_wikibase, "id", "1")
    assert "logObservations" in result_wikibase
    assert "lastMonth" in result_wikibase["logObservations"]
    assert "allObservations" in result_wikibase["logObservations"]["lastMonth"]

    assert (
        len(
            log_observation_list := result_wikibase["logObservations"]["lastMonth"][
                "allObservations"
            ]
        )
        == 4
    )

    assert_layered_property_value(log_observation_list, [0, "id"], "4")
    assert_layered_property_value(
        log_observation_list,
        [0, "observationDate"],
        datetime(2024, 2, 1).strftime(DATETIME_FORMAT),
    )
    assert_layered_property_value(log_observation_list, [0, "returnedData"], True)
    # assert_layered_property_value(log_observation_list, [0, "instanceAge"], 100)
    assert_layered_property_value(
        log_observation_list,
        [0, "firstLog", "date"],
        datetime(2024, 2, 1).strftime(DATETIME_FORMAT),
    )
    assert_layered_property_value(
        log_observation_list,
        [0, "lastLog", "date"],
        datetime(2024, 2, 1).strftime(DATETIME_FORMAT),
    )
    assert_layered_property_value(
        log_observation_list, [0, "lastLog", "userType"], None
    )
    assert_layered_property_value(log_observation_list, [0, "logCount"], 1)
    assert_layered_property_count(log_observation_list, [0, "logTypeRecords"], 1)
    assert_month_type_record(
        log_observation_list[0]["logTypeRecords"][0],
        expected_id="3",
        expected_log_type="THANK",
        expected_first_log_date=datetime(2024, 2, 1),
        expected_last_log_date=datetime(2024, 2, 1),
        expected_log_count=1,
        expected_user_count=0,
        expected_human_count=0,
    )
    assert_layered_property_value(log_observation_list, [0, "allUsers"], 0)
    assert_layered_property_value(log_observation_list, [0, "humanUsers"], 0)
    assert_layered_property_count(log_observation_list, [0, "userTypeRecords"], 0)

    assert_layered_property_value(log_observation_list, [1, "id"], "5")
    assert_layered_property_value(
        log_observation_list,
        [1, "observationDate"],
        datetime(2024, 3, 1).strftime(DATETIME_FORMAT),
    )
    assert_layered_property_value(log_observation_list, [1, "returnedData"], True)
    # assert_layered_property_value(log_observation_list, [1, "instanceAge"], 100)
    assert_layered_property_value(
        log_observation_list,
        [1, "firstLog", "date"],
        datetime(2024, 1, 31).strftime(DATETIME_FORMAT),
    )
    assert_layered_property_value(
        log_observation_list,
        [1, "lastLog", "date"],
        datetime(2024, 3, 1).strftime(DATETIME_FORMAT),
    )
    assert_layered_property_value(
        log_observation_list, [1, "lastLog", "userType"], None
    )
    assert_layered_property_value(log_observation_list, [1, "logCount"], 31)
    assert_layered_property_count(log_observation_list, [1, "logTypeRecords"], 1)
    assert_month_type_record(
        log_observation_list[1]["logTypeRecords"][0],
        expected_id="4",
        expected_log_type="THANK",
        expected_first_log_date=datetime(2024, 1, 31),
        expected_last_log_date=datetime(2024, 3, 1),
        expected_log_count=31,
        expected_user_count=0,
        expected_human_count=0,
    )
    assert_layered_property_value(log_observation_list, [1, "allUsers"], 0)
    assert_layered_property_value(log_observation_list, [1, "humanUsers"], 0)
    assert_layered_property_count(log_observation_list, [1, "userTypeRecords"], 0)

    assert_layered_property_value(log_observation_list, [2, "id"], "6")
    assert_layered_property_value(
        log_observation_list,
        [2, "observationDate"],
        datetime(2024, 3, 2).strftime(DATETIME_FORMAT),
    )
    assert_layered_property_value(log_observation_list, [2, "returnedData"], False)

    assert_layered_property_value(log_observation_list, [3, "id"], "7")
    assert_layered_property_value(
        log_observation_list,
        [3, "observationDate"],
        datetime(2024, 3, 3).strftime(DATETIME_FORMAT),
    )
    assert_layered_property_value(log_observation_list, [3, "returnedData"], True)
    # assert_layered_property_value(log_observation_list, [3, "instanceAge"], 160)
    assert_layered_property_value(log_observation_list, [3, "firstLog"], None)
    assert_layered_property_value(log_observation_list, [3, "lastLog"], None)
    assert_layered_property_value(log_observation_list, [3, "logCount"], 0)
    assert_layered_property_count(log_observation_list, [3, "logTypeRecords"], 0)
    assert_layered_property_value(log_observation_list, [3, "allUsers"], 0)
    assert_layered_property_value(log_observation_list, [3, "humanUsers"], 0)
    assert_layered_property_count(log_observation_list, [3, "userTypeRecords"], 0)
