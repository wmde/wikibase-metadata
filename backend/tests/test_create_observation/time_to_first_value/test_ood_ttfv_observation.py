"""Test update_out_of_date_time_to_first_value_observations"""

import pytest
from data.database_connection import get_async_session
from model.database.wikibase_model import WikibaseModel
from fetch_data import update_out_of_date_time_to_first_value_observations
from tests.utils import MockResponse

@pytest.fixture
async def wikibase(db_session):
    """Create a wikibase with script path and no TTFV observations"""
    async with get_async_session() as session:
        wikibase = WikibaseModel(
            wikibase_name="TTFV OOD Test Wikibase",
            base_url="https://ttfv-ood-example.com",
            script_path="/w",
        )
        wikibase.checked = True
        wikibase.reuse = True
        wikibase.test = False
        wikibase.wikibase_type = None
        session.add(wikibase)
        await session.flush()

@pytest.mark.asyncio
@pytest.mark.soup
async def test_update_out_of_date_time_to_first_value_observations_fail(wikibase, mocker):
    """Test Error Returned Scenario"""

    mocker.patch(
        "fetch_data.utils.fetch_data_from_api.requests.get",
        side_effect=[MockResponse("", 404)],
    )
    result = await update_out_of_date_time_to_first_value_observations()
    assert result.failure == 1
    assert result.success == 0
    assert result.total == 1
