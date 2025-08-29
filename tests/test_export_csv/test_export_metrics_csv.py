"""Test Export Metrics CSV"""

import shutil
from typing import Callable
import pytest
from export_csv.metric import export_metric_csv


class MockBackgroundTasks:
    """Mock BackgroundTasks"""

    def add_task(func: Callable, *args):
        """Add Task"""
        pass


EXPECTED_CONTENT = """
wikibase_id,wikibase_type,quantity_observation_date,total_items,total_lexemes,total_properties,total_triples,total_ei_properties,total_ei_statements,total_url_properties,total_url_statements,recent_changes_observation_date,first_change_date,last_change_date,human_change_count,human_change_user_count,bot_change_count,bot_change_user_count,software_version_observation_date,software_name,version
1,WikibaseType.SUITE,2025-08-29 10:35:13,2.0,4.0,1.0,8.0,16.0,32.0,64.0,128.0,2025-08-29 10:34:51,2024-03-01 12:00:00,2024-03-05 12:00:00,5.0,4.0,1.0,1.0,2025-08-29 10:34:40,MediaWiki,1.39.8
2,,,,,,,,,,,,,,,,,,2025-08-29 10:34:44,MediaWiki,1.39.8
3,WikibaseType.CLOUD,,,,,,,,,,,,,,,,,,,
5,WikibaseType.OTHER,,,,,,,,,,,,,,,,,,,
6,WikibaseType.CLOUD,,,,,,,,,,,,,,,,,,,
7,WikibaseType.CLOUD,,,,,,,,,,,,,,,,,,,
8,WikibaseType.CLOUD,,,,,,,,,,,,,,,,,,,
9,WikibaseType.CLOUD,,,,,,,,,,,,,,,,,,,
10,WikibaseType.CLOUD,,,,,,,,,,,,,,,,,,,
11,WikibaseType.CLOUD,,,,,,,,,,,,,,,,,,,
"""


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
    assert result.status_code == 200
    assert result.media_type == "text/csv"
    # CANNOT FIGURE OUT HOW TO CHECK CONTENT

    shutil.rmtree("export/data")
