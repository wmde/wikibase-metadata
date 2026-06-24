"""Test Wikibase All Statistics Observations"""

from datetime import datetime, timezone

import pytest
from data.database_connection import get_async_session
from model.database.wikibase_model import WikibaseModel
from model.database.wikibase_observation.statistics.wikibase_statistics_observation_model import WikibaseStatisticsObservationModel
from tests.test_query.wikibase.statistics_obs.assert_statistics import assert_statistics
from tests.test_query.wikibase.statistics_obs.statistics_fragment import (
    WIKIBASE_STATISTICS_OBSERVATION_FRAGMENT,
)
from tests.test_schema import test_schema
from tests.utils import assert_property_value

WIKIBASE_STATISTICS_ALL_OBSERVATIONS_QUERY = """
query MyQuery($wikibaseId: Int!) {
  wikibase(wikibaseId: $wikibaseId) {
    id
    statisticsObservations {
      allObservations {
        ...WikibaseStatisticsObservationFragment
      }
    }
  }
}

""" + WIKIBASE_STATISTICS_OBSERVATION_FRAGMENT

@pytest.fixture
async def wikibase_with_three_statistics_observations(db_session): # pylint: disable=unused-argument
    """Create a wikibase with 3 statistics observations: failed, success, failed"""
    async with get_async_session() as session:
        wikibase = WikibaseModel(
            wikibase_name="Statistics All Observations Test Wikibase",
            base_url="https://statistics-all-obs-example.com",
        )
        wikibase.checked = True
        wikibase.reuse = True
        wikibase.test = False
        wikibase.wikibase_type = None
        session.add(wikibase)
        await session.flush()
        await session.refresh(wikibase)

        obs0 = WikibaseStatisticsObservationModel()
        obs0.wikibase_id = wikibase.id
        obs0.returned_data = False
        obs0.observation_date = datetime(2024, 3, 1, tzinfo=timezone.utc)
        session.add(obs0)
        await session.flush()
        await session.refresh(obs0)

        obs1 = WikibaseStatisticsObservationModel()
        obs1.wikibase_id = wikibase.id
        obs1.returned_data = True
        obs1.observation_date = datetime(2024, 3, 2, tzinfo=timezone.utc)
        obs1.total_pages = 12655622
        obs1.content_pages = 851723
        obs1.total_files = 30
        obs1.total_edits = 36150323
        obs1.content_page_word_count_total = 27750
        obs1.total_users = 465
        obs1.active_users = 5
        obs1.total_admin = 17
        session.add(obs1)
        await session.flush()
        await session.refresh(obs1)

        obs2 = WikibaseStatisticsObservationModel()
        obs2.wikibase_id = wikibase.id
        obs2.returned_data = False
        obs2.observation_date = datetime(2024, 3, 3, tzinfo=timezone.utc)
        session.add(obs2)
        await session.flush()
        await session.refresh(obs2)

        wikibase_id = wikibase.id
        obs_ids = [str(obs0.id), str(obs1.id), str(obs2.id)]

    return wikibase_id, obs_ids


@pytest.mark.asyncio
@pytest.mark.query
@pytest.mark.statistics
async def test_wikibase_statistics_all_observations_query(wikibase_with_three_statistics_observations): # pylint: disable=redefined-outer-name
    """Test Wikibase All Statistics Observations"""

    wikibase_id, obs_ids = wikibase_with_three_statistics_observations

    result = await test_schema.execute(
        WIKIBASE_STATISTICS_ALL_OBSERVATIONS_QUERY,
        variable_values={"wikibaseId": wikibase_id},
    )

    assert result.errors is None
    assert result.data is not None
    assert "wikibase" in result.data
    result_wikibase = result.data["wikibase"]
    assert_property_value(result_wikibase, "id", str(wikibase_id))
    assert "statisticsObservations" in result_wikibase

    assert "allObservations" in result_wikibase["statisticsObservations"]
    statistics_observation_list = result_wikibase["statisticsObservations"]["allObservations"]
    assert len(statistics_observation_list) == 3

    assert_statistics(statistics_observation_list[0], obs_ids[0], False)
    assert_statistics(
        statistics_observation_list[1],
        obs_ids[1],
        True,
        (36150323, 36150323 / 12655622),
        (30,),
        (851723, 27750 / 851723, 27750, 12655622),
        (5, 17, 465),
    )
    assert_statistics(statistics_observation_list[2], obs_ids[2], False)