"""Test Wikibase Most Recent URL Observation Query"""

import pytest
from tests.test_schema import test_schema
from tests.utils import assert_property_value, get_mock_context


WIKIBASE_URL_MOST_RECENT_OBSERVATION_QUERY = (
    """
query MyQuery($wikibaseId: Int!) {
  wikibase(wikibaseId: $wikibaseId) {
    id
    urlObservations {
      mostRecent {
        id
        observationDate
        returnedData
        totalUrlProperties
        totalUrlStatements
      }
    }
  }
}
"""
)


@pytest.mark.asyncio
@pytest.mark.dependency(depends=["quantity-success"], scope="session")
@pytest.mark.query
@pytest.mark.quantity
async def test_wikibase_url_most_recent_observation_query():
    """Test Wikibase Most Recent URL Observation"""

    result = await test_schema.execute(
        WIKIBASE_URL_MOST_RECENT_OBSERVATION_QUERY,
        variable_values={"wikibaseId": 1},
        context_value=get_mock_context("test-auth-token"),
    )

    assert result.errors is None
    assert result.data is not None
    assert "wikibase" in result.data
    result_wikibase = result.data["wikibase"]
    assert_property_value(result_wikibase, "id", "1")

    assert "urlObservations" in result_wikibase
    most_recent = result_wikibase["urlObservations"]["mostRecent"]
    assert most_recent is not None
    assert_property_value(most_recent, "id", "1")
    assert_property_value(most_recent, "returnedData", True)
    assert_property_value(most_recent, "totalUrlProperties", 64)
    assert_property_value(most_recent, "totalUrlStatements", 128)

