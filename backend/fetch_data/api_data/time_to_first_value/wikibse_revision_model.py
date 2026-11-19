"""Wikibase Revision Record"""

from datetime import datetime, timezone

from fetch_data.api_data.constant import WIKIBASE_API_TIMESTAMP_FORMAT


class WikibaseRevisionRecord:
    """Wikibase Revision Record"""

    id: int
    title: str
    log_date: datetime

    def __init__(self, record: dict):
        self.id = record["pageid"]
        self.title = record["title"]
        self.log_date = min(
            datetime.strptime(r["timestamp"], WIKIBASE_API_TIMESTAMP_FORMAT).replace(
                tzinfo=timezone.utc
            )
            for r in record["revisions"]
        )

    def __str__(self) -> str:
        return (
            f"WikibaseRevisionRecord("
            f"id={self.id}, "
            f"title={self.title}, "
            f"log_date={self.log_date})"
        )
