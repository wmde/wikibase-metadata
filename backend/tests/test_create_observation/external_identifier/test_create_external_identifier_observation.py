"""Test create_external_identifier_observation"""

import time
from urllib.error import HTTPError
import pytest
from model.database.wikibase_model import WikibaseModel
from fetch_data import create_external_identifier_observation
from tests.test_schema import test_schema
from tests.utils import get_mock_context

FETCH_EXTERNAL_IDENTIFIER_MUTATION = """mutation MyMutation($wikibaseId: Int!) {
  fetchExternalIdentifierData(wikibaseId: $wikibaseId)
}"""


@pytest.fixture
async def wikibase_with_sparql(db_session):
    """Create a wikibase with sparql endpoint for observation tests"""
    from sqlalchemy.ext.asyncio import AsyncSession

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
        wikibase_id = wikibase.id
        await session.commit()
        return wikibase_id


@pytest.mark.asyncio
@pytest.mark.ei
@pytest.mark.sparql
async def test_create_external_identifier_observation_success(
    wikibase_with_sparql, mocker
):
    """Test"""

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
        variable_values={"wikibaseId": wikibase_with_sparql},
        context_value=get_mock_context("test-auth-token"),
    )

    assert result.errors is None
    assert result.data is not None
    assert result.data["fetchExternalIdentifierData"]


@pytest.mark.asyncio
@pytest.mark.ei
@pytest.mark.sparql
async def test_create_external_identifier_observation_failure(
    wikibase_with_sparql, mocker
):
    """Test"""

    time.sleep(1)

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
    success = await create_external_identifier_observation(wikibase_with_sparql)
    assert success is False
