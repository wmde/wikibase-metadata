"""Test create_external_identifier_observation"""

import time
from urllib.error import HTTPError
import pytest
from fetch_data import create_external_identifier_observation
from tests.test_schema import test_schema
from tests.utils import get_mock_context

FETCH_EXTERNAL_IDENTIFIER_MUTATION = """mutation MyMutation($wikibaseId: Int!) {
  fetchExternalIdentifierData(wikibaseId: $wikibaseId)
}"""


@pytest.mark.asyncio
@pytest.mark.dependency(
    name="external-identifier-success",
    depends=["external-identifier-success-ood"],
    scope="session",
)
@pytest.mark.mutation
@pytest.mark.ei
@pytest.mark.sparql
async def test_create_external_identifier_observation_success(mocker):
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
        variable_values={"wikibaseId": 1},
        context_value=get_mock_context("test-auth-token"),
    )

    assert result.errors is None
    assert result.data is not None
    assert result.data["fetchExternalIdentifierData"]


@pytest.mark.asyncio
@pytest.mark.dependency(
    name="external-identifier-failure",
    depends=["external-identifier-success"],
    scope="session",
)
@pytest.mark.ei
@pytest.mark.sparql
async def test_create_external_identifier_observation_failure(mocker):
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
    success = await create_external_identifier_observation(1)
    assert success is False
