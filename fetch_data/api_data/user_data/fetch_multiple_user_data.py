"""Get User Data"""

import json
from typing import Iterable
import requests
from fetch_data.api_data.user_data.user_data_url import user_url
from model.database import WikibaseModel


MULTIPLE_USER_QUERY_LIMIT = 50


def get_multiple_user_data(wikibase: WikibaseModel, users: Iterable[str]) -> list[dict]:
    """Get User Data"""

    if len(users) == 0:
        return []

    if len(users) > MULTIPLE_USER_QUERY_LIMIT:
        data = []
        list_users = list(users)
        for i in range(0, len(users), MULTIPLE_USER_QUERY_LIMIT):
            data.extend(
                get_multiple_user_data(
                    wikibase, list_users[i : i + MULTIPLE_USER_QUERY_LIMIT]
                )
            )
        return data

    result = requests.get(
        wikibase.action_api_url.url + user_url("|".join(users)), timeout=10
    )
    data = json.loads(result.content)
    return data["query"]["users"]
