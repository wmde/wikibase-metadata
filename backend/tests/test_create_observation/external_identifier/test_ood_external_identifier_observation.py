"""Test update_out_of_date_external_identifier_observations"""

import pytest

from data import get_async_session
from fetch_data import update_out_of_date_external_identifier_observations
from model.database import WikibaseModel


@pytest.fixture
async def wikibase_with_sparql_ei_ood(db_session):
    """Create a wikibase with sparql endpoint for OOD EI tests"""
    async with get_async_session() as session:
        wikibase = WikibaseModel(
            wikibase_name="EI OOD Test Wikibase",
            base_url="https://ei-ood-example.com",
            sparql_endpoint_url="https://ei-ood-example.com/sparql",
        )
        wikibase.checked = True
        wikibase.reuse = True
        wikibase.test = False
        wikibase.wikibase_type = None
        session.add(wikibase)
        await session.flush()


@pytest.mark.asyncio
@pytest.mark.ei
@pytest.mark.sparql
async def test_update_out_of_date_external_identifier_observations_success(
    wikibase_with_sparql_ei_ood, mocker
):
    """Test"""

    mocker.patch(
        "fetch_data.sparql_data.create_external_identifier_data_observation.get_sparql_results",
        side_effect=[],
    )
    result = await update_out_of_date_external_identifier_observations()
    assert result.failure == 1
    assert result.success == 0
    assert result.total == 1
