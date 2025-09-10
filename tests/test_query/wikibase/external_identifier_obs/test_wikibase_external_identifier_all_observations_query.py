"""Test Wikibase All External Identifier Observations"""

import pytest
from tests.test_query.wikibase.external_identifier_obs.assert_external_identifier import (
    assert_external_identifier,
)
from tests.test_query.wikibase.external_identifier_obs.external_identifier_fragment import (
    WIKIBASE_EXTERNAL_IDENTIFIER_OBSERVATION_FRAGMENT,
)
from tests.test_schema import test_schema
from tests.utils import assert_property_value, get_mock_context


WIKIBASE_EXTERNAL_IDENTIFIER_ALL_OBSERVATIONS_QUERY = (
    """
query MyQuery($wikibaseId: Int!) {
  wikibase(wikibaseId: $wikibaseId) {
    id
    externalIdentifierObservations {
      allObservations {
        ...WikibaseExternalIdentifierObservationFragment
      }
    }
  }
}

"""
    + WIKIBASE_EXTERNAL_IDENTIFIER_OBSERVATION_FRAGMENT
)


@pytest.mark.asyncio
@pytest.mark.dependency(
    depends=["external-identifier-success", "external-identifier-failure"],
    scope="session",
)
@pytest.mark.query
@pytest.mark.ei
async def test_wikibase_external_identifier_all_observations_query():
    """Test Wikibase All External Identifier Observations"""

    result = await test_schema.execute(
        WIKIBASE_EXTERNAL_IDENTIFIER_ALL_OBSERVATIONS_QUERY,
        variable_values={"wikibaseId": 1},
        context_value=get_mock_context("test-auth-token"),
    )

    assert result.errors is None
    assert result.data is not None
    assert "wikibase" in result.data
    result_wikibase = result.data["wikibase"]
    assert_property_value(result_wikibase, "id", "1")
    assert "externalIdentifierObservations" in result_wikibase

    assert "allObservations" in result_wikibase["externalIdentifierObservations"]
    assert (
        len(
            external_identifier_observation_list := result_wikibase[
                "externalIdentifierObservations"
            ]["allObservations"]
        )
        == 2
    )

    for index, (
        expected_id,
        expected_returned_data,
        expected_external_identifier_properties,
        expected_external_identifier_statements,
        expected_url_properties,
        expected_url_statements,
    ) in enumerate(
        [
            ("1", True, 16, 32, 64, 128),
            ("2", False, None, None, None, None),
        ]
    ):
        assert_external_identifier(
            external_identifier_observation_list[index],
            expected_id,
            expected_returned_data,
            expected_external_identifier_properties,
            expected_external_identifier_statements,
            expected_url_properties,
            expected_url_statements,
        )
