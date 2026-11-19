"""Test create_ttfv_observation"""

from fetch_data.api_data.time_to_first_value.missing_values import missing_values
from fetch_data.api_data.time_to_first_value.wikibase_creation_log_model import (
    WikibaseCreationLogRecord,
)

Q1 = WikibaseCreationLogRecord(
    {"logid": 5, "title": "Item:Q1", "timestamp": "2026-11-19T00:00:00Z"}
)
Q2 = WikibaseCreationLogRecord(
    {"logid": 6, "title": "Item:Q2", "timestamp": "2026-11-19T00:00:02Z"}
)
Q10 = WikibaseCreationLogRecord(
    {"logid": 50, "title": "Item:Q10", "timestamp": "2026-11-19T00:00:10Z"}
)
Q50 = WikibaseCreationLogRecord(
    {"logid": 250, "title": "Item:Q50", "timestamp": "2026-11-19T00:00:50Z"}
)
Q100 = WikibaseCreationLogRecord(
    {"logid": 500, "title": "Item:Q100", "timestamp": "2026-11-19T00:01:40Z"}
)
Q1000 = WikibaseCreationLogRecord(
    {"logid": 5000, "title": "Item:Q1000", "timestamp": "2026-11-19T00:16:40Z"}
)
Q10000 = WikibaseCreationLogRecord(
    {"logid": 50000, "title": "Item:Q10000", "timestamp": "2026-11-19T02:46:40Z"}
)


def test_missing_fifty():
    """Test Missing Q50"""

    test_data = [Q1, Q10, Q100, Q1000, Q10000]
    assert missing_values(test_data) is True


def test_success():
    """Test Success"""

    test_data = [Q50, Q1, Q10, Q100, Q1000, Q10000]
    assert missing_values(test_data) is False


def test_too_few_values():
    """Test Too Few Values"""

    test_data = [Q50, Q1, Q10]
    assert missing_values(test_data) is True


def test_weird_value():
    """Test Including Q2"""

    test_data = [Q50, Q1, Q2, Q10, Q100, Q1000, Q10000]
    assert missing_values(test_data) is True
