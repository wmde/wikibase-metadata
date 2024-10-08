"""Fetch User Type"""

import re
from typing import Optional
from fetch_data.api_data.user_data.fetch_single_user_data import get_single_user_data
from model.database import WikibaseModel
from model.enum import WikibaseUserType


def get_user_type_from_wikibase(
    wikibase: WikibaseModel, user: Optional[str]
) -> WikibaseUserType:
    """User Type from Wikibase"""

    if user is None:
        return WikibaseUserType.NONE

    user_data = get_single_user_data(wikibase, user)
    return get_user_type_from_user_data(user_data)


def get_user_type_from_user_data(user_data: dict) -> WikibaseUserType:
    """User Type from User Data"""

    if re.search(r"\b(bot|script)\b", user_data["name"], re.IGNORECASE) is not None:
        return WikibaseUserType.BOT
    if "groups" not in user_data and ("invalid" in user_data or "missing" in user_data):
        return WikibaseUserType.MISSING
    if "bot" in user_data["groups"]:
        return WikibaseUserType.BOT
    return WikibaseUserType.USER
