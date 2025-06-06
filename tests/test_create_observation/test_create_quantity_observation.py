"""Test create_quantity_observation"""

import time
from urllib.error import HTTPError
import pytest
from fetch_data import create_quantity_observation


@pytest.mark.asyncio
@pytest.mark.dependency(
    name="quantity-success", depends=["quantity-success-ood"], scope="session"
)
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
        ],
    )
    success = await create_quantity_observation(1)
    assert success


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
