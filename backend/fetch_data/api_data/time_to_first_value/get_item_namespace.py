"""Get Item Namespace"""

from fetch_data.api_data.util import get_namespaces, parse_namespace


async def get_item_namespace(api_url: str) -> int | str:
    """Check Namespace for Items"""

    namespaces = await get_namespaces(api_url=api_url)
    item_namespace_id = parse_namespace(namespaces, prop="canonical", value="Item")

    if item_namespace_id is None:
        raise ValueError("No Item Namespace Found")

    return item_namespace_id
