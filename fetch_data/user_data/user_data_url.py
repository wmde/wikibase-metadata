"""URL for User Data"""

from fetch_data.utils import dict_to_url


def all_users_url(api_url: str, continue_from: str | None = None) -> str:
    """URL for User Data"""

    parameters = {
        "action": "query",
        "list": "allusers",
        "aulimit": "max",
        "auprop": "groups|implicitgroups",
        "format": "json",
        "aufrom": continue_from,
    }
    return f"{api_url}{dict_to_url(parameters)}"
