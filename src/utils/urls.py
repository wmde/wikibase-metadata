def listPropertiesURL(base: str, property_type: str, limit: int) -> str:
    return f"{base}/w/index.php?title=Special:ListProperties/{property_type}&limit={limit}&offset=0"


def dailyPageviewsURL(base: str) -> str:
    return f"{base}/w/api.php?action=query&titles=Main_Page&prop=pageviews"


def dictToURL(parameters: dict) -> str:
    return "?" + "&".join([f"{k}={v}" for k, v in parameters.items() if v is not None])
