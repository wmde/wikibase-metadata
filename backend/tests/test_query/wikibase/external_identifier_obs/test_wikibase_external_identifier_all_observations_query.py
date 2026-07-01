"""Test Wikibase All External Identifier Observations"""

from datetime import datetime, timezone

import pytest

from data import get_async_session
from model.database import WikibaseExternalIdentifierObservationModel, WikibaseModel
from tests.test_query.wikibase.external_identifier_obs.assert_external_identifier import (
    assert_external_identifier,
)
from tests.test_query.wikibase.external_identifier_obs.external_identifier_fragment import (
    WIKIBASE_EXTERNAL_IDENTIFIER_OBSERVATION_FRAGMENT,
)
from tests.test_schema import test_schema
from tests.utils import assert_property_value

WIKIBASE_EXTERNAL_IDENTIFIER_ALL_OBSERVATIONS_QUERY = """
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

""" + WIKIBASE_EXTERNAL_IDENTIFIER_OBSERVATION_FRAGMENT


@pytest.fixture
async def wikibase_with_two_ei_observations(
    db_session,
):  # pylint: disable=unused-argument
    """Create a wikibase with two external identifier observations"""
    async with get_async_session() as session:
        wikibase = WikibaseModel(
            wikibase_name="EI All Observations Test Wikibase",
            base_url="https://ei-all-obs-example.com",
        )
        wikibase.checked = True
        wikibase.reuse = True
        wikibase.test = False
        wikibase.wikibase_type = None
        session.add(wikibase)
        await session.flush()
        await session.refresh(wikibase)

        obs1 = WikibaseExternalIdentifierObservationModel()
        obs1.wikibase_id = wikibase.id
        obs1.returned_data = True
        obs1.observation_date = datetime(2024, 3, 1, tzinfo=timezone.utc)
        obs1.total_external_identifier_properties = 16
        obs1.total_external_identifier_statements = 32
        obs1.total_url_properties = 64
        obs1.total_url_statements = 128
        session.add(obs1)
        await session.flush()
        await session.refresh(obs1)

        obs2 = WikibaseExternalIdentifierObservationModel()
        obs2.wikibase_id = wikibase.id
        obs2.returned_data = False
        obs2.observation_date = datetime(2024, 3, 2, tzinfo=timezone.utc)
        obs2.total_external_identifier_properties = 1
        obs2.total_external_identifier_statements = 2
        obs2.total_url_properties = None
        obs2.total_url_statements = None
        session.add(obs2)
        await session.flush()
        await session.refresh(obs2)

        wikibase_id = wikibase.id
        obs1_id = str(obs1.id)
        obs2_id = str(obs2.id)
    return wikibase_id, obs1_id, obs2_id


@pytest.mark.asyncio
@pytest.mark.query
@pytest.mark.ei
async def test_wikibase_external_identifier_all_observations_query(
    wikibase_with_two_ei_observations,
):  # pylint: disable=redefined-outer-name
    """Test Wikibase All External Identifier Observations"""

    wikibase_id, obs1_id, obs2_id = wikibase_with_two_ei_observations

    result = await test_schema.execute(
        WIKIBASE_EXTERNAL_IDENTIFIER_ALL_OBSERVATIONS_QUERY,
        variable_values={"wikibaseId": wikibase_id},
    )

    assert result.errors is None
    assert result.data is not None
    assert "wikibase" in result.data
    result_wikibase = result.data["wikibase"]
    assert_property_value(result_wikibase, "id", str(wikibase_id))
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
            (obs1_id, True, 16, 32, 64, 128),
            (obs2_id, False, 1, 2, None, None),
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
