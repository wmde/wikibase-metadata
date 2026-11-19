"""Test fetch creation data"""

from datetime import datetime
import re

import pytest

from fetch_data.api_data.time_to_first_value.get_creation_data import (
    get_all_creation_logs,
)
from tests.test_create_observation.time_to_first_value.test_create_ttfv_observation import (
    DATA_DIRECTORY,
)
from tests.utils import MockResponse

CREATION_LOG_API_URL = re.compile(
    # pylint: disable-next=line-too-long
    r"https://example\.com/w/api\.php\?action=query&format=json&list=logevents&letype=create&ledir=newer&lelimit=max&leprop=ids\|title\|timestamp&letitle=Item:(Q\d+)"
)


@pytest.mark.asyncio
async def test_get_creation_data_full_data(wikibase_fixture, mocker):
    """Test creation data returns full data"""

    def mock_get(*args, **kwargs):
        assert kwargs.get("timeout") == 300
        query = args[0]
        if (creation_log_match := CREATION_LOG_API_URL.match(query)) is not None:
            try:
                with open(
                    f"{DATA_DIRECTORY}/creation/{creation_log_match.group(1)}.json",
                    mode="rb",
                ) as data:
                    return MockResponse(query, 200, data.read())
            except FileNotFoundError:
                with open(f"{DATA_DIRECTORY}/creation/empty.json", mode="rb") as data:
                    return MockResponse(query, 200, data.read())

        raise NotImplementedError(query)

    mocker.patch(
        "fetch_data.utils.fetch_data_from_api.requests.get", side_effect=mock_get
    )

    api_url = wikibase_fixture.action_api_url()

    results = await get_all_creation_logs(api_url=api_url)

    assert len(results) == 3

    assert results[0].id == 250
    assert results[0].title == "Item:Q50"
    assert results[0].log_date == datetime(2026, 11, 19, 0, 0, 50)

    assert results[1].id == 5
    assert results[1].title == "Item:Q1"
    assert results[1].log_date == datetime(2026, 11, 19, 0, 0, 0)

    assert results[2].id == 50
    assert results[2].title == "Item:Q10"
    assert results[2].log_date == datetime(2026, 11, 19, 0, 0, 10)


@pytest.mark.asyncio
async def test_get_creation_data_no_data(wikibase_fixture, mocker):
    """Test creation data returns no data"""

    def mock_get(*args, **kwargs):
        assert kwargs.get("timeout") == 300
        query = args[0]
        if (CREATION_LOG_API_URL.match(query)) is not None:
            with open(f"{DATA_DIRECTORY}/creation/empty.json", mode="rb") as data:
                return MockResponse(query, 200, data.read())

        raise NotImplementedError(query)

    mocker.patch(
        "fetch_data.utils.fetch_data_from_api.requests.get", side_effect=mock_get
    )

    api_url = wikibase_fixture.action_api_url()

    results = await get_all_creation_logs(api_url=api_url)

    assert len(results) == 0
