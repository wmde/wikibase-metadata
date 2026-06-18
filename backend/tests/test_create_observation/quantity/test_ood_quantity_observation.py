"""Test update_out_of_date_quantity_observations"""

import pytest
from data.database_connection import get_async_session
from model.database.wikibase_model import WikibaseModel
from fetch_data import update_out_of_date_quantity_observations

@pytest.fixture
async def wikibase(db_session):
    """Create a wikibase with sparql endpoint and no quantity observations"""
    async with get_async_session() as session:
        wikibase = WikibaseModel(
            wikibase_name="Quantity OOD Test Wikibase",
            base_url="https://quantity-ood-example.com",
            sparql_endpoint_url="https://quantity-ood-example.com/sparql",
        )
        wikibase.checked = True
        wikibase.reuse = True
        wikibase.test = False
        wikibase.wikibase_type = None
        session.add(wikibase)
        await session.flush()
        await session.refresh(wikibase)

@pytest.mark.asyncio
@pytest.mark.quantity
@pytest.mark.sparql
async def test_update_out_of_date_quantity_observations_success(wikibase, mocker):
    """Test"""

    mocker.patch(
        "fetch_data.sparql_data.create_quantity_data_observation.get_sparql_results",
        side_effect=[],
    )
    result = await update_out_of_date_quantity_observations()
    assert result.failure == 1
    assert result.success == 0
    assert result.total == 1
