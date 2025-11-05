"""Fetch User Type"""

import re
from model.enum import WikibaseUserType


def get_user_type_from_user_data(user_data: dict) -> WikibaseUserType:
    """User Type from User Data"""

    if re.search(r"\b(bot|script)\b", user_data["name"], re.IGNORECASE) is not None:
        return WikibaseUserType.BOT
    if "groups" not in user_data and ("invalid" in user_data or "missing" in user_data):
        return WikibaseUserType.MISSING
    if "bot" in user_data["groups"]:
        return WikibaseUserType.BOT
    return WikibaseUserType.USER
