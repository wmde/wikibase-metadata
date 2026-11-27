"""Fetch Total Page Count"""

from fetch_data.utils import dict_to_url, fetch_api_data

ALL_PAGES_PARAMETERS = {
    "action": "query",
    "list": "allpages",
    "apnamespace": None,
    "aplimit": "max",
    "format": "json",
}


async def fetch_total_page_count(api_url: str, namespace_id: int | str) -> int:
    """Get Count of Unique Pages"""

    parameters = dict(ALL_PAGES_PARAMETERS)
    parameters["apnamespace"] = namespace_id

    data = set()

    should_query = True
    while should_query:
        query_data = await fetch_api_data(api_url + dict_to_url(parameters))

        for record in query_data["query"]["allpages"]:
            data.add(record["title"])

        if should_query := (
            "continue" in query_data and "apcontinue" in query_data["continue"]
        ):
            parameters["apcontinue"] = query_data["continue"]["apcontinue"]

    return len(data)
