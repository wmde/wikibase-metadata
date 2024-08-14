"""Test parse_datetime"""

from datetime import datetime
from typing import Optional
import pytest
from fetch_data.utils import parse_datetime


@pytest.mark.parametrize(
    ["date_string", "expected_datetime"],
    [
        (None, None),
        ("12:03 4 okt 2020", datetime(2020, 10, 4, 12, 3)),
        ("6 lug 2021 16:09", datetime(2021, 7, 6, 16, 9)),
        ("9 ene 2027 4:14", datetime(2027, 1, 9, 4, 14)),
        ("2021년 7월 21일 (수) 02:53", datetime(2021, 7, 21, 2, 53)),
        ("– (62dadc3) 2021년 7월 21일 (수) 02:53", None),
    ],
)
def test_parse_datetime_none(
    date_string: Optional[str], expected_datetime: Optional[datetime]
):
    """Test Null Scenario"""

    assert parse_datetime(date_string) == expected_datetime
