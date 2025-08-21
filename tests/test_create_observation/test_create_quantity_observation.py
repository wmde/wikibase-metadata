"""Test create_quantity_observation"""

import time
from unittest.mock import AsyncMock, patch
from urllib.error import HTTPError

import pytest

from fetch_data import create_quantity_observation
from fetch_data.sparql_data.create_quantity_data_observation import (
    find_count_limit1_last_offset,
)
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


@pytest.mark.asyncio
async def test_find_count_limit1_last_offset_success():
    """Test find_count_limit1_last_offset with successful results at various offsets"""

    # The offset values that are the last ones yielding a result we want to find
    target_values = [
        0,
        1,
        5,
        7,
        8,
        9,
        10,
        15,
        20,
        10_001,
        200_301,
        10_000_000,
        99_999_999,
    ]
    # define the amounts we expect the try_to_get_result function to be called
    call_counts = [3, 6, 5, 6, 5, 6, 10, 10, 10, 22, 27, 36, 36]

    for target_value, call_count in zip(target_values, call_counts):
        with patch(
            "fetch_data.sparql_data.create_quantity_data_observation.try_to_get_result",
            new_callable=AsyncMock,
        ) as mock:
            # Mock the function to return True only when offset < target_value
            # pylint: disable-next=cell-var-from-loop
            mock.side_effect = lambda wikibase, query, offset: offset <= target_value

            # Create a mock wikibase object
            class MockWikibase:
                "A Wikibase that is just an illusion....... Happy now, pylint? -.-"
                id = 1
                sparql_endpoint_url = type(
                    "obj", (object,), {"url": "http://example.com/sparql"}
                )()

            # Test the function
            result = await find_count_limit1_last_offset(
                MockWikibase(), "SELECT * WHERE { ?s ?p ?o }"
            )

            assert result == target_value
            assert mock.call_count == call_count
