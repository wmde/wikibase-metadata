"""Test get_multiple_user_data"""

import pytest
from fetch_data.api_data import get_multiple_user_data


@pytest.mark.asyncio
@pytest.mark.user
async def test_get_multiple_user_data_empty():
    """Test Empty Scenario"""

    assert await get_multiple_user_data(None, []) == []
