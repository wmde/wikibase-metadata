"""Item Creation Logs"""

from fetch_data.api_data.time_to_first_value.wikibase_creation_log_model import (
    WikibaseCreationLogRecord,
)
from fetch_data.utils import fetch_api_data
from fetch_data.utils.urls import dict_to_url


async def get_all_creation_logs(
    api_url: str, namespace_id: int
) -> list[WikibaseCreationLogRecord]:

    parameters = {
        "action": "query",
        "format": "json",
        "list": "logevents",
        "letype": "create",
        "lenamespace": namespace_id,
        "ledir": "newer",
        "lelimit": "max",
        "leprop": "ids|title|timestamp",
    }

    data: list[WikibaseCreationLogRecord] = []

    should_query = True
    while should_query:
        query_data = await fetch_api_data(api_url + dict_to_url(parameters))

        for record in query_data["query"]["logevents"]:
            data.append(WikibaseCreationLogRecord(record))

        should_query = (
            "continue" in query_data and "lecontinue" in query_data["continue"]
        )
        if should_query:
            parameters["lecontinue"] = query_data["continue"]["lecontinue"]

    return data
