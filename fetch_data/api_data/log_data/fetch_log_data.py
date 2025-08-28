"""Fetch Log Data"""

from datetime import datetime
from typing import Optional
from fetch_data.api_data.log_data.wikibase_log_record import WikibaseLogRecord
from fetch_data.utils import dict_to_url, fetch_api_data


def get_log_param_string(
    limit: Optional[int] = None,
    oldest: bool = False,
    offset: Optional[str] = None,
    prop: Optional[list[str]] = None,
) -> str:
    """Log Page URL Parameters"""

    parameters: dict = {
        "action": "query",
        "format": "json",
        "list": "logevents",
        "formatversion": 2,
        "ledir": "newer" if oldest else "older",
        "lelimit": limit,
    }
    if offset is not None:
        parameters["lecontinue"] = offset
    if prop is not None:
        parameters["leprop"] = "|".join(prop)
    return dict_to_url(parameters)


async def get_log_list_from_url(url: str) -> list[WikibaseLogRecord]:
    """Get Log List from URL"""

    data: list[WikibaseLogRecord] = []

    query_data = await fetch_api_data(url)
    for record in query_data["query"]["logevents"]:
        data.append(WikibaseLogRecord(record))

    return data


async def get_month_log_list(
    api_url: str, comparison_date: datetime, oldest: bool = False
) -> list[WikibaseLogRecord]:
    """Get Log List from api_url, limit to within 30 days of the comparison date"""

    data: list[WikibaseLogRecord] = []
    limit = 500

    should_query = True
    next_from: Optional[str] = None
    while should_query:
        query_data = await fetch_api_data(
            api_url + get_log_param_string(limit=limit, offset=next_from, oldest=oldest)
        )

        for record in query_data["query"]["logevents"]:
            data.append(WikibaseLogRecord(record))

        should_query = (
            (
                abs(
                    (
                        comparison_date
                        - (
                            max(data, key=lambda x: x.log_date)
                            if oldest
                            else min(data, key=lambda x: x.log_date)
                        ).log_date
                    ).days
                )
                <= 30
            )
            and "continue" in query_data
            and "lecontinue" in query_data["continue"]
        )
        if should_query:
            next_from = query_data["continue"]["lecontinue"]

    return [
        datum for datum in data if abs((comparison_date - datum.log_date).days) <= 30
    ]
