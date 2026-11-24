"""Test fetch oldest log"""

from datetime import datetime, timezone

import pytest

from fetch_data.api_data.time_to_first_value.get_oldest_log import get_oldest_log_date
from tests.test_create_observation.time_to_first_value.test_create_ttfv_observation import (
    DATA_DIRECTORY,
    OLDEST_LOG_API_URL,
)
from tests.utils import MockResponse


@pytest.mark.asyncio
async def test_get_oldest_log_full_data(wikibase_with_script_path, mocker):
    """Test oldest log returns full data"""

    def mock_get(*args, **kwargs):
        assert kwargs.get("timeout") == 300
        query = args[0]
        if (OLDEST_LOG_API_URL.match(query)) is not None:
            with open(f"{DATA_DIRECTORY}/oldest_log/success.json", mode="rb") as data:
                return MockResponse(query, 200, data.read())

        raise NotImplementedError(query)

    mocker.patch(
        "fetch_data.utils.fetch_data_from_api.requests.get", side_effect=mock_get
    )

    result = await get_oldest_log_date(
        api_url=wikibase_with_script_path.action_api_url()
    )
    assert result == datetime(2026, 11, 19, 0, 0, 0, tzinfo=timezone.utc)
