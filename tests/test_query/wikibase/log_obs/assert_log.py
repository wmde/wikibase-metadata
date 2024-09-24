"""Assert Log Records"""

from datetime import datetime
from typing import Optional
from tests.utils import (
    assert_layered_property_count,
    assert_property_value,
    DATETIME_FORMAT,
)


# pylint: disable=too-many-arguments,too-many-positional-arguments
def assert_month_record(
    month_record: dict,
    expected_id: str,
    expected_first_log_date: datetime,
    expected_last_log_date: datetime,
    expected_log_count: int,
    expected_user_count: int,
    expected_human_count: int,
    expected_log_type_record_count: int,
    expected_user_type_record_count: int,
):
    """Assert Month Record"""

    assert_property_value(month_record, "id", expected_id)
    assert_property_value(
        month_record, "firstLogDate", expected_first_log_date.strftime(DATETIME_FORMAT)
    )
    assert_property_value(
        month_record, "lastLogDate", expected_last_log_date.strftime(DATETIME_FORMAT)
    )
    assert_property_value(month_record, "logCount", expected_log_count)
    assert_property_value(month_record, "allUsers", expected_user_count)
    assert_property_value(month_record, "humanUsers", expected_human_count)
    assert_layered_property_count(
        month_record, ["logTypeRecords"], expected_log_type_record_count
    )
    assert_layered_property_count(
        month_record, ["userTypeRecords"], expected_user_type_record_count
    )


# pylint: disable=too-many-arguments,too-many-positional-arguments
def assert_month_type_record(
    returned_month_type_record: dict,
    expected_id: str,
    expected_first_log_date: datetime,
    expected_last_log_date: datetime,
    expected_log_count: int,
    expected_user_count: int,
    expected_log_type: Optional[str] = None,
    expected_user_type: Optional[str] = None,
    expected_human_count: Optional[int] = None,
):
    """Assert Month User/Log Type"""

    assert (expected_log_type or expected_user_type) is not None

    assert_property_value(returned_month_type_record, "id", expected_id)

    if expected_log_type is not None:
        assert_property_value(returned_month_type_record, "logType", expected_log_type)

    if expected_user_type is not None:
        assert_property_value(
            returned_month_type_record, "userType", expected_user_type
        )

    assert_property_value(
        returned_month_type_record,
        "firstLogDate",
        expected_first_log_date.strftime(DATETIME_FORMAT),
    )
    assert_property_value(
        returned_month_type_record,
        "lastLogDate",
        expected_last_log_date.strftime(DATETIME_FORMAT),
    )
    assert_property_value(returned_month_type_record, "logCount", expected_log_count)
    assert_property_value(returned_month_type_record, "allUsers", expected_user_count)
    if expected_human_count is not None:
        assert_property_value(
            returned_month_type_record, "humanUsers", expected_human_count
        )
