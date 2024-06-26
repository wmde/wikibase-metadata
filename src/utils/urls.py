def listPropertiesURL(base: str, property_type: str, limit: int) -> str:
    parameters = {
        "title": f"Special:ListProperties/{property_type}",
        "limit": limit,
        "offset": 0,
    }
    return f"{base}/w/index.php{dictToURL(parameters)}"


def dailyPageviewsURL(base: str) -> str:
    parameters = {"action": "query", "titles": "Main_Page", "prop": "pageviews"}
    return f"{base}/w/api.php{dictToURL(parameters)}"


def dictToURL(parameters: dict) -> str:
    return "?" + "&".join([f"{k}={v}" for k, v in parameters.items() if v is not None])
