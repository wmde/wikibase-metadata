"""Test fetch total page count"""

from datetime import datetime, timezone

import pytest

from fetch_data.api_data.api_quantity.fetch_total_page_count import (
    fetch_total_page_count,
)
from tests.test_create_observation.api_quantity.test_create_api_quantity_observation import (
    ALL_PAGES_API_URL,
    DATA_DIRECTORY,
)
from tests.utils import MockResponse


@pytest.mark.asyncio
async def test_fetch_total_page_count_two_pages(wikibase_with_script_path, mocker):
    """Test fetch total page count returns two pages of data"""

    def mock_get(*args, **kwargs):
        assert kwargs.get("timeout") == 300
        query = args[0]
        if (all_pages_match := ALL_PAGES_API_URL.match(query)) is not None:
            assert all_pages_match.group(1) == "120"
            if all_pages_match.group(2) == "":
                with open(f"{DATA_DIRECTORY}/allpages/page_1.json", mode="rb") as data:
                    return MockResponse(query, 200, data.read())
            else:
                with open(f"{DATA_DIRECTORY}/allpages/page_2.json", mode="rb") as data:
                    return MockResponse(query, 200, data.read())

        raise NotImplementedError(query)

    mocker.patch(
        "fetch_data.utils.fetch_data_from_api.requests.get", side_effect=mock_get
    )

    results = await fetch_total_page_count(
        api_url=wikibase_with_script_path.action_api_url(), namespace_id=120
    )
    assert results == 13
