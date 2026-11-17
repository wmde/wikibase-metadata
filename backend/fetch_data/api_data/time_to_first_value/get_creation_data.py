"""Item Creation Logs"""

from typing import Optional

from fetch_data.api_data.time_to_first_value.wikibase_creation_log_model import (
    WikibaseCreationLogRecord,
)
from fetch_data.utils import dict_to_url, fetch_api_data

CREATE_ITEM_PARAMETERS = {
    "action": "query",
    "format": "json",
    "list": "logevents",
    "letype": "create",
    # "lenamespace": namespace_id,
    "ledir": "newer",
    # "lelimit": "max",
    "leprop": "ids|title|timestamp",
}


async def get_all_creation_logs(api_url: str) -> list[WikibaseCreationLogRecord]:

    data: list[WikibaseCreationLogRecord] = []

    q_number = 1
    returning = True

    while returning or q_number <= 1000:
        record = await get_creation_log(api_url=api_url, q_number=q_number)

        if record is not None:
            data.append(record)

        returning = record is not None
        q_number *= 10

    return data


async def get_creation_log(
    api_url: str, q_number: int
) -> Optional[WikibaseCreationLogRecord]:
    parameters = dict(CREATE_ITEM_PARAMETERS)
    parameters["letitle"] = f"Item:Q{q_number}"
    parameters["lelimit"] = "max"
    query_data = await fetch_api_data(api_url + dict_to_url(parameters))

    if len(query_data["query"]["logevents"]) == 1:
        return WikibaseCreationLogRecord(query_data["query"]["logevents"][0])
    if len(query_data["query"]["logevents"]) == 0:
        return None
    raise ValueError("Multiple Records Found")
