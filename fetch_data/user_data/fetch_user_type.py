"""Fetch Log Data"""

from typing import Optional
from fetch_data.user_data.fetch_single_user_data import get_single_user_data
from model.database import WikibaseModel, WikibaseUserType


def get_user_type(wikibase: WikibaseModel, user: Optional[str]) -> WikibaseUserType:
    """User or Bot?"""

    if user is None:
        return WikibaseUserType.NONE

    user_data = get_single_user_data(wikibase, user)
    return get_user_type_from_user_data(user_data)


def get_user_type_from_user_data(user_data: dict) -> WikibaseUserType:
    """User or Bot?"""

    if "groups" not in user_data and ("invalid" in user_data or "missing" in user_data):
        return WikibaseUserType.MISSING
    if "bot" in user_data["groups"]:
        return WikibaseUserType.BOT
    return WikibaseUserType.USER
