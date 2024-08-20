"""Get User Data"""

import json
import requests
from fetch_data.api_data.user_data.user_data_url import user_url
from model.database import WikibaseModel


def get_single_user_data(wikibase: WikibaseModel, user: str) -> dict:
    """Get User Data"""

    result = requests.get(wikibase.action_api_url.url + user_url(user), timeout=10)
    data = json.loads(result.content)
    return data["query"]["users"][0]
