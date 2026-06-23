"""Test Wikibase Most Recent Statistics Observation Query"""

from datetime import datetime, timezone

import pytest
from data.database_connection import get_async_session
from model.database.wikibase_model import WikibaseModel
from model.database.wikibase_observation.statistics.wikibase_statistics_observation_model import (
    WikibaseStatisticsObservationModel,
)
from tests.test_query.wikibase.statistics_obs.assert_statistics import assert_statistics
from tests.test_query.wikibase.statistics_obs.statistics_fragment import (
    WIKIBASE_STATISTICS_OBSERVATION_FRAGMENT,
)
from tests.test_schema import test_schema
from tests.utils import assert_property_value

WIKIBASE_STATISTICS_MOST_RECENT_OBSERVATION_QUERY = """
query MyQuery($wikibaseId: Int!) {
  wikibase(wikibaseId: $wikibaseId) {
    id
    statisticsObservations {
      mostRecent {
        ...WikibaseStatisticsObservationFragment
      }
    }
  }
}

""" + WIKIBASE_STATISTICS_OBSERVATION_FRAGMENT


@pytest.fixture
async def wikibase_with_statistics(db_session):  # pylint: disable=unused-argument
    """Create a wikibase with a statistics observation"""
    async with get_async_session() as session:
        wikibase = WikibaseModel(
            wikibase_name="Aggregate Statistics Test Wikibase",
            base_url="https://aggregate-statistics-example.com",
        )
        wikibase.checked = True
        wikibase.reuse = True
        wikibase.test = False
        wikibase.wikibase_type = None
        session.add(wikibase)
        await session.flush()
        await session.refresh(wikibase)

        obs = WikibaseStatisticsObservationModel()
        obs.wikibase_id = wikibase.id
        obs.returned_data = True
        obs.observation_date = datetime(2024, 3, 1, tzinfo=timezone.utc)
        obs.total_pages = 12655622
        obs.content_pages = 851723
        obs.total_files = 30
        obs.total_edits = 36150323
        obs.content_page_word_count_total = 27750
        obs.total_users = 465
        obs.active_users = 5
        obs.total_admin = 17
        session.add(obs)
        await session.flush()
        return wikibase


@pytest.mark.asyncio
# @pytest.mark.dependency(depends=["statistics-success"], scope="session")
@pytest.mark.query
@pytest.mark.statistics
async def test_wikibase_statistics_most_recent_observation_query(
    wikibase_with_statistics,
):  # pylint: disable=redefined-outer-name
    """Test Wikibase Most Recent Statistics Observation"""

    wikibase_id = wikibase_with_statistics.id

    result = await test_schema.execute(
        WIKIBASE_STATISTICS_MOST_RECENT_OBSERVATION_QUERY,
        variable_values={"wikibaseId": wikibase_id},
    )

    assert result.errors is None
    assert result.data is not None
    assert "wikibase" in result.data
    result_wikibase = result.data["wikibase"]
    assert_property_value(result_wikibase, "id", str(wikibase_id))
    assert "statisticsObservations" in result_wikibase
    assert "mostRecent" in result_wikibase["statisticsObservationsisticsObservations"]
    most_recent = result_wikibase["statisticsObservations"]["mostRecent"]

    assert_statistics(
        most_recent,
        "2",
        True,
        (36150323, 36150323 / 12655622),  # edits
        (30,),  # files
        (851723, 27750 / 851723, 27750, 12655622),  # pages
        (5, 17, 465),  # users
    )
