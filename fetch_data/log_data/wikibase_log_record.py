"""Create Log Observation"""

from datetime import datetime
from bs4 import NavigableString, Tag
from fetch_data.utils import parse_datetime


class WikibaseLogRecord:
    """Parsing Record from Tag"""

    id: int
    user: str
    log_date: datetime

    def age(self) -> int:
        """Age in Days"""
        return (datetime.now() - self.log_date).days

    def __init__(self, record: Tag):
        self.id = int(record.attrs["data-mw-logid"])
        self.log_date = get_date_from_log(record)
        self.user = get_user_from_log(record)


def get_date_from_log(log: Tag) -> datetime:
    """Get Date from Log - fail if cannot parse"""

    date_string = log.find("a", attrs={"title": "Special:Log"}).string
    result = parse_datetime(date_string)
    if result is not None:
        return result
    raise ValueError(f"Could Not Parse {date_string}")


def get_user_from_log(log: Tag) -> str:
    """Get User from Log"""

    user_tag = log.find("a", attrs={"class": "mw-userlink"})
    if user_tag is None or isinstance(user_tag, NavigableString):
        raise ValueError(f"Could Not Find User in Log: {log}")

    user = user_tag.attrs["title"]
    if not isinstance(user, str):
        raise ValueError(f"User Title Not String in Tag: {user_tag}")

    return user
