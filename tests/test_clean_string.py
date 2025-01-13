"""Test Clean String"""

import pytest

from fetch_data.utils import clean_string


@pytest.mark.version
def test_clean_string():
    """Test get_log_param_string"""

    assert clean_string("4.2.0  (2024-07-18)") == "4.2.0 (2024-07-18)"
