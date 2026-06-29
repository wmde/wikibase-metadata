"""Test update_out_of_date_connectivity_observations"""

import pytest

from fetch_data import update_out_of_date_connectivity_observations
from model.database import WikibaseModel


@pytest.fixture
async def wikibase_out_of_date_connectivity(db_session):
    """Create 1 wikibase with no connectivity observations (out of date)"""
    from sqlalchemy.ext.asyncio import AsyncSession

    async with AsyncSession(bind=db_session) as session:
        wikibase = WikibaseModel(
            wikibase_name="Out of Date Connectivity Wikibase",
            base_url="https://out-of-date-connectivity-example.com",
            sparql_endpoint_url="https://out-of-date-connectivity-example.com/sparql",
        )
        wikibase.checked = True
        wikibase.reuse = True
        wikibase.test = False
        wikibase.wikibase_type = None
        session.add(wikibase)
        await session.flush()


@pytest.mark.asyncio
@pytest.mark.connectivity
@pytest.mark.sparql
async def test_update_out_of_date_connectivity_observations(
    wikibase_out_of_date_connectivity, mocker
):  # pylint: disable=redefined-outer-name, unused-argument
    """Test"""

    mocker.patch(
        "fetch_data.sparql_data.create_connectivity_data_observation.get_sparql_results",
        side_effect=[{"results": {"bindings": []}}],
    )
    result = await update_out_of_date_connectivity_observations()
    assert result.failure == 0
    assert result.success == 1
    assert result.total == 1
