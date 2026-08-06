"""Test create_quantity_observation"""

import time
from urllib.error import HTTPError

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from data import get_async_session
from fetch_data import create_quantity_observation
from model.database import WikibaseModel, WikibaseQuantityObservationModel
from tests.test_schema import test_schema
from tests.utils import get_mock_context

FETCH_QUANTITY_MUTATION = """mutation MyMutation($wikibaseId: Int!) {
  fetchQuantityData(wikibaseId: $wikibaseId)
}"""


@pytest.fixture
async def wikibase_with_sparql_quantity(db_session):
    """Create a wikibase with sparql endpoint for quantity tests"""
    async with AsyncSession(bind=db_session) as session:
        wikibase = WikibaseModel(
            wikibase_name="Quantity Test Wikibase",
            base_url="https://quantity-test-example.com",
            sparql_endpoint_url="https://quantity-test-example.com/sparql",
            reuse=True,
            wikibase_type=None,
        )
        wikibase.checked = True
        session.add(wikibase)
        await session.flush()
        await session.refresh(wikibase)
    return wikibase


@pytest.mark.asyncio
@pytest.mark.mutation
@pytest.mark.quantity
@pytest.mark.sparql
async def test_create_quantity_observation_success(
    db_session, wikibase_with_sparql_quantity, mocker
):
    """Test"""

    async with AsyncSession(bind=db_session) as session:
        before = await session.scalar(
            select(WikibaseQuantityObservationModel).where(
                WikibaseQuantityObservationModel.wikibase_id
                == wikibase_with_sparql_quantity.id
            )
        )
        assert before is None

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
        variable_values={"wikibaseId": wikibase_with_sparql_quantity.id},
        context_value=get_mock_context("test-auth-token"),
    )

    assert result.errors is None
    assert result.data is not None
    assert result.data["fetchQuantityData"]

    async with AsyncSession(bind=db_session) as session:
        after = await session.scalar(
            select(WikibaseQuantityObservationModel).where(
                WikibaseQuantityObservationModel.wikibase_id
                == wikibase_with_sparql_quantity.id
            )
        )
        assert after.total_items == 2
        assert after.total_lexemes == 4
        assert after.total_properties == 1
        assert after.total_triples == 8


@pytest.mark.asyncio
@pytest.mark.quantity
@pytest.mark.sparql
async def test_create_quantity_observation_failure(
    db_session, wikibase_with_sparql_quantity, mocker
):
    """Test"""

    time.sleep(1)

    async with AsyncSession(bind=db_session) as session:
        before = await session.scalar(
            select(WikibaseQuantityObservationModel).where(
                WikibaseQuantityObservationModel.wikibase_id
                == wikibase_with_sparql_quantity.id
            )
        )
        assert before is None

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
    success = await create_quantity_observation(wikibase_with_sparql_quantity.id)
    assert success is False

    async with AsyncSession(bind=db_session) as session:
        after = await session.scalar(
            select(WikibaseQuantityObservationModel).where(
                WikibaseQuantityObservationModel.wikibase_id
                == wikibase_with_sparql_quantity.id
            )
        )
        assert after.returned_data == False
