"""Test create_quantity_observation"""

import time
from urllib.error import HTTPError
import pytest
from fetch_data import create_quantity_observation
from tests.test_schema import test_schema
from tests.utils import get_mock_context

FETCH_QUANTITY_MUTATION = """mutation MyMutation($wikibaseId: Int!) {
  fetchQuantityData(wikibaseId: $wikibaseId)
}"""


@pytest.mark.asyncio
@pytest.mark.dependency(
    name="quantity-success", depends=["quantity-success-ood"], scope="session"
)
@pytest.mark.mutation
@pytest.mark.quantity
@pytest.mark.sparql
async def test_create_quantity_observation_success(mocker):
    """Test"""

    mocker.patch(
        "fetch_data.sparql_data.create_quantity_data_observation.get_sparql_results",
        side_effect=[
            {"results": {"bindings": [{"count": {"value": 1}}]}},  # Properties
            {"results": {"bindings": [{"count": {"value": 2}}]}},  # Items
            {"results": {"bindings": [{"count": {"value": 4}}]}},  # Lexemes
            {"results": {"bindings": [{"count": {"value": 8}}]}},  # Triples
            {"results": {"bindings": [{"count": {"value": 8}}]}},  # External Identifier Properties
            {"results": {"bindings": [{"count": {"value": 8}}]}},  # External Identifier Statements
            {"results": {"bindings": [{"count": {"value": 8}}]}},  # URL Properties
            {"results": {"bindings": [{"count": {"value": 8}}]}},  # URL Statements
        ],
    )

    result = await test_schema.execute(
        FETCH_QUANTITY_MUTATION,
        variable_values={"wikibaseId": 1},
        context_value=get_mock_context("test-auth-token"),
    )

    assert result.errors is None
    assert result.data is not None
    assert result.data["fetchQuantityData"]


@pytest.mark.asyncio
@pytest.mark.dependency(
    name="quantity-failure", depends=["quantity-success"], scope="session"
)
@pytest.mark.quantity
@pytest.mark.sparql
async def test_create_quantity_observation_failure(mocker):
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
    success = await create_quantity_observation(1)
    assert success is False
