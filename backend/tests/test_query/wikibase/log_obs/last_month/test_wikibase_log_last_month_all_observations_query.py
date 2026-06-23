"""Test Wikibase All Log Observations Query"""

from datetime import datetime, timezone
from freezegun import freeze_time
import pytest
from data.database_connection import get_async_session
from model.database.wikibase_model import WikibaseModel
from model.database.wikibase_observation.log.wikibase_log_month_log_type_observation_model import (
    WikibaseLogMonthLogTypeObservationModel,
)
from model.database.wikibase_observation.log.wikibase_log_month_observation_model import (
    WikibaseLogMonthObservationModel,
)
from model.enum.wikibase_log_type_enum import WikibaseLogType
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

WIKIBASE_LOG_ALL_OBSERVATIONS_QUERY = """
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

""" + WIKIBASE_LOG_OBSERVATION_FRAGMENT


@pytest.fixture
async def wikibase_with_four_log_observations(db_session):
    """Create a wikibase with 4 last-month log observations"""
    async with get_async_session() as session:
        wikibase = WikibaseModel(
            wikibase_name="Log All Observations Test Wikibase",
            base_url="https://log-all-obs-example.com",
        )
        wikibase.checked = True
        wikibase.reuse = True
        wikibase.test = False
        wikibase.wikibase_type = None
        session.add(wikibase)
        await session.flush()
        await session.refresh(wikibase)

        observation_ids = []
        log_type_ids = []

        # observation 0: single THANK log
        obs0 = WikibaseLogMonthObservationModel(
            wikibase_id=wikibase.id, first_month=False
        )
        obs0.returned_data = True
        obs0.observation_date = datetime(2024, 2, 1, tzinfo=timezone.utc)
        obs0.first_log_date = datetime(2024, 2, 1, tzinfo=timezone.utc)
        obs0.last_log_date = datetime(2024, 2, 1, tzinfo=timezone.utc)
        obs0.log_count = 1
        obs0.user_count = 0
        obs0.active_user_count = 0
        obs0.human_user_count = 0
        obs0.active_human_user_count = 0
        session.add(obs0)
        await session.flush()
        await session.refresh(obs0)

        lt0 = WikibaseLogMonthLogTypeObservationModel()
        lt0.log_month_observation_id = obs0.id
        lt0.log_type = WikibaseLogType.THANK
        lt0.first_log_date = datetime(2024, 2, 1, tzinfo=timezone.utc)
        lt0.last_log_date = datetime(2024, 2, 1, tzinfo=timezone.utc)
        lt0.log_count = 1
        lt0.user_count = 0
        lt0.active_user_count = 0
        lt0.human_user_count = 0
        lt0.active_human_user_count = 0
        session.add(lt0)
        await session.flush()
        await session.refresh(lt0)
        observation_ids.append(str(obs0.id))
        log_type_ids.append(str(lt0.id))

        # observation 1: 31 THANK logs over the month
        obs1 = WikibaseLogMonthObservationModel(
            wikibase_id=wikibase.id, first_month=False
        )
        obs1.returned_data = True
        obs1.observation_date = datetime(2024, 3, 1, tzinfo=timezone.utc)
        obs1.first_log_date = datetime(2024, 1, 31, tzinfo=timezone.utc)
        obs1.last_log_date = datetime(2024, 3, 1, tzinfo=timezone.utc)
        obs1.log_count = 31
        obs1.user_count = 0
        obs1.active_user_count = 0
        obs1.human_user_count = 0
        obs1.active_human_user_count = 0
        session.add(obs1)
        await session.flush()
        await session.refresh(obs1)

        lt1 = WikibaseLogMonthLogTypeObservationModel()
        lt1.log_month_observation_id = obs1.id
        lt1.log_type = WikibaseLogType.THANK
        lt1.first_log_date = datetime(2024, 1, 31, tzinfo=timezone.utc)
        lt1.last_log_date = datetime(2024, 3, 1, tzinfo=timezone.utc)
        lt1.log_count = 31
        lt1.user_count = 0
        lt1.active_user_count = 0
        lt1.human_user_count = 0
        lt1.active_human_user_count = 0
        session.add(lt1)
        await session.flush()
        await session.refresh(lt1)
        observation_ids.append(str(obs1.id))
        log_type_ids.append(str(lt1.id))

        # observation 2: failed fetch
        obs2 = WikibaseLogMonthObservationModel(
            wikibase_id=wikibase.id, first_month=False
        )
        obs2.returned_data = False
        obs2.observation_date = datetime(2024, 3, 2, tzinfo=timezone.utc)
        session.add(obs2)
        await session.flush()
        await session.refresh(obs2)
        observation_ids.append(str(obs2.id))

        # observation 3: empty success
        obs3 = WikibaseLogMonthObservationModel(
            wikibase_id=wikibase.id, first_month=False
        )
        obs3.returned_data = True
        obs3.observation_date = datetime(2024, 3, 3, tzinfo=timezone.utc)
        obs3.first_log_date = None
        obs3.last_log_date = None
        obs3.log_count = 0
        obs3.user_count = 0
        obs3.active_user_count = 0
        obs3.human_user_count = 0
        obs3.active_human_user_count = 0
        session.add(obs3)
        await session.flush()
        await session.refresh(obs3)
        observation_ids.append(str(obs3.id))

        wikibase_id = wikibase.id

    return {
        "wikibase_id": wikibase_id,
        "observation_ids": observation_ids,
        "log_type_ids": log_type_ids,
    }


