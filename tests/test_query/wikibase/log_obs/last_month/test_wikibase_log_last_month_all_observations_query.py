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


WIKIBASE_LOG_ALL_OBSERVATIONS_QUERY = (
    """
query MyQuery($wikibaseId: Int!) {
  wikibase(wikibaseId: $wikibaseId) {
    id
    logObservations {
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
    depends=["log-last-success-1", "log-last-success-2", "log-last-failure"],
    scope="session",
)
@pytest.mark.log
@pytest.mark.query
async def test_wikibase_log_last_month_all_observations_query():
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
    assert "lastMonth" in result_wikibase["logObservations"]
    assert "allObservations" in result_wikibase["logObservations"]["lastMonth"]

    assert (
        len(
            log_observation_list := result_wikibase["logObservations"]["lastMonth"][
                "allObservations"
            ]
        )
        == 3
    )

    assert_layered_property_value(log_observation_list, [0, "id"], "2")
    assert_layered_property_value(
        log_observation_list,
        [0, "observationDate"],
        datetime(2024, 3, 1).strftime(DATETIME_FORMAT),
    )
    assert_layered_property_value(log_observation_list, [0, "returnedData"], True)
    # assert_layered_property_value(log_observation_list, [0, "instanceAge"], 100)
    assert_layered_property_value(
        log_observation_list,
        [0, "firstLog", "date"],
        datetime(2024, 1, 31).strftime(DATETIME_FORMAT),
    )
    assert_layered_property_value(
        log_observation_list,
        [0, "lastLog", "date"],
        datetime(2024, 3, 1).strftime(DATETIME_FORMAT),
    )
    assert_layered_property_value(
        log_observation_list, [0, "lastLog", "userType"], None
    )
    assert_layered_property_value(log_observation_list, [0, "logCount"], 31)
    assert_layered_property_count(log_observation_list, [0, "logTypeRecords"], 1)
    assert_month_type_record(
        log_observation_list[0]["logTypeRecords"][0],
        expected_id="2",
        expected_log_type="THANK",
        expected_first_log_date=datetime(2024, 1, 31),
        expected_last_log_date=datetime(2024, 3, 1),
        expected_log_count=31,
        expected_user_count=0,
        expected_human_count=0,
    )
    assert_layered_property_value(log_observation_list, [0, "allUsers"], 0)
    assert_layered_property_value(log_observation_list, [0, "humanUsers"], 0)
    assert_layered_property_count(log_observation_list, [0, "userTypeRecords"], 0)

    assert_layered_property_value(log_observation_list, [1, "id"], "4")
    assert_layered_property_value(
        log_observation_list,
        [1, "observationDate"],
        datetime(2024, 3, 2).strftime(DATETIME_FORMAT),
    )
    assert_layered_property_value(log_observation_list, [1, "returnedData"], False)

    assert_layered_property_value(log_observation_list, [2, "id"], "5")
    assert_layered_property_value(
        log_observation_list,
        [2, "observationDate"],
        datetime(2024, 3, 3).strftime(DATETIME_FORMAT),
    )
    assert_layered_property_value(log_observation_list, [2, "returnedData"], True)
    # assert_layered_property_value(log_observation_list, [2, "instanceAge"], 160)
    assert_layered_property_value(log_observation_list, [2, "firstLog"], None)
    assert_layered_property_value(log_observation_list, [2, "lastLog"], None)
    assert_layered_property_value(log_observation_list, [2, "logCount"], 0)
    assert_layered_property_count(log_observation_list, [2, "logTypeRecords"], 0)
    assert_layered_property_value(log_observation_list, [2, "allUsers"], 0)
    assert_layered_property_value(log_observation_list, [2, "humanUsers"], 0)
    assert_layered_property_count(log_observation_list, [2, "userTypeRecords"], 0)
