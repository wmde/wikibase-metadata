"""Test fetch revision data"""

from datetime import datetime, timezone

import pytest

from fetch_data.api_data.time_to_first_value.get_revisions_data import (
    get_all_revision_logs,
)
from tests.test_create_observation.time_to_first_value.test_create_ttfv_observation import (
    ALL_REVISION_API_URL,
    DATA_DIRECTORY,
)
from tests.utils import MockResponse


@pytest.mark.asyncio
async def test_get_revisions_data_full_data(wikibase_with_script_path, mocker):
    """Test revisions data returns full data"""

    def mock_get(*args, **kwargs):
        assert kwargs.get("timeout") == 300
        query = args[0]
        if (all_revision_match := ALL_REVISION_API_URL.match(query)) is not None:
            assert all_revision_match.group(1) == "120"
            if all_revision_match.group(2) == "":
                with open(f"{DATA_DIRECTORY}/revision/page_1.json", mode="rb") as data:
                    return MockResponse(query, 200, data.read())
            else:
                with open(f"{DATA_DIRECTORY}/revision/page_2.json", mode="rb") as data:
                    return MockResponse(query, 200, data.read())

        raise NotImplementedError(query)

    mocker.patch(
        "fetch_data.utils.fetch_data_from_api.requests.get", side_effect=mock_get
    )

    results = await get_all_revision_logs(
        api_url=wikibase_with_script_path.action_api_url(), namespace_id=120
    )
    assert len(results) == 13

    assert results[0].id == 5
    assert results[0].title == "Item:Q1"
    assert results[0].log_date == datetime(2026, 11, 19, 0, 0, 1, tzinfo=timezone.utc)
