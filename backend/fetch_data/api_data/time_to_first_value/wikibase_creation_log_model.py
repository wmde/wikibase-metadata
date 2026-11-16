"""Wikibase Creation Log Record"""

from datetime import datetime


class WikibaseCreationLogRecord:
    """Wikibase creation Log Record"""

    id: int
    title: str
    log_date: datetime

    def __init__(self, record: dict):
        self.id = record["logid"]
        self.title = record["title"]
        self.log_date = datetime.strptime(record["timestamp"], "%Y-%m-%dT%H:%M:%SZ")

    def __str__(self) -> str:
        return (
            f"WikibaseCreationLogRecord("
            f"id={self.id}, "
            f"title={self.title}, "
            f"log_date={self.log_date})"
        )
