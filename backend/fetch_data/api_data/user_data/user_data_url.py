"""URL for User Data"""

from fetch_data.utils import dict_to_url


def all_users_url(continue_from: str | None = None) -> str:
    """URL for All User Data"""

    parameters = {
        "action": "query",
        "list": "allusers",
        "aulimit": "max",
        "auprop": "groups|implicitgroups",
        "format": "json",
        "aufrom": continue_from,
    }
    return dict_to_url(parameters)


def user_url(user: str) -> str:
    """Single User Url"""

    parameters = {
        "action": "query",
        "list": "users",
        "ususers": user,
        "usprop": "groups",
        "format": "json",
    }
    return dict_to_url(parameters)
