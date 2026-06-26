"""Test create_quantity_observation"""

import time
from urllib.error import HTTPError
import pytest
from data.database_connection import get_async_session
from model.database.wikibase_model import WikibaseModel
from fetch_data import create_quantity_observation
from tests.test_schema import test_schema
from tests.utils import get_mock_context

FETCH_QUANTITY_MUTATION = """mutation MyMutation($wikibaseId: Int!) {
  fetchQuantityData(wikibaseId: $wikibaseId)
}"""


@pytest.fixture
async def wikibase_with_sparql_quantity(db_session):  # pylint: disable=unused-argument
    """Create a wikibase with sparql endpoint for quantity tests"""
    async with get_async_session() as session:
        wikibase = WikibaseModel(
            wikibase_name="Quantity Test Wikibase",
            base_url="https://quantity-test-example.com",
            sparql_endpoint_url="https://quantity-test-example.com/sparql",
        )
        wikibase.checked = True
        wikibase.reuse = True
        wikibase.test = False
        wikibase.wikibase_type = None
        session.add(wikibase)
        await session.flush()
        await session.refresh(wikibase)
        wikibase_id = wikibase.id
    return wikibase_id


@pytest.mark.asyncio
@pytest.mark.mutation
@pytest.mark.quantity
@pytest.mark.sparql
async def test_create_quantity_observation_success(
    wikibase_with_sparql_quantity, mocker
):
    """Test"""

    mocker.patch(
        "fetch_data.sparql_data.create_quantity_data_observation.get_sparql_results",
        side_effect=[
            {"results": {"bindings": [{"count": {"value": 1}}]}},  # Properties
            {"results": {"bindings": [{"count": {"value": 2}}]}},  # Items
            {"results": {"bindings": [{"count": {"value": 4}}]}},  # Lexemes
            {"results": {"bindings": [{"count": {"value": 8}}]}},  # Triples
        ],
    )

    result = await test_schema.execute(
        FETCH_QUANTITY_MUTATION,
        variable_values={"wikibaseId": wikibase_with_sparql_quantity},
        context_value=get_mock_context("test-auth-token"),
    )

    assert result.errors is None
    assert result.data is not None
    assert result.data["fetchQuantityData"]


@pytest.mark.asyncio
@pytest.mark.quantity
@pytest.mark.sparql
async def test_create_quantity_observation_failure(
    wikibase_with_sparql_quantity, mocker
):
    """Test"""

    time.sleep(1)

    mocker.patch(
        "fetch_data.sparql_data.create_quantity_data_observation.get_sparql_results",
        side_effect=[
            {"results": {"bindings": [{"count": {"value": 1}}]}},  # Properties
            {"results": {"bindings": [{"count": {"value": 2}}]}},  # Items
            HTTPError(
                url="https://query.example.com/sparql",
                code=500,
                msg="Error",
                hdrs="",
                fp=None,
            ),
        ],
    )
    success = await create_quantity_observation(wikibase_with_sparql_quantity)
    assert success is False
