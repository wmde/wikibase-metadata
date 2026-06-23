"""Test Wikibase Most Recent External Identifier Observation Query"""

from select import select

import pytest
from model.database.wikibase_observation.external_identifier.wikibase_ei_obs_model import (
    WikibaseExternalIdentifierObservationModel,
)
from data.database_connection import get_async_session
from model.database.wikibase_model import WikibaseModel
from tests.utils.mock_request import get_mock_context
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
async def wikibase_with_ei_observation(
    db_session, mocker
):  # pylint: disable=unused-argument
    """Create a wikibase with an EI observation via mutation"""
    async with get_async_session() as session:
        wikibase = WikibaseModel(
            wikibase_name="EI Most Recent Test Wikibase",
            base_url="https://ei-most-recent-example.com",
            sparql_endpoint_url="https://ei-most-recent-example.com/sparql",
        )
        wikibase.checked = True
        wikibase.reuse = True
        wikibase.test = False
        wikibase.wikibase_type = None
        session.add(wikibase)
        await session.flush()
        await session.refresh(wikibase)
        wikibase_id = wikibase.id

    mocker.patch(
        "fetch_data.sparql_data.create_external_identifier_data_observation.get_sparql_results",
        side_effect=[
            {"results": {"bindings": [{"count": {"value": 16}}]}},
            {"results": {"bindings": [{"count": {"value": 32}}]}},
            {"results": {"bindings": [{"count": {"value": 64}}]}},
            {"results": {"bindings": [{"count": {"value": 128}}]}},
        ],
    )

    await test_schema.execute(
        FETCH_EXTERNAL_IDENTIFIER_MUTATION,
        variable_values={"wikibaseId": wikibase_id},
        context_value=get_mock_context("test-auth-token"),
    )

    async with get_async_session() as session:
        obs = await session.scalar(
            select(WikibaseExternalIdentifierObservationModel)
            .where(
                WikibaseExternalIdentifierObservationModel.wikibase_id == wikibase_id
            )
            .order_by(WikibaseExternalIdentifierObservationModel.id.desc())
        )
        obs_id = str(obs.id)

    return {"wikibase_id": wikibase_id, "obs_id": obs_id}


@pytest.mark.asyncio
@pytest.mark.query
@pytest.mark.ei
async def test_wikibase_external_identifier_most_recent_observation_query(
    wikibase_with_ei_observation,
):  # pylint: disable=redefined-outer-name
    """Test Wikibase Most Recent External Identifier Observation"""

    data = wikibase_with_ei_observation

    result = await test_schema.execute(
        WIKIBASE_EXTERNAL_IDENTIFIER_MOST_RECENT_OBSERVATION_QUERY,
        variable_values={"wikibaseId": data["wikibase_id"]},
    )

    assert result.errors is None
    assert result.data is not None
    assert "wikibase" in result.data
    result_wikibase = result.data["wikibase"]
    assert_property_value(result_wikibase, "id", str(data["wikibase_id"]))
    assert "externalIdentifierObservations" in result_wikibase
    assert "mostRecent" in result_wikibase["externalIdentifierObservations"]
    most_recent = result_wikibase["externalIdentifierObservations"]["mostRecent"]

    assert_external_identifier(most_recent, data["obs_id"], True, 16, 32, 64, 128)
