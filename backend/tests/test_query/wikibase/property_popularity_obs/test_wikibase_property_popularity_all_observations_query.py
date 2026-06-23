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