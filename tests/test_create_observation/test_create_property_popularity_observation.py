"""Test create_property_popularity_observation"""

from urllib.error import HTTPError
import pytest
from fetch_data import create_property_popularity_observation


@pytest.mark.asyncio
@pytest.mark.property
@pytest.mark.sparql
async def test_create_property_popularity_observation_success(mocker):
    """Test One-Pull Per Month, Data Returned Scenario"""

    mocker.patch(
        "fetch_data.sparql_data.create_property_popularity_data_observation.get_results",
        side_effect=[
            {
                "results": {
                    "bindings": [
                        {"property": {"value": "P1"}, "propertyCount": {"value": 12}}
                    ]
                }
            }
        ],
    )
    success = await create_property_popularity_observation(1)
    assert success


@pytest.mark.asyncio
@pytest.mark.property
@pytest.mark.sparql
async def test_create_property_popularity_observation_failure(mocker):
    """Test"""

    mocker.patch(
        "fetch_data.sparql_data.create_property_popularity_data_observation.get_results",
        side_effect=[
            HTTPError(
                url="query.test.url/sparql", code=500, msg="Error", hdrs="", fp=None
            ),
        ],
    )
    success = await create_property_popularity_observation(1)
    assert success is False