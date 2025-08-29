# pylint: disable=missing-function-docstring

"""Test create_quantity_observation"""

import pytest

import time

import urllib
from SPARQLWrapper.SPARQLExceptions import EndPointInternalError
from fetch_data.sparql_data.pull_wikidata import SPARQLResponseMalformed

from fetch_data import create_quantity_observation
from tests.test_schema import test_schema
from tests.utils import get_mock_context

FETCH_QUANTITY_MUTATION = """mutation MyMutation($wikibaseId: Int!) {
  fetchQuantityData(wikibaseId: $wikibaseId)
}"""


def sparql_result_count(c):
    return {"results": {"bindings": [{"count": {"value": c}}]}}


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
            sparql_result_count(1),  # Properties
            sparql_result_count(2),  # Items
            sparql_result_count(4),  # Lexemes
            sparql_result_count(8),  # Triples
            sparql_result_count(16),  # External Identifier Properties
            sparql_result_count(32),  # External Identifier Statements
            sparql_result_count(64),  # URL Properties
            sparql_result_count(128),  # URL Statements
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
    name="quantity-total-failure",
    depends=["quantity-success", "quantity-success-ood"],
    scope="session",
)
@pytest.mark.quantity
@pytest.mark.sparql
async def test_create_quantity_observation_total_failure(mocker):
    """Test"""

    time.sleep(1)

    mocker.patch(
        "fetch_data.sparql_data.create_quantity_data_observation.get_sparql_results",
        side_effect=[
            urllib.error.HTTPError(
                url="https://query.example.com/sparql",
                code=404,
                msg="Error",
                hdrs="",
                fp=None,
            ),  # fatal: endpoint not found
        ],
    )
    success = await create_quantity_observation(1)
    assert success is False


@pytest.mark.asyncio
@pytest.mark.dependency(
    name="quantity-partial-failure",
    depends=["quantity-success", "quantity-total-failure", "quantity-success-ood"],
    scope="session",
)
@pytest.mark.quantity
@pytest.mark.sparql
async def test_create_quantity_observation_partial_failure(mocker):
    """Test"""

    time.sleep(1)

    mocker.patch(
        "fetch_data.sparql_data.create_quantity_data_observation.get_sparql_results",
        side_effect=[
            sparql_result_count(1),  # Properties
            sparql_result_count(2),  # Items
            sparql_result_count(4),  # Lexemes
            sparql_result_count(8),  # Triples
            sparql_result_count(16),  # External Identifier Properties
            EndPointInternalError(
                response="Query timed out",
            ),  # External Identifier Statements - non fatal error
            SPARQLResponseMalformed(),  # URL Properties - non fatal error
            sparql_result_count(128),  # URL Property Statements
        ],
    )
    success = await create_quantity_observation(1)
    assert success is True  # partially obtained observations return True too
