"""Fetch Log Data"""

from datetime import datetime
from typing import List, Optional
from fetch_data.log_data.wikibase_log_record import WikibaseLogRecord
from fetch_data.utils import dict_to_url, fetch_api_data


def get_log_param_string(
    limit: Optional[int] = None, oldest: bool = False, offset: Optional[str] = None
):
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
    return dict_to_url(parameters)


def get_log_list_from_url(url: str) -> List[WikibaseLogRecord]:
    """Get Log List from URL"""

    data = []

    query_data = fetch_api_data(url)
    for record in query_data["query"]["logevents"]:
        data.append(WikibaseLogRecord(record))

    return data


def get_month_log_list(
    api_url: str, comparison_date: datetime, oldest: bool = False
) -> List[WikibaseLogRecord]:
    """Get Log List from api_url"""

    data: List[WikibaseLogRecord] = []
    limit = 500

    should_query = True
    next_from: Optional[str] = None
    # directory = f"data/logs/{re.sub(r'[^a-z]+', r'_', api_url)}"
    # os.makedirs(directory, exist_ok=True)
    while should_query:
        # print(next_from)
        query_data = fetch_api_data(
            api_url + get_log_param_string(limit=limit, offset=next_from, oldest=oldest)
        )

        # with open(f"{directory}/{datetime.now()}.json", "w", encoding="utf-8") as temp:
        #     json.dump(query_data, temp, indent="\t", sort_keys=False)
        for record in query_data["query"]["logevents"]:
            data.append(WikibaseLogRecord(record))

        # print(query_data.get('continue'))

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

    return data
