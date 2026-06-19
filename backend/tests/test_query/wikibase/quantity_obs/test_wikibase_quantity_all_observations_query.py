"""Test Wikibase All Quantity Observations"""

from datetime import datetime, timezone

import pytest
from data.database_connection import get_async_session
from model.database.wikibase_model import WikibaseModel
from model.database.wikibase_observation.quantity.wikibase_quantity_observation_model import (
    WikibaseQuantityObservationModel,
)
from tests.test_query.wikibase.quantity_obs.assert_quantity import assert_quantity
from tests.test_query.wikibase.quantity_obs.quantity_fragment import (
    WIKIBASE_QUANTITY_OBSERVATION_FRAGMENT,
)
from tests.test_schema import test_schema
from tests.utils import assert_property_value

WIKIBASE_QUANTITY_ALL_OBSERVATIONS_QUERY = """
query MyQuery($wikibaseId: Int!) {
  wikibase(wikibaseId: $wikibaseId) {
    id
    quantityObservations {
      allObservations {
        ...WikibaseQuantityObservationFragment
      }
    }
  }
}

""" + WIKIBASE_QUANTITY_OBSERVATION_FRAGMENT


@pytest.fixture
async def wikibase_with_two_quantity_observations(db_session):
    """Create a wikibase with two quantity observations"""
    async with get_async_session() as session:
        wikibase = WikibaseModel(
            wikibase_name="Quantity All Observations Test Wikibase",
            base_url="https://quantity-all-obs-example.com",
        )
        wikibase.checked = True
        wikibase.reuse = True
        wikibase.test = False
        wikibase.wikibase_type = None
        session.add(wikibase)
        await session.flush()
        await session.refresh(wikibase)

        obs1 = WikibaseQuantityObservationModel()
        obs1.wikibase_id = wikibase.id
        obs1.returned_data = True
        obs1.observation_date = datetime(2024, 3, 1, tzinfo=timezone.utc)
        obs1.total_items = 2
        obs1.total_lexemes = 4
        obs1.total_properties = 1
        obs1.total_triples = 8
        session.add(obs1)
        await session.flush()
        await session.refresh(obs1)

        obs2 = WikibaseQuantityObservationModel()
        obs2.wikibase_id = wikibase.id
        obs2.returned_data = False
        obs2.observation_date = datetime(2024, 3, 2, tzinfo=timezone.utc)
        obs2.total_items = 2
        obs2.total_lexemes = None
        obs2.total_properties = 1
        obs2.total_triples = None
        session.add(obs2)
        await session.flush()
        await session.refresh(obs2)

        wikibase_id = wikibase.id
        obs1_id = str(obs1.id)
        obs2_id = str(obs2.id)
    return wikibase_id, obs1_id, obs2_id


@pytest.mark.asyncio
@pytest.mark.query
@pytest.mark.quantity
async def test_wikibase_quantity_all_observations_query(
    wikibase_with_two_quantity_observations,
):
    """Test Wikibase All Quantity Observations"""

    wikibase_id, obs1_id, obs2_id = wikibase_with_two_quantity_observations

    result = await test_schema.execute(
        WIKIBASE_QUANTITY_ALL_OBSERVATIONS_QUERY,
        variable_values={"wikibaseId": wikibase_id},
    )

    assert result.errors is None
    assert result.data is not None
    assert "wikibase" in result.data
    result_wikibase = result.data["wikibase"]
    assert_property_value(result_wikibase, "id", str(wikibase_id))
    assert "quantityObservations" in result_wikibase

    assert "allObservations" in result_wikibase["quantityObservations"]
    assert (
        len(
            quantity_observation_list := result_wikibase["quantityObservations"][
                "allObservations"
            ]
        )
        == 2
    )

    for index, (
        expected_id,
        expected_returned_data,
        expected_items,
        expected_lexemes,
        expected_properties,
        expected_triples,
    ) in enumerate(
        [
            (obs1_id, True, 2, 4, 1, 8),
            (obs2_id, False, 2, None, 1, None),
        ]
    ):
        assert_quantity(
            quantity_observation_list[index],
            expected_id,
            expected_returned_data,
            expected_items,
            expected_lexemes,
            expected_properties,
            expected_triples,
        )
