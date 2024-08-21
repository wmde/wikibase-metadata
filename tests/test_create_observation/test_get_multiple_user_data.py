"""Test get_multiple_user_data"""

import pytest
from fetch_data.api_data import get_multiple_user_data


@pytest.mark.user
def test_get_multiple_user_data_empty():
    """Test Empty Scenario"""

    assert get_multiple_user_data(None, []) == []
