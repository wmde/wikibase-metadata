"""Test create_property_popularity_observation"""

import asyncio
import time
from urllib.error import HTTPError
import pytest
from data.database_connection import get_async_session
from model.database.wikibase_model import WikibaseModel
from fetch_data import create_property_popularity_observation
from tests.test_schema import test_schema
from tests.utils import get_mock_context

FETCH_PROPERTY_POPULARITY_MUTATION = """mutation MyMutation($wikibaseId: Int!) {
  fetchPropertyPopularityData(wikibaseId: $wikibaseId)
}"""


@pytest.fixture
async def wikibase_with_sparql(db_session): # pylint: disable=unused-argument
    """Create a wikibase with sparql endpoint"""
    async with get_async_session() as session:
        wikibase = WikibaseModel(
            wikibase_name="Property Test Wikibase",
            base_url="https://property-test-example.com",
            sparql_endpoint_url="https://property-test-example.com/sparql",
        )
        wikibase.checked = True
        wikibase.reuse = True
        wikibase.test = False
        wikibase.wikibase_type = None
        session.add(wikibase)
        await session.flush()
        await session.refresh(wikibase)
        return wikibase


@pytest.mark.asyncio
@pytest.mark.property
@pytest.mark.sparql
async def test_create_property_popularity_observation_success(
    wikibase_with_sparql, mocker
):
    """Test One-Pull Per Month, Data Returned Scenario"""

    await asyncio.to_thread(time.sleep, 1)

    mocker.patch(
        "fetch_data.sparql_data.create_property_popularity_data_observation.get_sparql_results",
        side_effect=[
            {
                "results": {
                    "bindings": [
                        {"property": {"value": "P1"}, "propertyCount": {"value": 12}},
                        {"property": {"value": "P14"}, "propertyCount": {"value": 1}},
                    ]
                }
            }
        ],
    )

    result = await test_schema.execute(
        FETCH_PROPERTY_POPULARITY_MUTATION,
        variable_values={"wikibaseId": wikibase_with_sparql.id},
        context_value=get_mock_context("test-auth-token"),
    )

    assert result.errors is None
    assert result.data is not None
    assert result.data["fetchPropertyPopularityData"]


@pytest.mark.asyncio
@pytest.mark.property
@pytest.mark.sparql
async def test_create_property_popularity_observation_failure(
    wikibase_with_sparql, mocker
):
    """Test"""

    mocker.patch(
        "fetch_data.sparql_data.create_property_popularity_data_observation.get_sparql_results",
        side_effect=[
            HTTPError(
                url="https://query.example.com/sparql",
                code=500,
                msg="Error",
                hdrs="",
                fp=None,
            )
        ],
    )
    success = await create_property_popularity_observation(wikibase_with_sparql.id)
    assert success is False
