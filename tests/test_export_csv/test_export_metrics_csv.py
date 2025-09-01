"""Test Export Metrics CSV"""

import os
import re
from typing import Callable
import pytest
from export_csv.metric import export_metric_csv


class MockBackgroundTasks:
    """Mock BackgroundTasks"""

    task_list = []

    # pylint: disable-next=unused-argument
    def add_task(self, func: Callable, *args):
        """
        Add Task

        really add filename to list
        """

        self.task_list.append(args[0])


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
        "total_ei_properties",
        "total_ei_statements",
        "total_url_properties",
        "total_url_statements",
        "recent_changes_observation_date",
        "first_change_date",
        "last_change_date",
        "human_change_count",
        "human_change_user_count",
        "bot_change_count",
        "bot_change_user_count",
        "software_version_observation_date",
        "software_name",
        "version\n",
    ]
)
EXPECTED_PATTERN = re.compile(
    ",".join(
        [
            r"\d+",
            r"(WikibaseType\.(CLOUD|OTHER|SUITE)|)",
            r"https?://[a-z0-9\-_.\?=/]+",
            # Quantity
            r"(\d{4}-\d\d-\d\d \d\d:\d\d:\d\d|)",
            r"(\d+\.0|)",
            r"(\d+\.0|)",
            r"(\d+\.0|)",
            r"(\d+\.0|)",
            r"(\d+\.0|)",
            r"(\d+\.0|)",
            r"(\d+\.0|)",
            r"(\d+\.0|)",
            # # Recent Changes
            r"(\d{4}-\d\d-\d\d \d\d:\d\d:\d\d|)",
            r"(\d{4}-\d\d-\d\d \d\d:\d\d:\d\d|)",
            r"(\d{4}-\d\d-\d\d \d\d:\d\d:\d\d|)",
            r"(\d+\.0|)",
            r"(\d+\.0|)",
            r"(\d+\.0|)",
            r"(\d+\.0|)",
            # # Software
            r"(\d{4}-\d\d-\d\d \d\d:\d\d:\d\d|)",
            r"(MediaWiki|)",
            r"(\d+\.\d+\.\d+|)\n",
        ]
    )
)


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

    mock_background_tasks = MockBackgroundTasks()

    result = await export_metric_csv(mock_background_tasks)
    assert len(mock_background_tasks.task_list) == 1
    assert result.status_code == 200
    assert result.media_type == "text/csv"
    # CANNOT FIGURE OUT HOW TO CHECK CONTENT OF RESPONSE

    with open(mock_background_tasks.task_list[0], mode="r", encoding="utf-8") as file:
        returned_lines = file.readlines()
        assert returned_lines[0] == EXPECTED_HEADER_ROW
        for returned_line in returned_lines[1:]:
            assert EXPECTED_PATTERN.match(returned_line)

    for file in mock_background_tasks.task_list:
        os.remove(file)
