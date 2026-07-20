"""Test create_external_identifier_observation"""

import time
from urllib.error import HTTPError

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from data.database_connection import get_async_session
from fetch_data import create_external_identifier_observation
from model.database import WikibaseModel
from model.database.wikibase_observation.external_identifier.wikibase_ei_obs_model import (
    WikibaseExternalIdentifierObservationModel,
)
from tests.test_schema import test_schema
from tests.utils import get_mock_context

FETCH_EXTERNAL_IDENTIFIER_MUTATION = """mutation MyMutation($wikibaseId: Int!) {
  fetchExternalIdentifierData(wikibaseId: $wikibaseId)
}"""


@pytest.fixture
async def wikibase_with_sparql(db_session):
    """Create a wikibase with sparql endpoint for observation tests"""

    async with AsyncSession(bind=db_session) as session:
        wikibase = WikibaseModel(
            wikibase_name="EI Test Wikibase",
            base_url="https://example.com",
            sparql_endpoint_url="https://query.example.com/sparql",
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
@pytest.mark.ei
@pytest.mark.sparql
async def test_create_external_identifier_observation_success(
    wikibase_with_sparql, mocker
):
    """Test"""

    async with get_async_session() as session:
        before = await session.scalar(
            select(WikibaseExternalIdentifierObservationModel).where(
                WikibaseExternalIdentifierObservationModel.wikibase_id
                == wikibase_with_sparql.id
            )
        )
        assert before is None

    mocker.patch(
        "fetch_data.sparql_data.create_external_identifier_data_observation.get_sparql_results",
        side_effect=[
            {
                "results": {"bindings": [{"count": {"value": 16}}]}
            },  # External Identifier Properties
            {
                "results": {"bindings": [{"count": {"value": 32}}]}
            },  # External Identifier Statements
            {"results": {"bindings": [{"count": {"value": 64}}]}},  # URL Properties
            {"results": {"bindings": [{"count": {"value": 128}}]}},  # URL Statements
        ],
    )

    result = await test_schema.execute(
        FETCH_EXTERNAL_IDENTIFIER_MUTATION,
        variable_values={"wikibaseId": wikibase_with_sparql.id},
        context_value=get_mock_context("test-auth-token"),
    )

    assert result.errors is None
    assert result.data is not None
    assert result.data["fetchExternalIdentifierData"]

    async with get_async_session() as session:
        after = await session.scalar(
            select(WikibaseExternalIdentifierObservationModel).where(
                WikibaseExternalIdentifierObservationModel.wikibase_id
                == wikibase_with_sparql.id
            )
        )
        assert after.total_external_identifier_properties == 16
        assert after.total_external_identifier_statements == 32
        assert after.total_url_properties == 64
        assert after.total_url_statements == 128


@pytest.mark.asyncio
@pytest.mark.ei
@pytest.mark.sparql
async def test_create_external_identifier_observation_failure(
    wikibase_with_sparql, mocker
):
    """Test"""

    async with get_async_session() as session:
        before = await session.scalar(
            select(WikibaseExternalIdentifierObservationModel).where(
                WikibaseExternalIdentifierObservationModel.wikibase_id
                == wikibase_with_sparql.id
            )
        )
        assert before is None

    mocker.patch(
        "fetch_data.sparql_data.create_external_identifier_data_observation.get_sparql_results",
        side_effect=[
            {"results": {"bindings": [{"count": {"value": 1}}]}},  # EI Props
            {"results": {"bindings": [{"count": {"value": 2}}]}},  # EI Statements
            HTTPError(
                url="https://query.example.com/sparql",
                code=500,
                msg="Error",
                hdrs="",
                fp=None,
            ),
        ],
    )
    success = await create_external_identifier_observation(wikibase_with_sparql.id)
    assert success is False

    async with get_async_session() as session:
        after = await session.scalar(
            select(WikibaseExternalIdentifierObservationModel).where(
                WikibaseExternalIdentifierObservationModel.wikibase_id
                == wikibase_with_sparql.id
            )
        )
        assert after.returned_data == False
