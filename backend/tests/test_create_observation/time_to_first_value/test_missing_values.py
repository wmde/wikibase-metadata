"""Test create_ttfv_observation"""

from fetch_data.api_data.time_to_first_value.missing_values import missing_values
from fetch_data.api_data.time_to_first_value.wikibase_creation_log_model import (
    WikibaseCreationLogRecord,
)

DATA_DIRECTORY = "tests/test_create_observation/time_to_first_value/data"

FETCH_TTFV_MUTATION = """mutation MyMutation($wikibaseId: Int!) {
  fetchTimeToFirstValueData(wikibaseId: $wikibaseId)
}"""


def test_missing_fifty():
    """Test Missing Q50"""

    test_data = [
        WikibaseCreationLogRecord(
            {"logid": 5, "title": "Item:Q1", "timestamp": "2026-11-19T00:00:00Z"}
        ),
        WikibaseCreationLogRecord(
            {"logid": 50, "title": "Item:Q10", "timestamp": "2026-11-19T00:00:10Z"}
        ),
        WikibaseCreationLogRecord(
            {"logid": 500, "title": "Item:Q100", "timestamp": "2026-11-19T00:01:40Z"}
        ),
        WikibaseCreationLogRecord(
            {"logid": 5000, "title": "Item:Q1000", "timestamp": "2026-11-19T00:16:40Z"}
        ),
        WikibaseCreationLogRecord(
            {
                "logid": 50000,
                "title": "Item:Q10000",
                "timestamp": "2026-11-19T02:46:40Z",
            }
        ),
    ]
    assert missing_values(test_data) == True


def test_success():
    """Test Success"""

    test_data = [
        WikibaseCreationLogRecord(
            {"logid": 250, "title": "Item:Q50", "timestamp": "2026-11-19T00:00:50Z"}
        ),
        WikibaseCreationLogRecord(
            {"logid": 5, "title": "Item:Q1", "timestamp": "2026-11-19T00:00:00Z"}
        ),
        WikibaseCreationLogRecord(
            {"logid": 50, "title": "Item:Q10", "timestamp": "2026-11-19T00:00:10Z"}
        ),
        WikibaseCreationLogRecord(
            {"logid": 500, "title": "Item:Q100", "timestamp": "2026-11-19T00:01:40Z"}
        ),
        WikibaseCreationLogRecord(
            {"logid": 5000, "title": "Item:Q1000", "timestamp": "2026-11-19T00:16:40Z"}
        ),
        WikibaseCreationLogRecord(
            {
                "logid": 50000,
                "title": "Item:Q10000",
                "timestamp": "2026-11-19T02:46:40Z",
            }
        ),
    ]
    assert missing_values(test_data) == True


def test_too_few_values():
    """Test Too Few Values"""

    test_data = [
        WikibaseCreationLogRecord(
            {"logid": 250, "title": "Item:Q50", "timestamp": "2026-11-19T00:00:50Z"}
        ),
        WikibaseCreationLogRecord(
            {"logid": 5, "title": "Item:Q1", "timestamp": "2026-11-19T00:00:00Z"}
        ),
        WikibaseCreationLogRecord(
            {"logid": 50, "title": "Item:Q10", "timestamp": "2026-11-19T00:00:10Z"}
        ),
    ]
    assert missing_values(test_data) == True


def test_weird_value():
    """Test Including Q2"""

    test_data = [
        WikibaseCreationLogRecord(
            {"logid": 250, "title": "Item:Q50", "timestamp": "2026-11-19T00:00:50Z"}
        ),
        WikibaseCreationLogRecord(
            {"logid": 5, "title": "Item:Q1", "timestamp": "2026-11-19T00:00:00Z"}
        ),
        WikibaseCreationLogRecord(
            {"logid": 6, "title": "Item:Q2", "timestamp": "2026-11-19T00:00:02Z"}
        ),
        WikibaseCreationLogRecord(
            {"logid": 50, "title": "Item:Q10", "timestamp": "2026-11-19T00:00:10Z"}
        ),
        WikibaseCreationLogRecord(
            {"logid": 500, "title": "Item:Q100", "timestamp": "2026-11-19T00:01:40Z"}
        ),
        WikibaseCreationLogRecord(
            {"logid": 5000, "title": "Item:Q1000", "timestamp": "2026-11-19T00:16:40Z"}
        ),
        WikibaseCreationLogRecord(
            {
                "logid": 50000,
                "title": "Item:Q10000",
                "timestamp": "2026-11-19T02:46:40Z",
            }
        ),
    ]
    assert missing_values(test_data) == True
