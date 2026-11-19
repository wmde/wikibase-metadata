"""Wikibase Creation Log Record"""

from datetime import datetime, timezone

from fetch_data.api_data.constant import WIKIBASE_API_TIMESTAMP_FORMAT


class WikibaseCreationLogRecord:
    """Wikibase Creation Log Record"""

    id: int
    title: str
    log_date: datetime

    def __init__(self, record: dict):
        self.id = record["logid"]
        self.title = record["title"]
        self.log_date = datetime.strptime(
            record["timestamp"], WIKIBASE_API_TIMESTAMP_FORMAT
        ).replace(tzinfo=timezone.utc)

    def __str__(self) -> str:
        return (
            f"WikibaseCreationLogRecord("
            f"id={self.id}, "
            f"title={self.title}, "
            f"log_date={self.log_date})"
        )
