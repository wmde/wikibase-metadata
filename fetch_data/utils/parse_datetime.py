"""Parse Datetime"""

from datetime import datetime
import re
from typing import Optional


# pylint: disable-next=too-many-return-statements
def parse_datetime(date_string: Optional[str]) -> Optional[datetime]:
    """Parse Datetime"""

    if date_string is None:
        return None

    initial_clean_date_string = re.sub(r"[,.]", r"", date_string)

    try:
        return datetime.strptime(initial_clean_date_string, "%H:%M %d %B %Y")
    except ValueError:
        pass

    try:
        return datetime.strptime(initial_clean_date_string, "%H:%M %d %b %Y")
    except ValueError:
        pass

    try:
        return datetime.strptime(initial_clean_date_string, "%H:%M %B %d %Y")
    except ValueError:
        pass

    try:
        return datetime.strptime(initial_clean_date_string, "%d %b %Y %H:%M")
    except ValueError:
        pass

    month_abbreviated_date_string = re.sub(
        r"([a-z]{3})[a-z]+", r"\1", initial_clean_date_string
    ).lower()

    # German
    if (
        un_german_date_string := month_abbreviated_date_string.replace("mär", "mar")
        .replace("mai", "may")
        .replace("okt", "oct")
        .replace("dez", "dec")
    ) != month_abbreviated_date_string:
        return parse_datetime(un_german_date_string)

    # Italian
    if (
        un_italian_date_string := month_abbreviated_date_string.replace("gen", "jan")
        .replace("mag", "may")
        .replace("giu", "jun")
        .replace("lug", "jul")
        .replace("ago", "aug")
        .replace("ott", "oct")
        .replace("dic", "dec")
    ) != month_abbreviated_date_string:
        return parse_datetime(un_italian_date_string)

    # Polish
    if (
        un_polish_date_string := month_abbreviated_date_string.replace("sty", "jan")
        .replace("lut", "feb")
        .replace("kwi", "apr")
        .replace("maj", "may")
        .replace("cze", "jun")
        .replace("lip", "jul")
        .replace("sie", "aug")
        .replace("wrz", "sep")
        .replace("paź", "oct")
        .replace("lis", "nov")
        .replace("gru", "dec")
    ) != month_abbreviated_date_string:
        return parse_datetime(un_polish_date_string)

    # Spanish
    if (
        un_spanish_date_string := month_abbreviated_date_string.replace("ene", "jan")
        .replace("abr", "apr")
        .replace("ago", "aug")
        .replace("dic", "dec")
        .replace(" à ", " ")
    ) != month_abbreviated_date_string:
        return parse_datetime(un_spanish_date_string)

    try:
        return datetime.strptime(
            re.sub(r"[^0-9:\-]+", r" ", initial_clean_date_string), "%Y %m %d %H:%M"
        )
    except ValueError:
        pass

    # raise ValueError(f"{date_string} cannot be parsed")
    return None
