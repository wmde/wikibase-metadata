"""Assert WikibaseLogRecord Matches Expectations"""

from datetime import datetime
from typing import Optional

from fetch_data.api_data.log_data import WikibaseLogRecord


# pylint: disable=too-many-arguments
def assert_log_record(
    log: WikibaseLogRecord,
    expected_id: int,
    expected_log_date: datetime,
    expected_age: int,
    expected_user: Optional[str],
    expected_log_type_name: str,
):
    """Assert WikibaseLogRecord Matches Expectations"""

    assert log.id == expected_id
    assert log.log_date == expected_log_date
    assert log.age() == expected_age
    assert log.log_type.name == expected_log_type_name
    assert log.user == expected_user
