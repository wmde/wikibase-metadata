"""Test Wikibase All Property Popularity Observations Query"""

import pytest
from tests.test_query.wikibase.property_popularity_obs.assert_property_popularity import (
    assert_property_count,
)
from tests.test_query.wikibase.property_popularity_obs.property_popularity_fragment import (
    WIKIBASE_PROPERTY_POPULARITY_OBSERVATION_FRAGMENT,
)
from tests.test_schema import test_schema
from tests.utils import (
    assert_layered_property_count,
    assert_layered_property_value,
    assert_property_value,
)
from datetime import datetime, timezone
from data.database_connection import get_async_session
from model.database import WikibaseModel, WikibasePropertyPopularityObservationModel
from model.database.wikibase_observation.property.count_model import WikibasePropertyPopularityCountModel

WIKIBASE_PROPERTY_POPULARITY_ALL_OBSERVATIONS_QUERY = """
query MyQuery($wikibaseId: Int!) {
  wikibase(wikibaseId: $wikibaseId) {
    id
    propertyPopularityObservations {
      allObservations {
        ...WikibasePropertyPopularityObservationFragment
      }
    }
  }
}

""" + WIKIBASE_PROPERTY_POPULARITY_OBSERVATION_FRAGMENT


@pytest.fixture
async def wikibase_with_three_property_popularity_observations(db_session):
    """Create a wikibase with 3 property popularity observations: empty, P1/P14, and failed"""
    async with get_async_session() as session:
        wikibase = WikibaseModel(
            wikibase_name="Property Popularity All Observations Test Wikibase",
            base_url="https://property-popularity-all-obs-example.com",
        )
        wikibase.checked = True
        wikibase.reuse = True
        wikibase.test = False
        wikibase.wikibase_type = None
        session.add(wikibase)
        await session.flush()
        await session.refresh(wikibase)

        # observation 0: empty, no properties
        obs0 = WikibasePropertyPopularityObservationModel()
        obs0.wikibase_id = wikibase.id
        obs0.returned_data = True
        obs0.observation_date = datetime(2024, 3, 1, tzinfo=timezone.utc)
        session.add(obs0)
        await session.flush()
        await session.refresh(obs0)

        # observation 1: P1=12, P14=1
        obs1 = WikibasePropertyPopularityObservationModel()
        obs1.wikibase_id = wikibase.id
        obs1.returned_data = True
        obs1.observation_date = datetime(2024, 3, 2, tzinfo=timezone.utc)
        session.add(obs1)
        await session.flush()
        await session.refresh(obs1)

        p1 = WikibasePropertyPopularityCountModel(property_url="P1", usage_count=12)
        p1.wikibase_property_popularity_observation_id = obs1.id
        session.add(p1)

        p14 = WikibasePropertyPopularityCountModel(property_url="P14", usage_count=1)
        p14.wikibase_property_popularity_observation_id = obs1.id
        session.add(p14)

        await session.flush()
        await session.refresh(p1)
        await session.refresh(p14)

        # observation 2: failed fetch
        obs2 = WikibasePropertyPopularityObservationModel()
        obs2.wikibase_id = wikibase.id
        obs2.returned_data = False
        obs2.observation_date = datetime(2024, 3, 3, tzinfo=timezone.utc)
        session.add(obs2)
        await session.flush()
        await session.refresh(obs2)

        wikibase_id = wikibase.id

    return {
        "wikibase_id": wikibase_id,
        "obs0_id": str(obs0.id),
        "obs1_id": str(obs1.id),
        "obs2_id": str(obs2.id),
        "p1_id": str(p1.id),
        "p14_id": str(p14.id),
    }


@pytest.mark.asyncio
@pytest.mark.property
@pytest.mark.query
async def test_wikibase_property_popularity_all_observations_query(wikibase_with_three_property_popularity_observations):
    """Test Wikibase All Property Popularity Observations Query"""

    data = wikibase_with_three_property_popularity_observations
    wikibase_id = data["wikibase_id"]

    result = await test_schema.execute(
        WIKIBASE_PROPERTY_POPULARITY_ALL_OBSERVATIONS_QUERY,
        variable_values={"wikibaseId": wikibase_id},
    )

    assert result.errors is None
    assert result.data is not None
    assert "wikibase" in result.data
    result_wikibase = result.data["wikibase"]
    assert_property_value(result_wikibase, "id", str(wikibase_id))
    assert "propertyPopularityObservations" in result_wikibase

    assert "allObservations" in result_wikibase["propertyPopularityObservations"]
    property_popularity_observation_list = result_wikibase["propertyPopularityObservations"]["allObservations"]
    assert len(property_popularity_observation_list) == 3

    assert_layered_property_value(property_popularity_observation_list, [0, "id"], data["obs0_id"])
    assert "observationDate" in property_popularity_observation_list[0]
    assert_layered_property_value(
        property_popularity_observation_list, [0, "returnedData"], True
    )
    assert_layered_property_count(
        property_popularity_observation_list, [0, "propertyPopularityCounts"], 0
    )

    assert_layered_property_value(property_popularity_observation_list, [1, "id"], data["obs1_id"])
    assert "observationDate" in property_popularity_observation_list[1]
    assert_layered_property_value(
        property_popularity_observation_list, [1, "returnedData"], True
    )
    assert_layered_property_count(
        property_popularity_observation_list, [1, "propertyPopularityCounts"], 2
    )

    for index, (expected_id, expected_property_url, expected_usage_count) in enumerate(
        [
            (data["p1_id"], "P1", 12),
            (data["p14_id"], "P14", 1),
        ]
    ):
        assert_property_count(
            property_popularity_observation_list[1]["propertyPopularityCounts"][index],
            expected_id,
            expected_property_url,
            expected_usage_count,
        )

    assert_layered_property_value(property_popularity_observation_list, [2, "id"], data["obs2_id"])
    assert "observationDate" in property_popularity_observation_list[2]
    assert_layered_property_value(
        property_popularity_observation_list, [2, "returnedData"], False
    )
    assert_layered_property_count(
        property_popularity_observation_list, [2, "propertyPopularityCounts"], 0
    )