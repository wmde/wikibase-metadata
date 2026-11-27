"""Get Namespaces"""

from fetch_data.utils import dict_to_url, fetch_api_data


async def get_namespaces(api_url: str) -> dict[int, dict[str, str | int]]:
    """Check Namespace for Items"""

    namespace_data: dict = await fetch_api_data(
        api_url
        + dict_to_url(
            {
                "action": "query",
                "meta": "siteinfo",
                "siprop": "namespaces",
                "format": "json",
            }
        )
    )
    namespaces: dict[int, dict[str, str | int]] = namespace_data["query"]["namespaces"]
    return namespaces

