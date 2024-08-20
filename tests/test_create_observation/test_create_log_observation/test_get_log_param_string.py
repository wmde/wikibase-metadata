"""Test get_log_param_string"""

import pytest
from fetch_data.api_data.log_data.fetch_log_data import get_log_param_string


@pytest.mark.log
def test_get_log_param_string():
    """Test get_log_param_string"""

    assert (
        get_log_param_string()
        == "?action=query&format=json&list=logevents&formatversion=2&ledir=older"
    )
    assert (
        get_log_param_string(limit=100)
        == "?action=query&format=json&list=logevents&formatversion=2&ledir=older&lelimit=100"
    )
    assert (
        get_log_param_string(oldest=True)
        == "?action=query&format=json&list=logevents&formatversion=2&ledir=newer"
    )
    assert (
        get_log_param_string(offset="20200101000000|1")
        == "?action=query&format=json&list=logevents&formatversion=2&ledir=older&lecontinue=20200101000000|1"  # pylint: disable=line-too-long
    )
