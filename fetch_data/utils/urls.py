"""URL Utilities"""


def dict_to_url(parameters: dict) -> str:
    """URL parameter dictionary"""

    return "?" + "&".join([f"{k}={v}" for k, v in parameters.items() if v is not None])
