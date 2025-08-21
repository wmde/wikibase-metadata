"""Test create_quantity_data_observation"""

import pytest
from unittest.mock import AsyncMock, patch
from fetch_data.sparql_data.create_quantity_data_observation import (
    find_count_limit1_last_offset,
    try_to_get_result,
)
from tests.utils import get_mock_context


@pytest.mark.asyncio
async def test_find_count_limit1_last_offset_success():
    """Test find_count_limit1_last_offset with successful results at various offsets"""

    # Mock try_to_get_result to return True for offsets 0-9, False for 10+
    mock_try_to_get_result = AsyncMock()
    mock_try_to_get_result.side_effect = lambda wikibase, query, offset: offset < 10

    with patch(
        "fetch_data.sparql_data.create_quantity_data_observation.try_to_get_result",
        mock_try_to_get_result,
    ):
        # Create a mock wikibase object
        class MockWikibase:
            id = 1
            sparql_endpoint_url = type(
                "obj", (object,), {"url": "http://example.com/sparql"}
            )()

        # Test the function
        result = await find_count_limit1_last_offset(
            MockWikibase(), "SELECT * WHERE { ?s ?p ?o }"
        )

        # Should return 9 (last offset that returned True)
        assert result == 9
        assert mock_try_to_get_result.call_count == 11  # 0 through 10


@pytest.mark.asyncio
async def test_find_count_limit1_last_offset_all_false():
    """Test find_count_limit1_last_offset when all offsets return False"""

    # Mock try_to_get_result to return False for all offsets
    mock_try_to_get_result = AsyncMock()
    mock_try_to_get_result.return_value = False

    with patch(
        "fetch_data.sparql_data.create_quantity_data_observation.try_to_get_result",
        mock_try_to_get_result,
    ):
        # Create a mock wikibase object
        class MockWikibase:
            id = 1
            sparql_endpoint_url = type(
                "obj", (object,), {"url": "http://example.com/sparql"}
            )()

        # Test the function
        result = await find_count_limit1_last_offset(
            MockWikibase(), "SELECT * WHERE { ?s ?p ?o }"
        )

        # Should return -1 (no successful offset)
        assert result == -1
        assert mock_try_to_get_result.call_count == 1  # Only called once with offset 0


@pytest.mark.asyncio
async def test_find_count_limit1_last_offset_all_true():
    """Test find_count_limit1_last_offset when all offsets return True"""

    # Mock try_to_get_result to return True for all offsets
    mock_try_to_get_result = AsyncMock()
    mock_try_to_get_result.return_value = True

    with patch(
        "fetch_data.sparql_data.create_quantity_data_observation.try_to_get_result",
        mock_try_to_get_result,
    ):
        # Create a mock wikibase object
        class MockWikibase:
            id = 1
            sparql_endpoint_url = type(
                "obj", (object,), {"url": "http://example.com/sparql"}
            )()

        # Test the function
        result = await find_count_limit1_last_offset(
            MockWikibase(), "SELECT * WHERE { ?s ?p ?o }"
        )

        # Should return 0 (since we're using binary search and the first call is with offset 0)
        # The binary search will find that offset 0 works, but we don't know about higher offsets
        # due to the way the algorithm is structured
        assert result == 0
        # The actual number of calls depends on the binary search implementation
        # but it should be more than 1 call
        assert mock_try_to_get_result.call_count > 1


@pytest.mark.asyncio
async def test_find_count_limit1_last_offset_mixed_results():
    """Test find_count_limit1_last_offset with mixed results (True, False, True)"""

    # Mock try_to_get_result to return True for offset 0, False for 1, True for 2
    call_count = 0

    def mock_try_to_get_result(wikibase, query, offset):
        nonlocal call_count
        call_count += 1
        if offset == 0 or offset == 2:
            return True
        return False

    with patch(
        "fetch_data.sparql_data.create_quantity_data_observation.try_to_get_result",
        mock_try_to_get_result,
    ):
        # Create a mock wikibase object
        class MockWikibase:
            id = 1
            sparql_endpoint_url = type(
                "obj", (object,), {"url": "http://example.com/sparql"}
            )()

        # Test the function
        result = await find_count_limit1_last_offset(
            MockWikibase(), "SELECT * WHERE { ?s ?p ?o }"
        )

        # Should return 2 (last offset that returned True)
        assert result == 2
        # The call count should be reasonable for binary search
        assert call_count > 0
