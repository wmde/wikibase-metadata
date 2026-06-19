"""Test update_out_of_date_user_observations"""

import pytest
from data.database_connection import get_async_session
from model.database.wikibase_model import WikibaseModel
from fetch_data import update_out_of_date_user_observations

@pytest.fixture
async def wikibase(db_session):  # pylint: disable=unused-argument
    """Create a test wikibase"""
    async with get_async_session() as session:
        wikibase = WikibaseModel(
            wikibase_name="Test Wikibase",
            base_url="https://example.com",
            script_path="/w"
        )
        wikibase.checked = True
        session.add(wikibase)
        await session.flush()
        return wikibase

@pytest.mark.asyncio
@pytest.mark.user
async def test_update_out_of_date_user_observations_empty(wikibase, mocker):
    """Test No-Data Scenario"""

    mocker.patch(
        "fetch_data.api_data.user_data.fetch_all_user_data.fetch_api_data",
        side_effect=[{"query": {"allusers": []}}],
    )
    result = await update_out_of_date_user_observations()
    assert result.failure == 0
    assert result.success == 1
    assert result.total == 1
