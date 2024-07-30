"""Test create_quantity_observation"""

from urllib.error import HTTPError
import pytest
from fetch_data.sparql_data import create_quantity_observation


@pytest.mark.asyncio
@pytest.mark.quantity
@pytest.mark.sparql
async def test_create_quantity_observation_success(mocker):
    """Test"""

    mocker.patch(
        "fetch_data.sparql_data.create_quantity_data_observation.get_results",
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
@pytest.mark.quantity
@pytest.mark.sparql
async def test_create_quantity_observation_failure(mocker):
    """Test"""

    mocker.patch(
        "fetch_data.sparql_data.create_quantity_data_observation.get_results",
        side_effect=[
            {"results": {"bindings": [{"count": {"value": 1}}]}},  # Properties
            {"results": {"bindings": [{"count": {"value": 2}}]}},  # Items
            HTTPError(
                url="query.test.url/sparql", code=500, msg="Error", hdrs="", fp=None
            ),
        ],
    )
    success = await create_quantity_observation(1)
    assert success is False
