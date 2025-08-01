"""Test create_property_popularity_observation"""

import asyncio
import time
from urllib.error import HTTPError
import pytest
from fetch_data import create_property_popularity_observation
from tests.test_schema import test_schema
from tests.utils import get_mock_context


FETCH_PROPERTY_POPULARITY_MUTATION = """mutation MyMutation($wikibaseId: Int!) {
  fetchPropertyPopularityData(wikibaseId: $wikibaseId)
}"""


@pytest.mark.asyncio
@pytest.mark.dependency(
    name="property-popularity-success",
    depends=["property-popularity-success-ood"],
    scope="session",
)
@pytest.mark.mutation
@pytest.mark.property
@pytest.mark.sparql
async def test_create_property_popularity_observation_success(mocker):
    """Test One-Pull Per Month, Data Returned Scenario"""

    await asyncio.to_thread(time.sleep, 1)

    mocker.patch(
        "fetch_data.sparql_data.create_property_popularity_data_observation.get_sparql_results",
        side_effect=[
            {
                "results": {
                    "bindings": [
                        {"property": {"value": "P1"}, "propertyCount": {"value": 12}},
                        {"property": {"value": "P14"}, "propertyCount": {"value": 1}},
                    ]
                }
            }
        ],
    )

    result = await test_schema.execute(
        FETCH_PROPERTY_POPULARITY_MUTATION,
        variable_values={"wikibaseId": 1},
        context_value=get_mock_context("test-auth-token"),
    )

    assert result.errors is None
    assert result.data is not None
    assert result.data["fetchPropertyPopularityData"]


@pytest.mark.asyncio
@pytest.mark.dependency(
    name="property-popularity-failure",
    depends=["property-popularity-success"],
    scope="session",
)
@pytest.mark.property
@pytest.mark.sparql
async def test_create_property_popularity_observation_failure(mocker):
    """Test"""

    mocker.patch(
        "fetch_data.sparql_data.create_property_popularity_data_observation.get_sparql_results",
        side_effect=[
            HTTPError(
                url="https://query.example.com/sparql",
                code=500,
                msg="Error",
                hdrs="",
                fp=None,
            )
        ],
    )
    success = await create_property_popularity_observation(1)
    assert success is False
