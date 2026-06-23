"""Test Wikibase Most Recent Quantity Observation Query"""

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
from tests.utils import get_mock_context

WIKIBASE_QUANTITY_MOST_RECENT_OBSERVATION_QUERY = """
query MyQuery($wikibaseId: Int!) {
  wikibase(wikibaseId: $wikibaseId) {
    id
    quantityObservations {
      mostRecent {
        ...WikibaseQuantityObservationFragment
      }
    }
  }
}

""" + WIKIBASE_QUANTITY_OBSERVATION_FRAGMENT

FETCH_QUANTITY_MUTATION = """mutation MyMutation($wikibaseId: Int!) {
  fetchQuantityData(wikibaseId: $wikibaseId)
}"""


@pytest.fixture
async def test_fixture(db_session, mocker, wikibase_fixture): # pylint: disable=unused-argument
    """Create Wikibase Test Fixture"""

    mocker.patch(
        "fetch_data.sparql_data.create_quantity_data_observation.get_sparql_results",
        side_effect=[
            {"results": {"bindings": [{"count": {"value": 1}}]}},  # Properties
            {"results": {"bindings": [{"count": {"value": 2}}]}},  # Items
            {"results": {"bindings": [{"count": {"value": 4}}]}},  # Lexemes
            {"results": {"bindings": [{"count": {"value": 8}}]}},  # Triples
        ],
    )

    result = await test_schema.execute(
        FETCH_QUANTITY_MUTATION,
        variable_values={"wikibaseId": wikibase_fixture.id},
        context_value=get_mock_context("test-auth-token"),
    )

    print("asdf")
    print(result)

    return wikibase_fixture


@pytest.fixture
async def wikibase_with_quantity_observation(
    db_session,
):  # pylint: disable=unused-argument
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

        wikibase_id = wikibase.id
        obs1_id = str(obs1.id)
    return wikibase_id, obs1_id


@pytest.mark.asyncio
# @pytest.mark.dependency(depends=["quantity-success"], scope="session")
@pytest.mark.query
@pytest.mark.quantity
async def test_wikibase_quantity_most_recent_observation_query(
    wikibase_with_quantity_observation,
):  # pylint: disable=redefined-outer-name
    """Test Wikibase Most Recent Quantity Observation"""

    wikibase_id, obs1_id = wikibase_with_quantity_observation

    result = await test_schema.execute(
        WIKIBASE_QUANTITY_MOST_RECENT_OBSERVATION_QUERY,
        variable_values={"wikibaseId": wikibase_id},
    )

    assert result.errors is None
    assert result.data is not None
    assert "wikibase" in result.data
    result_wikibase = result.data["wikibase"]
    assert_property_value(result_wikibase, "id", str(wikibase_id))
    assert "quantityObservations" in result_wikibase
    assert "mostRecent" in result_wikibase["quantityObservations"]
    most_recent = result_wikibase["quantityObservations"]["mostRecent"]

    assert_quantity(most_recent, str(obs1_id), True, 2, 4, 1, 8)
