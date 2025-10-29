"""Test update_out_of_date_property_observations"""

import pytest
from fetch_data import update_out_of_date_property_observations


@pytest.mark.asyncio
@pytest.mark.dependency(
    name="property-popularity-success-ood",
    depends=["add-wikibase", "update-wikibase-url"],
    scope="session",
)
@pytest.mark.property
@pytest.mark.sparql
async def test_update_out_of_date_property_observations_success(mocker):
    """Test One-Pull Per Month, Data Returned Scenario"""

    mocker.patch(
        "fetch_data.sparql_data.create_property_popularity_data_observation.get_sparql_results",
        side_effect=[{"results": {"bindings": []}}],
    )
    result = await update_out_of_date_property_observations()
    assert result.failure == 0
    assert result.success == 1
    assert result.total == 1
