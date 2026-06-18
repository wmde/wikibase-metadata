"""Test update_out_of_date_property_observations"""

import pytest
from data.database_connection import get_async_session
from model.database.wikibase_model import WikibaseModel
from fetch_data import update_out_of_date_property_observations

@pytest.fixture
async def wikibase(db_session):
    """Create a wikibase with sparql endpoint and no property observations"""
    async with get_async_session() as session:
        wikibase = WikibaseModel(
            wikibase_name="Property OOD Test Wikibase",
            base_url="https://property-ood-example.com",
            sparql_endpoint_url="https://property-ood-example.com/sparql",
        )
        wikibase.checked = True
        wikibase.reuse = True
        wikibase.test = False
        wikibase.wikibase_type = None
        session.add(wikibase)
        await session.flush()
        await session.refresh(wikibase)

@pytest.mark.asyncio
@pytest.mark.property
@pytest.mark.sparql
async def test_update_out_of_date_property_observations_success(wikibase, mocker):
    """Test One-Pull Per Month, Data Returned Scenario"""

    mocker.patch(
        "fetch_data.sparql_data.create_property_popularity_data_observation.get_sparql_results",
        side_effect=[{"results": {"bindings": []}}],
    )
    result = await update_out_of_date_property_observations()
    assert result.failure == 0
    assert result.success == 1
    assert result.total == 1
