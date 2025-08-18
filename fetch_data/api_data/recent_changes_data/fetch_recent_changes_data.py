"""Fetch Recent Changes Data"""

from datetime import datetime, timedelta, UTC
from typing import Optional

from fetch_data.api_data.recent_changes_data.wikibase_recent_change_record import (
    WikibaseRecentChangeRecord,
)
from fetch_data.utils import dict_to_url, fetch_api_data


def get_recent_changes_param_string(
    limit: Optional[int] = None,
    continue_from: Optional[str] = None,
    bots: bool = False,
) -> str:
    """Recent Changes Page URL Parameters"""
    parameters: dict = {
        "action": "query",
        "format": "json",
        "list": "recentchanges",
        "formatversion": 2,
        "rcprop": "user|userid|timestamp",
        "rclimit": limit,
    }
    if bots:
        parameters["rcshow"] = "bot"
    else:
        parameters["rcshow"] = "!bot"
    if continue_from is not None:
        parameters["rccontinue"] = continue_from
    return dict_to_url(parameters)


async def get_recent_changes_list(
    api_url: str, bots: bool = False
) -> list[WikibaseRecentChangeRecord]:
    """Get Recent Changes List from api_url, for the last 30 days"""

    data: list[WikibaseRecentChangeRecord] = []
    limit = 500

    should_query = True
    next_from: Optional[str] = None
    thirty_days_ago = datetime.now(UTC) - timedelta(days=30)

    while should_query:
        query_data = await fetch_api_data(
            api_url
            + get_recent_changes_param_string(
                limit=limit, continue_from=next_from, bots=bots
            )
        )

        for record in query_data["query"]["recentchanges"]:
            data.append(WikibaseRecentChangeRecord(record))

        # The API returns recent changes in descending order of time.
        # So the last one in the list is the oldest.
        oldest_record_in_batch_date = data[-1].timestamp

        should_query = (
            oldest_record_in_batch_date > thirty_days_ago
            and "continue" in query_data
            and "rccontinue" in query_data["continue"]
        )
        if should_query:
            next_from = query_data["continue"]["rccontinue"]

    return [datum for datum in data if datum.timestamp >= thirty_days_ago]
