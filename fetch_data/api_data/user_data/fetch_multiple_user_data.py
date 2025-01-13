"""Fetch Multiple User Data"""

from collections.abc import Iterable
from fetch_data.api_data.user_data.user_data_url import user_url
from fetch_data.utils.fetch_data_from_api import fetch_api_data
from model.database import WikibaseModel


MULTIPLE_USER_QUERY_LIMIT = 50


async def get_multiple_user_data(
    wikibase: WikibaseModel, users: Iterable[str]
) -> list[dict]:
    """Fetch Multiple User Data"""

    if len(users) == 0:
        return []

    if len(users) > MULTIPLE_USER_QUERY_LIMIT:
        data = []
        list_users = list(users)
        for i in range(0, len(users), MULTIPLE_USER_QUERY_LIMIT):
            data.extend(
                await get_multiple_user_data(
                    wikibase, list_users[i : i + MULTIPLE_USER_QUERY_LIMIT]
                )
            )
        return data

    data = await fetch_api_data(wikibase.action_api_url.url + user_url("|".join(users)))
    return data["query"]["users"]