@freeze_time(datetime(2024, 4, 1))
@pytest.mark.asyncio
@pytest.mark.log
@pytest.mark.query
async def test_wikibase_log_last_month_all_observations_query(
    wikibase_with_four_log_observations,
):
    """Test Wikibase All Log Observations Query"""

    wikibase_id = wikibase_with_four_log_observations["wikibase_id"]
    obs_ids = wikibase_with_four_log_observations["observation_ids"]
    lt_ids = wikibase_with_four_log_observations["log_type_ids"]

    result = await test_schema.execute(
        WIKIBASE_LOG_ALL_OBSERVATIONS_QUERY, variable_values={"wikibaseId": wikibase_id}
    )

    assert result.errors is None
    assert result.data is not None
    assert "wikibase" in result.data
    result_wikibase = result.data["wikibase"]
    assert_property_value(result_wikibase, "id", str(wikibase_id))
    assert "logObservations" in result_wikibase
    assert "lastMonth" in result_wikibase["logObservations"]
    assert "allObservations" in result_wikibase["logObservations"]["lastMonth"]

    log_observation_list = result_wikibase["logObservations"]["lastMonth"][
        "allObservations"
    ]
    assert len(log_observation_list) == 4

    assert_layered_property_value(log_observation_list, [0, "id"], obs_ids[0])
    assert_layered_property_value(
        log_observation_list,
        [0, "observationDate"],
        datetime(2024, 2, 1).strftime(DATETIME_FORMAT),
    )
    assert_layered_property_value(log_observation_list, [0, "returnedData"], True)
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
        expected_id=lt_ids[0],
        expected_log_type="THANK",
        expected_first_log_date=datetime(2024, 2, 1),
        expected_last_log_date=datetime(2024, 2, 1),
        expected_log_count=1,
        expected_user_count=0,
        expected_active_user_count=0,
        expected_human_count=0,
        expected_active_human_count=0,
    )
    assert_layered_property_value(log_observation_list, [0, "allUsers"], 0)
    assert_layered_property_value(log_observation_list, [0, "activeUsers"], 0)
    assert_layered_property_value(log_observation_list, [0, "humanUsers"], 0)
    assert_layered_property_value(log_observation_list, [0, "activeHumanUsers"], 0)
    assert_layered_property_count(log_observation_list, [0, "userTypeRecords"], 0)

    assert_layered_property_value(log_observation_list, [1, "id"], obs_ids[1])
    assert_layered_property_value(
        log_observation_list,
        [1, "observationDate"],
        datetime(2024, 3, 1).strftime(DATETIME_FORMAT),
    )
    assert_layered_property_value(log_observation_list, [1, "returnedData"], True)
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
        expected_id=lt_ids[1],
        expected_log_type="THANK",
        expected_first_log_date=datetime(2024, 1, 31),
        expected_last_log_date=datetime(2024, 3, 1),
        expected_log_count=31,
        expected_user_count=0,
        expected_active_user_count=0,
        expected_human_count=0,
        expected_active_human_count=0,
    )
    assert_layered_property_value(log_observation_list, [1, "allUsers"], 0)
    assert_layered_property_value(log_observation_list, [1, "activeUsers"], 0)
    assert_layered_property_value(log_observation_list, [1, "humanUsers"], 0)
    assert_layered_property_value(log_observation_list, [1, "activeHumanUsers"], 0)
    assert_layered_property_count(log_observation_list, [1, "userTypeRecords"], 0)

    assert_layered_property_value(log_observation_list, [2, "id"], obs_ids[2])
    assert_layered_property_value(
        log_observation_list,
        [2, "observationDate"],
        datetime(2024, 3, 2).strftime(DATETIME_FORMAT),
    )
    assert_layered_property_value(log_observation_list, [2, "returnedData"], False)

    assert_layered_property_value(log_observation_list, [3, "id"], obs_ids[3])
    assert_layered_property_value(
        log_observation_list,
        [3, "observationDate"],
        datetime(2024, 3, 3).strftime(DATETIME_FORMAT),
    )
    assert_layered_property_value(log_observation_list, [3, "returnedData"], True)
    assert_layered_property_value(log_observation_list, [3, "firstLog"], None)
    assert_layered_property_value(log_observation_list, [3, "lastLog"], None)
    assert_layered_property_value(log_observation_list, [3, "logCount"], 0)
    assert_layered_property_count(log_observation_list, [3, "logTypeRecords"], 0)
    assert_layered_property_value(log_observation_list, [3, "allUsers"], 0)
    assert_layered_property_value(log_observation_list, [3, "activeUsers"], 0)
    assert_layered_property_value(log_observation_list, [3, "humanUsers"], 0)
    assert_layered_property_value(log_observation_list, [3, "activeHumanUsers"], 0)
    assert_layered_property_count(log_observation_list, [3, "userTypeRecords"], 0)
