"""Test fetch namespace data"""

import re

import pytest

from fetch_data.api_data.time_to_first_value.get_item_namespace import (
    get_item_namespace,
)
from tests.test_create_observation.time_to_first_value.test_create_ttfv_observation import (
    DATA_DIRECTORY,
)
from tests.utils import MockResponse

NAMESPACE_API_URL = re.compile(
    r"https://example\.com/w/api\.php\?action=query&meta=siteinfo&siprop=namespaces&format=json"
)


@pytest.mark.asyncio
async def test_get_item_namespace_full_data(wikibase_fixture, mocker):
    """Test item namespace returns full data"""

    def mock_get(*args, **kwargs):
        assert kwargs.get("timeout") == 300
        query = args[0]
        if (NAMESPACE_API_URL.match(query)) is not None:
            with open(f"{DATA_DIRECTORY}/namespace/success.json", mode="rb") as data:
                return MockResponse(query, 200, data.read())

        raise NotImplementedError(query)

    mocker.patch(
        "fetch_data.utils.fetch_data_from_api.requests.get", side_effect=mock_get
    )

    result = await get_item_namespace(api_url=wikibase_fixture.action_api_url())
    assert result == "120"


@pytest.mark.asyncio
async def test_get_item_namespace_no_data(wikibase_fixture, mocker):
    """Test item namespace returns no data"""

    def mock_get(*args, **kwargs):
        assert kwargs.get("timeout") == 300
        query = args[0]
        if (NAMESPACE_API_URL.match(query)) is not None:
            with open(f"{DATA_DIRECTORY}/namespace/failure.json", mode="rb") as data:
                return MockResponse(query, 200, data.read())

        raise NotImplementedError(query)

    mocker.patch(
        "fetch_data.utils.fetch_data_from_api.requests.get", side_effect=mock_get
    )

    with pytest.raises(ValueError) as excinfo:
        await get_item_namespace(api_url=wikibase_fixture.action_api_url())
    assert "No Item Namespace Found" == str(excinfo.value)
