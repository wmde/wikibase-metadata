"""Test update_out_of_date_quantity_observations"""

import pytest
from fetch_data import update_out_of_date_quantity_observations


@pytest.mark.asyncio
@pytest.mark.dependency(
    name="quantity-success-ood",
    depends=["add-wikibase", "update-wikibase-url"],
    scope="session",
)
@pytest.mark.quantity
@pytest.mark.sparql
async def test_update_out_of_date_quantity_observations_success(mocker):
    """Test"""

    mocker.patch(
        "fetch_data.sparql_data.create_quantity_data_observation.get_sparql_results",
        side_effect=[],
    )
    result = await update_out_of_date_quantity_observations()
    assert result.failure == 1
    assert result.success == 0
    assert result.total == 1
