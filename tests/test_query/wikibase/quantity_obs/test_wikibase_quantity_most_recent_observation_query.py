"""Test Wikibase Most Recent Quantity Observation Query"""

import pytest
from tests.test_query.wikibase.quantity_obs.assert_quantity import assert_quantity
from tests.test_query.wikibase.quantity_obs.quantity_fragment import (
    WIKIBASE_QUANTITY_OBSERVATION_FRAGMENT,
)
from tests.test_schema import test_schema
from tests.utils import assert_property_value, get_mock_context


WIKIBASE_QUANTITY_MOST_RECENT_OBSERVATION_QUERY = (
    """
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

"""
    + WIKIBASE_QUANTITY_OBSERVATION_FRAGMENT
)


@pytest.mark.asyncio
@pytest.mark.dependency(depends=["quantity-success"], scope="session")
@pytest.mark.query
@pytest.mark.quantity
async def test_wikibase_quantity_most_recent_observation_query():
    """Test Wikibase Most Recent Quantity Observation"""

    result = await test_schema.execute(
        WIKIBASE_QUANTITY_MOST_RECENT_OBSERVATION_QUERY,
        variable_values={"wikibaseId": 1},
    )

    assert result.errors is None
    assert result.data is not None
    assert "wikibase" in result.data
    result_wikibase = result.data["wikibase"]
    assert_property_value(result_wikibase, "id", "1")
    assert "quantityObservations" in result_wikibase
    assert "mostRecent" in result_wikibase["quantityObservations"]
    most_recent = result_wikibase["quantityObservations"]["mostRecent"]

    assert_quantity(most_recent, "1", True, 2, 4, 1, 8)
