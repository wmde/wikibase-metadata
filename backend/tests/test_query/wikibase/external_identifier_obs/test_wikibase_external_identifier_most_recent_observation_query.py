"""Test Wikibase Most Recent External Identifier Observation Query"""

import pytest
from backend.tests.utils.mock_request import get_mock_context
from tests.test_query.wikibase.external_identifier_obs.assert_external_identifier import (
    assert_external_identifier,
)
from tests.test_query.wikibase.external_identifier_obs.external_identifier_fragment import (
    WIKIBASE_EXTERNAL_IDENTIFIER_OBSERVATION_FRAGMENT,
)
from tests.test_schema import test_schema
from tests.utils import assert_property_value

WIKIBASE_EXTERNAL_IDENTIFIER_MOST_RECENT_OBSERVATION_QUERY = """
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

""" + WIKIBASE_EXTERNAL_IDENTIFIER_OBSERVATION_FRAGMENT

FETCH_EXTERNAL_IDENTIFIER_MUTATION = """mutation MyMutation($wikibaseId: Int!) {
  fetchExternalIdentifierData(wikibaseId: $wikibaseId)
}"""

@pytest.fixture
async def wikibase(wikibase_fixture, mocker):
    
    print(wikibase_fixture.id)
    """Create a wikibase with a connectivity observation with relationship counts"""
    mocker.patch(
            "fetch_data.sparql_data.create_external_identifier_data_observation.get_sparql_results",
            side_effect=[
                {
                    "results": {"bindings": [{"count": {"value": 16}}]}
                },  # External Identifier Properties
                {
                    "results": {"bindings": [{"count": {"value": 32}}]}
                },  # External Identifier Statements
                {"results": {"bindings": [{"count": {"value": 64}}]}},  # URL Properties
                {"results": {"bindings": [{"count": {"value": 128}}]}},  # URL Statements
            ],
        )

    result = await test_schema.execute(
        FETCH_EXTERNAL_IDENTIFIER_MUTATION,
        variable_values={"wikibaseId": wikibase_fixture.id},
        context_value=get_mock_context("test-auth-token"),
    )

@pytest.mark.asyncio
# @pytest.mark.dependency(depends=["external-identifier-success"], scope="session")
@pytest.mark.query
@pytest.mark.ei
async def test_wikibase_external_identifier_most_recent_observation_query(wikibase, wikibase_fixture):
    """Test Wikibase Most Recent External Identifier Observation"""

    print('asdf')
    result = await test_schema.execute(
        WIKIBASE_EXTERNAL_IDENTIFIER_MOST_RECENT_OBSERVATION_QUERY,
        variable_values={"wikibaseId": wikibase_fixture.id},
    )

    assert result.errors is None
    assert result.data is not None
    assert "wikibase" in result.data
    result_wikibase = result.data["wikibase"]
    assert_property_value(result_wikibase, "id", str(wikibase_fixture.id))
    assert "externalIdentifierObservations" in result_wikibase
    assert "mostRecent" in result_wikibase["externalIdentifierObservations"]
    most_recent = result_wikibase["externalIdentifierObservations"]["mostRecent"]

  # Should be external identifier id
    assert_external_identifier(most_recent, str(wikibase_fixture.id), True, 16, 32, 64, 128)
