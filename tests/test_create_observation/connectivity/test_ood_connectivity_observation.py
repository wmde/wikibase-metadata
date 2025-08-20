"""Test update_out_of_date_connectivity_observations"""

import pytest
from fetch_data import update_out_of_date_connectivity_observations


@pytest.mark.asyncio
@pytest.mark.connectivity
@pytest.mark.dependency(
    name="connectivity-success-ood",
    depends=["add-wikibase", "update-wikibase-url"],
    scope="session",
)
@pytest.mark.sparql
async def test_update_out_of_date_connectivity_observations(mocker):
    """Test"""

    mocker.patch(
        "fetch_data.sparql_data.create_connectivity_data_observation.get_sparql_results",
        side_effect=[{"results": {"bindings": []}}],
    )
    await update_out_of_date_connectivity_observations()
