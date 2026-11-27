"""Get Namespaces"""

from typing import Optional

from fetch_data.utils import dict_to_url, fetch_api_data


async def get_namespaces(api_url: str) -> dict[int, dict[str, str | int]]:
    """Get Namespace Data"""

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


def parse_namespace(
    namespaces: dict[int, dict[str, str | int]], prop: str, value: str
) -> Optional[int | str]:
    """Parse Namespaces"""

    for namespace_id, namespace in namespaces.items():
        if prop in namespace and namespace[prop] == value:
            return namespace_id

    return None
