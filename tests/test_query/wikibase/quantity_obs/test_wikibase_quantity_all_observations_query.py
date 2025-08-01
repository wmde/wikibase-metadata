"""Test Wikibase All Quantity Observations"""

import pytest
from tests.test_query.wikibase.quantity_obs.assert_quantity import assert_quantity
from tests.test_query.wikibase.quantity_obs.quantity_fragment import (
    WIKIBASE_QUANTITY_OBSERVATION_FRAGMENT,
)
from tests.test_schema import test_schema
from tests.utils import assert_property_value, get_mock_context


WIKIBASE_QUANTITY_ALL_OBSERVATIONS_QUERY = (
    """
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

"""
    + WIKIBASE_QUANTITY_OBSERVATION_FRAGMENT
)


@pytest.mark.asyncio
@pytest.mark.dependency(
    depends=["quantity-success", "quantity-failure"], scope="session"
)
@pytest.mark.query
@pytest.mark.quantity
async def test_wikibase_quantity_all_observations_query():
    """Test Wikibase All Quantity Observations"""

    result = await test_schema.execute(
        WIKIBASE_QUANTITY_ALL_OBSERVATIONS_QUERY,
        variable_values={"wikibaseId": 1},
        context_value=get_mock_context("test-auth-token"),
    )

    assert result.errors is None
    assert result.data is not None
    assert "wikibase" in result.data
    result_wikibase = result.data["wikibase"]
    assert_property_value(result_wikibase, "id", "1")
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
        expected_external_identifier_properties,
        expected_external_identifier_statements,
        expected_url_properties,
        expected_url_statements,
    ) in enumerate(
        [
            ("1", True, 2, 4, 1, 8, 16, 32, 64, 128),
            ("2", False, 2, None, 1, None, None, None, None, None),
        ]
    ):
        print(
            quantity_observation_list[index],
        )
        assert_quantity(
            quantity_observation_list[index],
            expected_id,
            expected_returned_data,
            expected_items,
            expected_lexemes,
            expected_properties,
            expected_triples,
            expected_external_identifier_properties,
            expected_external_identifier_statements,
            expected_url_properties,
            expected_url_statements,
        )
