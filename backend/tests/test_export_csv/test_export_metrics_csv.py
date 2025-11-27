"""Test Export Metrics CSV"""

import re
import pytest
from fastapi.testclient import TestClient
from app import app


EXPECTED_HEADER_ROW = ",".join(
    [
        "wikibase_id",
        "wikibase_type",
        "base_url",
        "quantity_observation_date",
        "total_items",
        "total_lexemes",
        "total_properties",
        "total_triples",
        "ei_observation_date",
        "total_ei_properties",
        "total_ei_statements",
        "total_url_properties",
        "total_url_statements",
        "recent_changes_observation_date",
        "first_change_date",
        "last_change_date",
        "human_change_count",
        "human_change_user_count",
        "human_change_active_user_count",
        "bot_change_count",
        "bot_change_user_count",
        "bot_change_active_user_count",
        "software_version_observation_date",
        "software_name",
        "version",
    ]
)
EXPECTED_PATTERN_LIST = [
    re.compile(r"\d+"),
    re.compile(r"(WikibaseType\.(CLOUD|OTHER|SUITE)|)"),
    re.compile(r"https?://[a-z0-9\-_.\?=/]+"),
    # Quantity
    re.compile(r"(\d{4}-\d\d-\d\d \d\d:\d\d:\d\d.\d+\+00:00|)"),
    re.compile(r"(\d+\.0|)"),
    re.compile(r"(\d+\.0|)"),
    re.compile(r"(\d+\.0|)"),
    re.compile(r"(\d+\.0|)"),
    # External Identifier
    re.compile(r"(\d{4}-\d\d-\d\d \d\d:\d\d:\d\d.\d+\+00:00|)"),
    re.compile(r"(\d+\.0|)"),
    re.compile(r"(\d+\.0|)"),
    re.compile(r"(\d+\.0|)"),
    re.compile(r"(\d+\.0|)"),
    # # Recent Changes
    re.compile(r"(\d{4}-\d\d-\d\d \d\d:\d\d:\d\d.\d+\+00:00|)"),
    re.compile(r"(\d{4}-\d\d-\d\d \d\d:\d\d:\d\d.\d+\+00:00|)"),
    re.compile(r"(\d{4}-\d\d-\d\d \d\d:\d\d:\d\d.\d+\+00:00|)"),
    re.compile(r"(\d+\.0|)"),
    re.compile(r"(\d+\.0|)"),
    re.compile(r"(\d+\.0|)"),
    re.compile(r"(\d+\.0|)"),
    re.compile(r"(\d+\.0|)"),
    re.compile(r"(\d+\.0|)"),
    # # Software
    re.compile(r"(\d{4}-\d\d-\d\d \d\d:\d\d:\d\d.\d+\+00:00|)"),
    re.compile(r"(MediaWiki|)"),
    re.compile(r"(\d+\.\d+\.\d+|)"),
]


@pytest.mark.asyncio
@pytest.mark.dependency(
    depends=[
        "update-wikibase-type-other",
        "update-wikibase-type-suite",
        "update-wikibase-type-test",
    ],
    scope="session",
)
async def test_export_metric_csv():
    """Test Export Metric CSV"""

    client = TestClient(app)
    result = client.get("/csv/metrics?authorization=test-auth-token")
    assert result.status_code == 200
    content = result.content.decode("utf-8")

    lines = content.splitlines()
    assert len(lines) >= 2
    assert lines[0] == EXPECTED_HEADER_ROW

    for line in lines[1:]:
        for i, pattern in enumerate(EXPECTED_PATTERN_LIST):
            assert pattern.match(line.split(",")[i])
