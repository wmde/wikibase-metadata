"""Get Item Namespace"""

from fetch_data.utils import dict_to_url, fetch_api_data
from model.database import WikibaseModel


async def get_item_namespace(wikibase: WikibaseModel) -> int:
    """Check Namespace for Items"""

    namespace_data: dict = await fetch_api_data(
        wikibase.action_api_url()
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
    for namespace_id, namespace in namespaces.items():
        if "canonical" in namespace and namespace["canonical"] == "Item":
            return namespace_id

    raise ValueError("No Item Namespace Found")
