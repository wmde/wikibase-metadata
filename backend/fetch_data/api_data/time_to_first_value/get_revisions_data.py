"""Fetch Revisions Data"""

from fetch_data.api_data.time_to_first_value.wikibase_revision_model import (
    WikibaseRevisionRecord,
)
from fetch_data.utils import dict_to_url, fetch_api_data


async def get_all_revision_logs(
    api_url: str, namespace_id: int
) -> list[WikibaseRevisionRecord]:
    """Fetch All Revisions"""

    data: list = []

    parameters = {
        "action": "query",
        "format": "json",
        "list": "allrevisions",
        "arvnamespace": namespace_id,
        "arvdir": "newer",
        "arvlimit": "max",
        "arvprop": "ids|title|timestamp",
    }

    data: list[WikibaseRevisionRecord] = []

    should_query = True
    while should_query:
        query_data = await fetch_api_data(api_url + dict_to_url(parameters))

        for record in query_data["query"]["allrevisions"]:
            data.append(WikibaseRevisionRecord(record))

        should_query = (
            "continue" in query_data and "arvcontinue" in query_data["continue"]
        )
        if should_query:
            parameters["arvcontinue"] = query_data["continue"]["arvcontinue"]

    return data
