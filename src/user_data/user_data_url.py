from src.utils.urls import dictToURL


def usersURL(api_url: str, continue_from: str | None = None) -> str:
    parameters = {
        "action": "query",
        "list": "allusers",
        "aulimit": "max",
        "auprop": "groups|implicitgroups",
        "format": "json",
        "aufrom": continue_from,
    }
    return f"{api_url}{dictToURL(parameters)}"
