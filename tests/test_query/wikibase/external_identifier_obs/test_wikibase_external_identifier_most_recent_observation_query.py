"""Test Wikibase Most Recent External Identifier Observation Query"""

import pytest
from tests.test_query.wikibase.external_identifier_obs.assert_external_identifier import (
    assert_external_identifier,
)
from tests.test_query.wikibase.external_identifier_obs.external_identifier_fragment import (
    WIKIBASE_EXTERNAL_IDENTIFIER_OBSERVATION_FRAGMENT,
)
from tests.test_schema import test_schema
from tests.utils import assert_property_value, get_mock_context


WIKIBASE_EXTERNAL_IDENTIFIER_MOST_RECENT_OBSERVATION_QUERY = (
    """
query MyQuery($wikibaseId: Int!) {
  wikibase(wikibaseId: $wikibaseId) {
    id
    externalIdentifierObservations {
      mostRecent {
        ...WikibaseExternalIdentifierObservationFragment
      }
    }
  }
}

"""
    + WIKIBASE_EXTERNAL_IDENTIFIER_OBSERVATION_FRAGMENT
)


@pytest.mark.asyncio
@pytest.mark.dependency(depends=["external-identifier-success"], scope="session")
@pytest.mark.query
@pytest.mark.ei
async def test_wikibase_external_identifier_most_recent_observation_query():
    """Test Wikibase Most Recent External Identifier Observation"""

    result = await test_schema.execute(
        WIKIBASE_EXTERNAL_IDENTIFIER_MOST_RECENT_OBSERVATION_QUERY,
        variable_values={"wikibaseId": 1},
        context_value=get_mock_context("test-auth-token"),
    )

    assert result.errors is None
    assert result.data is not None
    assert "wikibase" in result.data
    result_wikibase = result.data["wikibase"]
    assert_property_value(result_wikibase, "id", "1")
    assert "externalIdentifierObservations" in result_wikibase
    assert "mostRecent" in result_wikibase["externalIdentifierObservations"]
    most_recent = result_wikibase["externalIdentifierObservations"]["mostRecent"]

    assert_external_identifier(most_recent, "1", True, 16, 32, 64, 128)
