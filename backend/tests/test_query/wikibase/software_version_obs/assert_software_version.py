"""Assert Software Version"""

from datetime import datetime
from typing import Optional
from tests.utils import assert_property_value, DATETIME_FORMAT


def assert_software_version(
    returned_software_version: dict,
    expected_id: str,
    expected_name: str,
    expected_version: str,
    expected_version_date: Optional[datetime],
    expected_version_hash: Optional[str],
):
    """Assert Software Version"""

    assert_property_value(returned_software_version, "id", expected_id)
    assert_property_value(returned_software_version, "softwareName", expected_name)
    assert_property_value(returned_software_version, "version", expected_version)
    assert_property_value(
        returned_software_version,
        "versionDate",
        (
            expected_version_date
            if expected_version_date is None
            else expected_version_date.strftime(DATETIME_FORMAT)
        ),
    )
    assert_property_value(
        returned_software_version, "versionHash", expected_version_hash
    )
