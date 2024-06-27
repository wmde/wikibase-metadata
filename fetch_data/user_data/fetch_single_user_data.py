"""Get User Data"""

import json
from typing import Iterable
import requests
from fetch_data.user_data.user_data_url import user_url
from model.database import WikibaseModel


def get_single_user_data(wikibase: WikibaseModel, user: str) -> dict:
    """Get User Data"""

    result = requests.get(wikibase.action_api_url.url + user_url(user), timeout=10)
    data = json.loads(result.content)
    return data["query"]["users"][0]


def get_multiple_user_data(wikibase: WikibaseModel, users: Iterable[str]) -> list[dict]:
    """Get User Data"""

    result = requests.get(
        wikibase.action_api_url.url + user_url("|".join(users)), timeout=10
    )
    data = json.loads(result.content)
    return data["query"]["users"]
