"""Test update_out_of_date_software_observations"""

import pytest
from data.database_connection import get_async_session
from model.database.wikibase_model import WikibaseModel
from fetch_data import update_out_of_date_software_observations
from tests.utils import MockResponse

@pytest.fixture
async def wikibase(db_session):
    """Create a wikibase with article path and no software observations"""
    async with get_async_session() as session:
        wikibase = WikibaseModel(
            wikibase_name="Software OOD Test Wikibase",
            base_url="https://software-ood-example.com",
            article_path="/wiki",
        )
        wikibase.checked = True
        wikibase.reuse = True
        wikibase.test = False
        wikibase.wikibase_type = None
        session.add(wikibase)
        await session.flush()

@pytest.mark.asyncio
@pytest.mark.soup
@pytest.mark.version
async def test_update_out_of_date_software_observations_fail(wikibase, mocker):
    """Test Data Returned Scenario"""

    mocker.patch(
        "fetch_data.soup_data.software.create_software_version_data_observation.requests.get",
        side_effect=[MockResponse("", 404)],
    )
    result = await update_out_of_date_software_observations()
    assert result.failure == 1
    assert result.success == 0
    assert result.total == 1
