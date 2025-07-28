"""Wikibase Recent Change Record"""

from datetime import datetime
from typing import Optional


class WikibaseRecentChangeRecord:
    """Wikibase Recent Change Record"""

    type: str
    title: str
    user: Optional[str]
    userid: int
    timestamp: datetime
    comment: str
    ns: int

    def __init__(self, record: dict):
        self.type = record["type"]
        self.title = record["title"]
        self.user = record.get("user")
        self.userid = record["userid"]
        self.timestamp = datetime.strptime(record["timestamp"], "%Y-%m-%dT%H:%M:%SZ")
        self.comment = record["comment"]
        self.ns = record["ns"]

    def __str__(self) -> str:
        return (
            f"WikibaseRecentChangeRecord("
            f"type={self.type}, "
            f"title={self.title}, "
            f"user={self.user}, "
            f"timestamp={self.timestamp})"
        )
