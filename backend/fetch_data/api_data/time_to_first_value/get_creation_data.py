"""Item Creation Logs"""

from fetch_data.api_data.time_to_first_value.wikibase_creation_log_model import (
    WikibaseCreationLogRecord,
)
from fetch_data.utils import dict_to_url, fetch_api_data


async def get_all_creation_logs(api_url: str) -> list[WikibaseCreationLogRecord]:

    parameters = {
        "action": "query",
        "format": "json",
        "list": "logevents",
        "letype": "create",
        # "lenamespace": namespace_id,
        "ledir": "newer",
        "lelimit": "max",
        "leprop": "ids|title|timestamp",
    }

    data: list[WikibaseCreationLogRecord] = []

    q_number = 1
    returning = True

    while returning or q_number <= 1000:
        parameters["letitle"] = f"Item:Q{q_number}"
        query_data = await fetch_api_data(api_url + dict_to_url(parameters))

        for record in query_data["query"]["logevents"]:
            data.append(WikibaseCreationLogRecord(record))

        returning = len(query_data["query"]["logevents"]) > 0
        q_number *= 10

    return data
