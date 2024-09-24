"""Assert Quantity Observation"""

from typing import Optional
from tests.utils import assert_layered_property_value, assert_property_value


def assert_edits(
    returned_statistics: dict, expected_total_edits: int, expected_average_edits: float
):
    """Assert Edits"""

    assert_layered_property_value(
        returned_statistics, ["edits", "editsPerPageAvg"], expected_average_edits
    )
    assert_layered_property_value(
        returned_statistics, ["edits", "totalEdits"], expected_total_edits
    )


def assert_files(returned_statistics: dict, expected_total_files: int):
    """Assert Files"""

    assert_layered_property_value(
        returned_statistics, ["files", "totalFiles"], expected_total_files
    )


def assert_pages(
    returned_statistics: dict,
    expected_content_pages: int,
    expected_content_page_word_count_avg: float,
    expected_content_page_word_count_total: int,
    expected_total_pages: int,
):
    """Assert Pages"""

    assert_layered_property_value(
        returned_statistics, ["pages", "contentPages"], expected_content_pages
    )
    assert_layered_property_value(
        returned_statistics,
        ["pages", "contentPageWordCountAvg"],
        expected_content_page_word_count_avg,
    )
    assert_layered_property_value(
        returned_statistics,
        ["pages", "contentPageWordCountTotal"],
        expected_content_page_word_count_total,
    )
    assert_layered_property_value(
        returned_statistics, ["pages", "totalPages"], expected_total_pages
    )


def assert_users(
    returned_statistics: dict,
    expected_active_users: int,
    expected_total_admin: int,
    expected_total_users: int,
):
    """Assert Users"""

    assert_layered_property_value(
        returned_statistics, ["users", "activeUsers"], expected_active_users
    )
    assert_layered_property_value(
        returned_statistics, ["users", "totalAdmin"], expected_total_admin
    )
    assert_layered_property_value(
        returned_statistics, ["users", "totalUsers"], expected_total_users
    )


# pylint: disable=too-many-arguments,too-many-positional-arguments
def assert_statistics(
    returned_statistics: dict,
    expected_id: str,
    expected_returned_data: bool,
    expected_edits: Optional[tuple[int, float]] = None,
    expected_files: Optional[tuple[int]] = None,
    expected_pages: Optional[tuple[int, float, int, int]] = None,
    expected_users: Optional[tuple[int, int, int]] = None,
):
    """Assert Statistics Observation"""

    assert_property_value(returned_statistics, "id", expected_id)
    assert "observationDate" in returned_statistics
    assert_property_value(returned_statistics, "returnedData", expected_returned_data)

    if expected_edits is None:
        assert_property_value(returned_statistics, "edits", None)
    else:
        assert_edits(
            returned_statistics,
            expected_total_edits=expected_edits[0],
            expected_average_edits=expected_edits[1],
        )

    if expected_files is None:
        assert_property_value(returned_statistics, "files", None)
    else:
        assert_files(returned_statistics, expected_total_files=expected_files[0])

    if expected_pages is None:
        assert_property_value(returned_statistics, "pages", None)
    else:
        assert_pages(
            returned_statistics,
            expected_content_pages=expected_pages[0],
            expected_content_page_word_count_avg=expected_pages[1],
            expected_content_page_word_count_total=expected_pages[2],
            expected_total_pages=expected_pages[3],
        )

    if expected_users is None:
        assert_property_value(returned_statistics, "users", None)
    else:
        assert_users(
            returned_statistics,
            expected_active_users=expected_users[0],
            expected_total_admin=expected_users[1],
            expected_total_users=expected_users[2],
        )
