from datetime import datetime, timedelta
from typing import Optional

from freezegun import freeze_time
from fetch_data.log_data.fetch_log_data import get_log_list_from_url
from fetch_data.log_data.wikibase_log_record import WikibaseLogRecord


def assert_log_record(
    log: WikibaseLogRecord,
    expected_id: int,
    expected_log_date: datetime,
    expected_age: int,
    expected_user: Optional[str],
    expected_log_type_name: str,
):
    assert log.id == expected_id
    assert log.log_date == expected_log_date
    assert log.age() == expected_age
    assert log.log_type.name == expected_log_type_name
    assert log.user == expected_user
