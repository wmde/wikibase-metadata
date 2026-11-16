"""Wikibase Revision Record"""

from datetime import datetime


class WikibaseRevisionRecord:
    """Wikibase Revision Record"""

    id: int
    title: str
    log_date: datetime

    def __init__(self, record: dict):
        self.id = record["pageid"]
        self.title = record["title"]
        self.log_date = min(
            datetime.strptime(r["timestamp"], "%Y-%m-%dT%H:%M:%SZ")
            for r in record["revisions"]
        )

    def __str__(self) -> str:
        return (
            f"WikibaseRevisionRecord("
            f"id={self.id}, "
            f"title={self.title}, "
            f"log_date={self.log_date})"
        )
