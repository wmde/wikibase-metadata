"""Get Item Namespace"""

from fetch_data.api_data.util import get_namespaces


async def get_item_namespace(api_url: str) -> int | str:
    """Check Namespace for Items"""

    namespaces = await get_namespaces(api_url=api_url)
    for namespace_id, namespace in namespaces.items():
        if "canonical" in namespace and namespace["canonical"] == "Item":
            return namespace_id

    raise ValueError("No Item Namespace Found")
